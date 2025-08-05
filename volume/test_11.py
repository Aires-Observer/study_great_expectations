import os
import great_expectations as gx
from great_expectations.datasource.fluent import Datasource, DataAsset, BatchRequest
from great_expectations.validator.validator import Validator
import pandas as pd
    
# 之前的验证都是列级别的验证，这里开始进行表级别的验证

current_dir = os.path.dirname(os.path.realpath(__file__))

test_df = pd.read_csv(os.path.join(current_dir, "test_data/test_data_02.csv"))
print(test_df.to_markdown())
context = gx.get_context()
source_name = "test_11_pandas_data_source"
data_source: Datasource = context.sources.add_or_update_pandas(name=source_name)
data_asset: DataAsset = data_source.add_dataframe_asset(name="test_11_asset", dataframe=test_df)
batch_request: BatchRequest = data_asset.build_batch_request()
suite_name = "test_11_suite"
context.add_or_update_expectation_suite(expectation_suite_name=suite_name)
validator: Validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)

validator.expect_table_row_count_to_be_between(min_value=30, max_value=50)
validator.expect_table_row_count_to_equal(30)
validator.expect_table_column_count_to_be_between(min_value=5, max_value=10)
validator.expect_table_column_count_to_equal(11)
validator.expect_table_columns_to_match_ordered_list(column_list=(["new_column"] + list(test_df.columns)))
validator.expect_table_columns_to_match_set(column_set=set(test_df.columns))

results = validator.validate()
with open(os.path.join(current_dir, "result/test_result_11.json"), "w", encoding="utf-8") as f:
    f.write(str(results))
