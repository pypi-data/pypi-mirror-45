import time
import os
import shutil
from d3m.base import utils as base_utils
import pandas.api.types as ptypes # can use?
from typing import Dict, Optional
from sklearn.ensemble import RandomForestClassifier
from datasmash.quantizer import Quantizer, vectorize_label
from datasmash.utils import xgenesess, argmax_prod_matrix_list, pprint_dict
from datasmash.d3m_dataset_loader import D3MDatasetLoader
from datasmash.config import CWD, BIN_PATH
from datasmash._version import __version__
from d3m import container, utils as d3m_utils
#from d3m_metadata import container, hyperparams, metadata as metadata_module, params, utils
from d3m.metadata import hyperparams, params, base
from d3m.container import dataset, numpy, pandas
from d3m.primitive_interfaces.base import CallResult, DockerContainer
from d3m.primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase


Inputs = container.Dataset
Outputs = container.DataFrame


class Params(params.Params):
    quantizer_params: Optional[dict]


class Hyperparams(hyperparams.Hyperparams):
    pass


class d3m_Quantizer(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """

    """
    __author__ = "UChicago"
    metadata = base.PrimitiveMetadata({
        "algorithm_types": ['HIDDEN_MARKOV_MODEL', 'RANDOM_WALK',
                            'VARIABLE_ORDER_MARKOV_MODEL'],
        "name": "datasmash.d3m_Quantizer",
        "primitive_family": "TIME_SERIES_CLASSIFICATION",
        "python_path": "d3m.primitives.datasmash.d3m_Quantizer",
        "source": {
        	'name': 'UChicago',
			'contact': 'mailto:virotaru@uchicago.edu',
            'uris': [ 
                    'https://gitlab.datadrivendiscovery.org/uchicago/datasmash/datasmash/d3m_quantizer.py',
                    'https://gitlab.datadrivendiscovery.org/uchicago/datasmash.git',
            ],
		},
        "version": __version__,
        "id": "3b593a75-fd8f-4779-8489-2ab69e4bf55a",
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

        self._d3m_reader = D3MDatasetLoader()
        self._qtz = None
        self._fitted = False

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        """
        outputs argument should be specified as None
        """
        self._d3m_reader.load_dataset(data=inputs,
                                      train_or_test='train')
        self._tmp_dir, self._channel_dirs, self.channel_problems, self.y = (
            self._d3m_reader.write_libs(problem_type='supervised'))
        self._fitted = False
        print(self._channel_dirs)

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
        """

        """
        qtz = Quantizer(problem_type='supervised',
                        num_quantizations=1,
                        #multi_partition=True,
                        core_hours=1000000,
                        featurization=None,
                        featurization_params=None)
                        #xgenesess_hours=self._xgenesess_hours)
        qtz.fit_transform(self._tmp_dir + '/channel_0')
        self._qtz = qtz
        return CallResult(None) 

    def produce(self, *, inputs: Inputs, timeout: float = None,
                iterations: int = None) -> CallResult[Outputs]:
        metadata1 = inputs.metadata
        dataframe_resource_id, dataframe = base_utils.get_tabular_resource(inputs, None) 
        metadata1 = self._update_metadata(inputs.metadata, dataframe_resource_id)
        self._d3m_reader.load_dataset(data=inputs, train_or_test='test')
        channel_problems = self._d3m_reader.write_test()
        to_Return = self._qtz.transform(self._tmp_dir + '/test/channel_0/test')
        final = container.DataFrame(to_Return)
        metadata1 = metadata1.update((), {
            'dimension': {
                'length': to_Return.shape[1],
            },
        })
        for col in range(to_Return.shape[1]):
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