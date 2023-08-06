import time
import os
import json
import numpy as np
import subprocess as sp
import pandas as pd
import json
from typing import Dict, Optional
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from datasmash.quantizer import Quantizer, vectorize_label
from datasmash.utils import (genesess, argmax_prod_matrix_list, pprint_dict,
                             predict_random)
from datasmash.d3m_dataset_loader import D3MDatasetLoader
from datasmash.config import CWD, BIN_PATH
from datasmash._version import __version__

#from d3m_metadata import container, hyperparams, metadata as metadata_module, params, utils
#import d3m.metadata as utils
from d3m.metadata import hyperparams, params, base
from d3m import container
from d3m.primitive_interfaces.base import CallResult, DockerContainer
from d3m.primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase


Inputs = container.Dataset
Outputs = container.DataFrame


class Params(params.Params):
    quantizer_params: Optional[dict]


class Hyperparams(hyperparams.Hyperparams):
    depth = hyperparams.UniformInt(
        default = 1000,
        lower = 100,
        upper = 10000,
        description = 'Exponentiated tree depth in inferred Markov Model. ',
        semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter']
    )
    quantizer_core_hours = hyperparams.Bounded(
        default = 28,
        lower = 1,
        upper = None,
        description = ('Number of core-hours one wishes to allot to the'
                       + ' QUANTIZATION the QUANTIZATION PORTION of the algorithm.'),
        semantic_types = ['https://metadata.datadrivendiscovery.org/types/TuningParameter',
                          'https://metadata.datadrivendiscovery.org/types/ResourcesUseParameter']
    )


