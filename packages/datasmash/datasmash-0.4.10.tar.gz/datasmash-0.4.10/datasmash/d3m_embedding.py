import os
import subprocess as sp
import numpy as np
import json
import typing
import pandas as pd
from typing import Dict
import tempfile
import shutil
from distutils.dir_util import copy_tree
from datasmash.utils import pprint_dict, matrix_list_p_norm, smash
from datasmash.d3m_dataset_loader import D3MDatasetLoader
from datasmash.quantizer import Quantizer, fit_one_channel
from datasmash.config import BIN_PATH
from datasmash._version import __version__
from sklearn.manifold import MDS

from d3m.base import utils as base_utils
from d3m.metadata import hyperparams, params, base
from d3m import container 
from d3m.primitive_interfaces.base import CallResult, DockerContainer
from d3m.primitive_interfaces.featurization import FeaturizationLearnerPrimitiveBase


Inputs = container.Dataset
Outputs = container.DataFrame


class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    n_components = hyperparams.Hyperparameter[int](
        default = 2,
        description = 'Number of features to create from each time series. ',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter']
    )
    quantizer_core_hours = hyperparams.Bounded(
        default = 28,
        lower = 1,
        upper = None,
        description = ('Number of core-hours one wishes to allot to the'
                       + ' QUANTIZATION PORTION of the algorithm.'),
        semantic_types = ['https://metadata.datadrivendiscovery.org/types/TuningParameter',
                          'https://metadata.datadrivendiscovery.org/types/ResourcesUseParameter']
    )


