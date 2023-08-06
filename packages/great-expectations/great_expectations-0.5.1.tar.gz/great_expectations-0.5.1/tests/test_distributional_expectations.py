# import pytest

# import numpy as np
# from .test_utils import CONTEXTS, get_dataset

# from great_expectations.dataset.sqlalchemy_dataset import SqlAlchemyDataset

# @pytest.fixture(params=CONTEXTS)
# def non_json_dataset(request):
#     """Provide dataset fixtures that have special values and/or are otherwise useful outside
#     the standard json testing framework"""
#     data = {
#         "infinities": [-np.inf, -10, -np.pi, 0, np.pi, 10/2.2, np.inf],
#         "nulls": [np.nan, None, 0, 1.1, 2.2, 3.3, None],
#         "naturals": [1, 2, 3, 4, 5, 6, 7]
#     }
#     schemas = {
#         "pandas": {
#             "infinities": "float64",
#             "nulls": "float64",
#             "naturals": "float64"
#         },
#         "postgresql": {
#             "infinities": "float",
#             "nulls": "float",
#             "naturals": "float"
#         },
#         "sqlite": {
#             "infinities": "float",
#             "nulls": "float",
#             "naturals": "float"
#         }
#     }
#     return get_dataset(request.param, data, schemas=schemas)


# # def test_expect_column_bootstrapped_ks_test_p_value_to_be_greater_than_bad_partition(non_json_dataset):
# #     if isinstance(non_json_dataset, SqlAlchemyDataset):
# #         # Known not implemented yet
# #         return

# #     with pytest.raises(ValueError):
# #         non_json_dataset.expect_column_bootstrapped_ks_test_p_value_to_be_greater_than(
# #             'naturals', {'bins': [-np.inf, 0, 1, 2, 3], 'weights': [0.25, 0.25, 0.25, 0.25]})