class d3m_XG2(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """

    """
    __author__ = "UChicago"
    metadata = base.PrimitiveMetadata({
        "algorithm_types": ['HIDDEN_MARKOV_MODEL', 'RANDOM_WALK',
                            'VARIABLE_ORDER_MARKOV_MODEL'],
        "name": "datasmash.d3m_XG2",
        "primitive_family": "TIME_SERIES_CLASSIFICATION",
        "python_path": "d3m.primitives.datasmash.d3m_XG2",
        "source": {
        	'name': 'UChicago',
			'contact': 'mailto:virotaru@uchicago.edu',
            'uris': [ 
                    'https://gitlab.datadrivendiscovery.org/uchicago/datasmash/datasmash/d3m_genesess.py',
                    'https://gitlab.datadrivendiscovery.org/uchicago/datasmash.git',
            ],
		},
        "version": __version__,
        "id": "d989655c-a583-4bc3-94bc-cdd7b3ccb3aa",
        'installation': [
            {'type': base.PrimitiveInstallationType.PIP,
             'package': 'datasmash',
             'version': __version__
            }
        ],
        "keywords": [
            'time',
            'series',
            'data smashing',
            'data-smashing',
            'data_smashing',
            'datasmashing',
            'classification',
            'parameter-free',
            'hyperparameter-free'
        ]
    })


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)


        assert os.path.isfile(os.path.join(BIN_PATH, 'XgenESeSS')), "invalid bin path."
        self._bin_path = BIN_PATH
        self._channel_partition_map = {}
        self._cwd = os.getcwd()
        self._d3m_reader = D3MDatasetLoader()
        self._tmp_dir = ''
        self._channel_dirs = []
        self._selected_channels = set()
        self._detrending = False
        self._inplace = True
        self._channel_probabilities = {}
        self._channel_predictions = {}
        self._fitted = False
        self._depth = self.hyperparams['depth']
        self._quantizer_core_hours = self.hyperparams['quantizer_core_hours']
        self._channels = None

        #if classifier is not None:
        #    self._classifier = classifier
        #else:
        self._classifier = GradientBoostingClassifier(n_estimators=500, max_depth = 5)

    #@property
    #def selected_channels(self):
    #    return self._selected_channels

    #@selected_channels.setter
    #def selected_channels(self, channels):
    #    if not isinstance(channels, list):
    #        channels_ = [channels]
    #    else:
    #        channels_ = channels
    #    channels_ = ['channel_' + str(c) for c in channels_]
    #    self._selected_channels = set(channels_)

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        """
        outputs argument should be specified as None
        """

        print('Datasmash version:',__version__)

        f = open("BUG.txt", "w")
        f.write(str(inputs))
        f.write(str(outputs))
        f.close()
        self._d3m_reader.load_dataset(data=inputs,
                                      train_or_test='train')
        self._tmp_dir, self._channel_dirs, self.channel_problems, self.y = (
            self._d3m_reader.write_libs(problem_type='supervised'))
        self._fitted = False

    def _fit_one_channel(self, directory):
        """

        """
        y = vectorize_label(self.channel_problems['channel_0']['raw_libs'], self.y)
        qtz = Quantizer(problem_type='supervised',
                        num_quantizations='max',
                        #multi_partition=True,
                        core_hours=self._quantizer_core_hours,
                        featurization=genesess,
                        featurization_params={'multi_line': True, 'depth': self._depth})
        X = qtz.fit_transform(directory)
        return X, y, qtz

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
        """

        """
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
            X, self.y, qtz = self._fit_one_channel(channel_dir) # TODO: self.y
            channel_name = os.path.basename(channel_dir)
            self._channel_partition_map[channel_name] = qtz

        #if verbose:
        #    print('Quantizing in place:', self.inplace)
        #    print('Chosen partition:')
        #    pprint_dict(self._channel_partition_map)

        #self._classifier.fit(X, self.y)

        self._fitted = True
        return CallResult(None)

    def produce(self, *, inputs: Inputs, timeout: float = None,
                iterations: int = None) -> CallResult[Outputs]:
        """

        """
        #if partition is not None:
            #    current_partition = partition
            #elif self._channel_partition_map is not None:
                #current_partition = self._channel_partition_map
                #self._d3m_reader.load_dataset(data=inputs,
                #                              train_or_test='test')
        current_partition = self._channel_partition_map
        self._d3m_reader.load_dataset(data=inputs,
                                      train_or_test='test')

        channels = self._channels
        if channels is not None:
            if not isinstance(channels, list):
                channels = [channels]
                if bool(self._selected_channels):
                    for channel in channels:
                        if channel not in self._selected_channels:
                            raise ValueError("The partition was not found for this "
                                             "channel. Re-run 'fit()' with this "
                                             "channel included before running "
                                             "'produce()' with this channel.")

        channel_problems = self._d3m_reader.write_test()

        for channel, problem in channel_problems.items():
            if channels is not None:
                channels_ = ['channel_' + str(c) for c in channels]
                if channel not in channels_:
                    #if verbose:
                        print('Excluding', channel, '...')
                        continue
                elif bool(self._selected_channels) and (channel not in
                                                        self._selected_channels):
                    #if verbose:
                        print('Excluding', channel, '...')
                        continue

            #if verbose:
            #start = time.time()
            test_file = problem['test']


            qtz = current_partition[channel]
            #print(json.dumps(qtz.parameters, indent=4))
            #print(json.dumps(qtz.data, indent=4))

            X = qtz.transform(test_file)

            # Return random predictions if ALL quantizations fail on test set
            if X is None or qtz.training_X is None:
                class_list = self._d3m_reader.class_list
                random_predictions = predict_random(class_list, test_file)
                return CallResult(random_predictions)

            self._classifier.fit(qtz.training_X, self.y)
            predictions = self._classifier.predict(X)
            if not isinstance(inputs, str):
                print('Hacky loader\n')
                stri = str(inputs)
                str_list = stri.split('\'')
                for stri in str_list:
                    if stri.find('file:///')>=0:
                        inputs = stri[7:]
            with open(inputs, 'r') as inputFile:
                datasetSchema = json.load(inputFile)
                inputFile.close()
            dataResources = datasetSchema['dataResources']

            table = next(dataResources[i] for i in range(len(dataResources)) if dataResources[i]['resType'] == 'table')
            tablePath = table['resPath']
            d3mIndex = pd.read_csv(os.path.join(os.path.dirname(inputs), tablePath), usecols=['d3mIndex'])
            trainTargetsCatLabel = next(dataResources[i]['resPath'] for i in range(len(dataResources)) if dataResources[i]['resType'] == 'table')
            for column in table['columns']:
                if 'suggestedTarget' in column['role']:
                    trainTargetsCatLabel = column['colName']


            to_return = pd.DataFrame({'d3mIndex':d3mIndex['d3mIndex'], trainTargetsCatLabel:predictions})           
            return CallResult(container.DataFrame(to_return, generate_metadata=False))

    def get_params(self) -> Params:
        
        return Params(
                    quantizer_params=self.__dict__)


    def set_params(self, *, params: Params) -> None:
        self.__dict__ = params['quantizer_params']