class d3m_SmashEmbedding(FeaturizationLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """

    """
    __author__ = "UChicago"
    metadata = base.PrimitiveMetadata({
        "algorithm_types": ['HIDDEN_MARKOV_MODEL', 'RANDOM_WALK',
                            'VARIABLE_ORDER_MARKOV_MODEL'],
        "name": "datasmash.d3m_SmashEmbedding",
        "primitive_family": "EVALUATION",
        "python_path": "d3m.primitives.datasmash.d3m_SmashEmbedding",
        "source": {
        	'name': 'UChicago',
			'contact': 'mailto:virotaru@uchicago.edu',
            'uris': [ 
                    'https://gitlab.datadrivendiscovery.org/uchicago/datasmash/datasmash/d3m_embedding.py',
                    'https://gitlab.datadrivendiscovery.org/uchicago/datasmash.git',
            ],
		},
        "version": __version__,
        "id": "1df5f748-122f-45a7-aff8-46cf5332c097",
        'installation': [
            {'type': base.PrimitiveInstallationType.PIP,
             'package': 'datasmash',
             'version': __version__
            }
        ],
        "hyperparameters_to_tune": [
            "n_components"
        ],
        "keywords": [
            'time',
            'series',
            'data smashing',
            'data-smashing',
            'data_smashing',
            'datasmashing',
            'feature construction',
            'embed'
            'embedding',
            'featurization',
            'parameter-free',
            'hyperparameter-free'
        ]
    })


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        assert os.path.isfile(os.path.join(BIN_PATH, 'smash')), "Error: invalid bin path."
        self._bin_path = os.path.abspath(os.path.join(BIN_PATH, 'smash'))
        self._cwd = os.getcwd()
        self._d3m_reader = D3MDatasetLoader()
        self._tmp_dir = ''
        self._channel_dirs = []
        self._channel_partition_map = {}
        self._selected_channels = set()
        self._num_streams = 0

        self._channels = None
        self._train_path = None

        self._n_components = self.hyperparams['n_components']
        self._embed_class = MDS(n_components=self._n_components, dissimilarity='precomputed')
        self._quantizer_core_hours = self.hyperparams['quantizer_core_hours']

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None: 
        data = inputs
        if not isinstance(data, str):
            stri = str(data)
            str_list = stri.split('\'')
            for stri in str_list:
                if stri.find('file:///')>=0:
                    self._train_path = os.path.dirname(os.path.dirname(stri[7:]))
        
    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:        
        return CallResult(None)
        
        
    def produce(self, *, inputs: Inputs, timeout: float = None,
                iterations: int = None) -> CallResult[Outputs]:
        """

        """    
        metadata1 = inputs.metadata
        dataframe_resource_id, dataframe = base_utils.get_tabular_resource(inputs, None) 
        metadata1 = self._update_metadata(inputs.metadata, dataframe_resource_id)         
        data = inputs
        if not isinstance(data, str):
            stri = str(data)
            str_list = stri.split('\'')
            for stri in str_list:
                if stri.find('file:///')>=0:
                    TEST_DIR = os.path.dirname(os.path.dirname(stri[7:]))
        TRAIN_DIR = self._train_path   
        if (TEST_DIR.find('TEST'))!=-1:
            _test = 'TEST'
        else:
            _test = 'TRAIN'
        if (TRAIN_DIR.find('TEST'))!=-1:
            _train = 'TEST'
        else:
            _train = 'TRAIN'
        with open(os.path.join(TEST_DIR, 'dataset_' + _test, 'datasetDoc.json' ) , 'r') as inputFile:
            datasetSchema = json.load(inputFile)
            inputFile.close()
        # Load the problem description schema
        with open(os.path.join(TRAIN_DIR, 'problem_' + _train, 'problemDoc.json' ) , 'r') as inputFile:
            problemSchema = json.load(inputFile)
            inputFile.close()
        # get the paths of the training and test sets from the configuration json
        TRAIN_DATA = os.path.join(TRAIN_DIR, 'dataset_' +  _train, 'datasetDoc.json')
        TEST_DATA = os.path.join(TEST_DIR, 'dataset_' +  _test, 'datasetDoc.json')

        # get test d3mIndices
        dataResources = datasetSchema['dataResources']
        table = next(dataResources[i] for i in range(len(dataResources)) if dataResources[i]['resType'] == 'table')
        tablePath = table['resPath']
        d3mIndex = pd.read_csv(os.path.join(TEST_DIR, 'dataset_' +  _test, tablePath), usecols=['d3mIndex'])

        trainTargetsCatLabel = next(dataResources[i]['resPath'] for i in range(len(dataResources)) if dataResources[i]['resType'] == 'table')


        # Check that the problem is timeseries_classification and
        # find the train directory with timeseries .csv files and learningData.csv
        is_timeseries_data = 0
        for resource in datasetSchema['dataResources']:
            if resource['resType'] == 'timeseries':
                is_timeseries_data = 1
                train_timeseries_dir = resource['resPath']
            elif resource['resType'] == 'table':
                train_learningData_csv = resource['resPath']
        #learning_data = pd.read_csv(os.path.join(jsonCall['train_data'],
        #                                         'dataset_TRAIN',
        #                                         train_learningData_csv))
        learning_data = pd.read_csv(os.path.join(TRAIN_DIR, 'dataset_' +  _train, train_learningData_csv))
        train_range = len(learning_data)

        if not is_timeseries_data:
            print("Problem is not of type 'TIMESERIES_CLASSIFICATION'. Exiting.")
            exit(1)

        with open(os.path.join(TEST_DIR, 'dataset_' +  _test,
                               'datasetDoc.json'), 'r') as inputFile:
            test_datasetSchema = json.load(inputFile)

        # find the test directory with timeseries .csv files and learningData.csv
        for resource in test_datasetSchema['dataResources']:
            if resource['resType'] == 'timeseries':
                test_timeseries_dir = resource['resPath']
            elif resource['resType'] == 'table':
                test_learningData_csv = resource['resPath']
        #test_learning_data = pd.read_csv(os.path.join(jsonCall['test_data'],
        #                                              'dataset_TEST',
        #                                              test_learningData_csv))
        test_learning_data = pd.read_csv(os.path.join(TEST_DIR, 'dataset_' +  _test, test_learningData_csv))

        # create a temporary directory which will be a concatenation of the training
        # and test data
        tmp_dir = tempfile.mkdtemp(dir='./')

        # copy over the dataset_TRAIN directory first
        #shutil.copytree(os.path.join(jsonCall['train_data'], 'dataset_TRAIN'),
        #                os.path.join(tmp_dir, 'dataset_TRAIN'))

        shutil.copytree(os.path.join(TRAIN_DIR, 'dataset_' +  _train),
                        os.path.join(tmp_dir, 'dataset_' +  _train))

        # combine the train and test learningData.csv files and save them in the
        # temporary directory
        combined_learning_data = pd.concat([learning_data, test_learning_data])
        combined_learning_data.to_csv(os.path.join(tmp_dir, 'dataset_' +  _train,
                                                   train_learningData_csv), index=False)

        # copy the test timeseries .csv files over to the temporary train timeseries
        # directory 
        #copy_tree(os.path.join(jsonCall['test_data'], 'dataset_TEST',
        copy_tree(os.path.join(TEST_DIR, 'dataset_' +  _test,
                               test_timeseries_dir), os.path.join(tmp_dir,
                                                                  'dataset_' +  _train,
                                                                  train_timeseries_dir))

        dataResources = datasetSchema['dataResources']
        table = next(dataResources[i] for i in range(len(dataResources)) if dataResources[i]['resType'] == 'table')
        for column in table['columns']:
            if 'suggestedTarget' in column['role']:
                trainTargetsCatLabel = column['colName']

        TRAIN_DATA = os.path.join(tmp_dir, 'dataset_' +  _train,'datasetDoc.json')
        inputs = TRAIN_DATA
        print('Datasmash version:',__version__)
        self._d3m_reader.load_dataset(data=inputs,
                                      train_or_test='train')
        self._tmp_dir, self._channel_dirs, self._num_streams = self._d3m_reader.write_libs(problem_type='unsupervised')

        channels = self._channels
        if channels is not None:
            if channels == -1:
                pass
            elif not isinstance(channels, list):
                channels = [channels]
            selected_channels = ['channel_' + str(c) for c in channels]
            self._selected_channels = set(selected_channels)
        elif bool(self._selected_channels):
            selected_channels = self._selected_channels
        else:
            selected_channels = self._channel_dirs

        for channel_dir in selected_channels:
            X, qtz = fit_one_channel(channel_dir, problem_type='unsupervised',
                                     num_quantizations=1,
                                     #multi_partition=False,
                                     core_hours=self._quantizer_core_hours)
            channel_name = os.path.basename(channel_dir)
            self._channel_partition_map[channel_name] = (X, qtz)

        #if verbose:
        #print('Chosen partition:')
        #pprint_dict(self._channel_partition_map)

        # run smash to get the distance matrix

        distance_matrices = []
        for channel_dir, (X, _) in self._channel_partition_map.items():
            channel_path = os.path.join(self._tmp_dir, channel_dir)
            #input_data = os.path.join(channel_path, 'dataset')
            #X.to_csv(input_data, sep=' ', header=False, index=False)
            output_file = os.path.join(channel_path, 'H.dst')
            results = smash(X[0], outfile=output_file)
            distance_matrices.append(results)

        final_dist_matrix = matrix_list_p_norm(distance_matrices, p=2)
        feature_vector = self._embed_class.fit_transform(results)
        to_return = pd.DataFrame(feature_vector[train_range: , ]) 
 #       metadata1 = metadata.update((), {
   #         'dimension': {
   #             'length': len(to_return),
   #         },
   #     })


        final = container.DataFrame(to_return)
        metadata1 = metadata1.update((), {
            'dimension': {
                'length': self.hyperparams['n_components'],
            },
        })
        for col in range(self.hyperparams['n_components']):
            metadata1 = metadata1.update((base.ALL_ELEMENTS, col), {'structural_type': float})
            metadata1 = metadata1.update((base.ALL_ELEMENTS, col), {'semantic_types': ['https://metadata.datadrivendiscovery.org/types/Attribute']})
        #outputs_metadata = inputs_metadata.select_columns([column_index])
        #outputs_metadata.update_column(0, {'structural_type': float})
        index_columns = metadata1.get_index_columns()
        column_metadata = metadata1.query((base.ALL_ELEMENTS, 1))
        semantic_types = column_metadata.get('structural_type', [])
        #'https://metadata.datadrivendiscovery.org/types/CategoricalData'
        final.metadata = metadata1 
        return CallResult(final)
    
    
    def _update_metadata(cls, metadata: base.DataMetadata, resource_id: base.SelectorSegment) -> base.DataMetadata:
        resource_metadata = dict(metadata.query((resource_id,)))

        if 'structural_type' not in resource_metadata or not issubclass(resource_metadata['structural_type'], container.DataFrame):
            raise TypeError("The Dataset resource is not a DataFrame, but \"{type}\".".format(
                type=resource_metadata.get('structural_type', None),
            ))

        resource_metadata.update(
            {
                'schema': base.CONTAINER_SCHEMA_VERSION,
            },
        )

        new_metadata = base.DataMetadata(resource_metadata)

        new_metadata = metadata.copy_to(new_metadata, (resource_id,))

        # Resource is not anymore an entry point.
        new_metadata = new_metadata.remove_semantic_type((), 'https://metadata.datadrivendiscovery.org/types/DatasetEntryPoint')

        return new_metadata

    
    def get_params(self) -> Params:
        
        return Params(
                    quantizer_params=self.__dict__)


    def set_params(self, *, params: Params) -> None:
        self.__dict__ = params['quantizer_params']
