# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import numpy as np
import pandas
import scipy.sparse as sparse
from sklearn.pipeline import Pipeline

from .feature_mappers import encoders_to_mappers_dict, get_feature_mapper_for_pipeline, IdentityMapper, \
    PassThroughMapper, FuncTransformer


class DataMapper(object):
    """Class to transform raw features to engineered features using list of transformations."""

    def __init__(self, transformations=None):
        """Initialize DataMapper object.

        :param transformations: List of (column_name, transformer) tuples.
        :type transformations: (str, (class containing .transform method))
        :param examples: DataFrame or numpy array of input
        :type examples: pandas.DataFrame or numpy.array
        """
        self._transformations = self._build_transformations_pipeline(transformations)
        self._feature_map = None

    @property
    def feature_map(self):
        """Feature map from raw to generated.

        :return: mapping from raw to generated features
        :rtype: [[int]]
        """
        if not self._feature_map:
            raise ValueError("feat map not built. Run Transform first.")
        return self._feature_map

    def _build_transformations_pipeline(self, transformations):
        """Generate a list of FeatureMappers that can transform as well as contain a featmap property

        :param transformations: from a list of composed transformations, generate featuremappers.
        :type transformations: [Transformation]
        :return: list of tuples of columns and Featuremapper
        :rtype: [(str, FeatureMapper)]
        """
        result = []
        for columns, tr in transformations:
            result.append((columns, self._get_feature_mapper(tr, columns)))

        return result

    def _extract_column(self, x, columns):
        """Extract column from dataframe/numpy array x and reshape if column_name is list.

        :param x: input raw data
        :type x: numpy array or pandas.DataFrame
        :param columns: columns names as a list or a single column as a string
        :type columns: str or [str]
        :return: column or columns from input data
        :rtype: numpy.array
        """
        if isinstance(x, pandas.DataFrame):
            x_column = x[columns].values
        else:
            x_column = x[:, columns]
        if isinstance(columns, list) and len(columns) == 1:
            x_column = x_column.reshape(-1, 1)

        return x_column

    def _get_feature_mapper(self, transformer, columns):
        """Get FeatureMapper from transformer and columns list that can also get the associated featmap.

        :param transformer: object that has a transform method
        :type transformer: class that has a transform method
        :param columns: list of columns or a single column
        :type columns: [str] or str
        :return: feature mapper associated with the transformer
        :rtype: FeatureMapper
        """
        # if there is only one column, we can just look at the shape of final transformers and get result
        is_list = isinstance(columns, list)
        if (is_list and len(columns) == 1) or (not is_list):
            if transformer is None:
                if is_list:
                    return IdentityMapper(FuncTransformer(lambda x: x))
                else:
                    return IdentityMapper(FuncTransformer(lambda x: x.reshape(-1, 1)))
            else:
                return PassThroughMapper(transformer)

        # if it is one of the supported transformations
        transformer_type = type(transformer)
        if transformer_type in encoders_to_mappers_dict:
            return encoders_to_mappers_dict[transformer_type](transformer)

        if isinstance(transformer, Pipeline):
            return get_feature_mapper_for_pipeline(transformer)

        # its a many to many or many to one map if we end up here
        raise ValueError("Many to many or many to one transformers not supported in raw explanations.")

    def _add_num_to_list_of_lists(self, num, list_of_list):
        """For a sequence of transformers in DataMappers, feature mapping from transformers need to add the number of
        columns generated from the previous set of transformers to their mapping in order to get the correct index of
        generated column. This helper function adds an integer to the integers in the list of lists which is the
        feature mapping.

        :param num: number to be added to the integers in list_of_list
        :type num: int
        :param list_of_list: feature map
        :type list_of_list: [[int]]
        :return: list of lists
        :rtype: [[int]]
        """
        result = []
        for lst in list_of_list:
            result.append([num + i for i in lst])
        return result

    def _build_feature_map(self, columns):
        """Build the feature map from the feature maps of list of transformation wrappers in DataMapper.

        :param columns: input columns either as string names for dataframe or list of integers for numpy array
        :type columns: [str] or [int]
        """

        raw_to_engineered_map = {}
        last_num_cols = 0
        for column_names, transform_wrapper in self._transformations:
            raw_to_engineered = self._add_num_to_list_of_lists(last_num_cols, transform_wrapper.feature_map)

            if not isinstance(column_names, list):
                column_names = [column_names]

            for i, col in enumerate(column_names):
                if col not in raw_to_engineered_map:
                    raw_to_engineered_map[col] = []
                raw_to_engineered_map[col].extend(raw_to_engineered[i])

            # number of cols in engineered until this transformation
            last_num_cols += sum([len(x) for x in raw_to_engineered])

        feature_map = []
        # return the results in the order the columns are in the input
        for col in columns:
            feature_map.append(raw_to_engineered_map.get(col, []))

        self._feature_map = feature_map

    def transform(self, x):
        """Transform input data given the transformations.

        :param x: input data
        :type x: pandas.DataFrame or numpy array
        :return: transformed data
        :rtype: numpy.array or scipy.sparse matrix
        """
        results = []
        for columns, tr in self._transformations:
            x_column = self._extract_column(x, columns)
            results.append(tr.transform(x_column))

        if self._feature_map is None:
            columns = x.columns if isinstance(x, pandas.DataFrame) else list(range(x.shape[1]))
            self._build_feature_map(columns)

        if any(map(sparse.issparse, results)):
            return sparse.hstack(results).tocsr()
        else:
            return np.hstack(tuple(results))
