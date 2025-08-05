import os
import pandas as pd
import great_expectations as gx
from great_expectations.datasource.fluent import Datasource, DataAsset, BatchRequest
from great_expectations.validator.validator import Validator
from pyspark.sql import SparkSession
import expectations
    
# 临时测试各种新的期望和功能
current_dir = os.path.dirname(os.path.realpath(__file__))

# 创建 Spark Session
spark = SparkSession.builder.appName("gx_test").getOrCreate()

# 读取数据
spark_df = spark.read.csv(os.path.join(current_dir, "test_data/test_data_03.csv"), header=True, inferSchema=True)
pandas_df = pd.read_csv(os.path.join(current_dir, "test_data/test_data_03.csv"))

context = gx.get_context()

# ===== Spark 测试 =====
print("=== Testing Spark Engine ===")
spark_source_name = "temp_test_spark_data_source"
spark_data_source: Datasource = context.sources.add_or_update_spark(name=spark_source_name)
spark_data_asset: DataAsset = spark_data_source.add_dataframe_asset(name="temp_test_spark_asset", dataframe=spark_df)
spark_batch_request: BatchRequest = spark_data_asset.build_batch_request()
spark_suite_name = "temp_test_spark_suite"
context.add_or_update_expectation_suite(expectation_suite_name=spark_suite_name)
spark_validator: Validator = context.get_validator(batch_request=spark_batch_request, expectation_suite_name=spark_suite_name)

spark_validator.expect_columns_arithmetic_to_equals_result_column(left_column="list_price", right_column="discount", result_column="sale_price", operator="*", column_list=["list_price", "discount", "sale_price"])

# ===== pandas 测试 =====
print("=== Testing Pandas Engine ===")
pandas_source_name = "temp_test_pandas_data_source"
pandas_data_source: Datasource = context.sources.add_or_update_pandas(name=pandas_source_name)
pandas_data_asset: DataAsset = pandas_data_source.add_dataframe_asset(name="temp_test_pandas_asset", dataframe=pandas_df)
pandas_batch_request: BatchRequest = pandas_data_asset.build_batch_request()
pandas_suite_name = "temp_test_pandas_suite"
context.add_or_update_expectation_suite(expectation_suite_name=pandas_suite_name)
pandas_validator: Validator = context.get_validator(batch_request=pandas_batch_request, expectation_suite_name=pandas_suite_name)

pandas_validator.expect_columns_arithmetic_to_equals_result_column(left_column="list_price", right_column="discount", result_column="sale_price", operator="*", column_list=["list_price", "discount", "sale_price"])

# ===== 验证结果 =====
result_format = {
    "result_format": "COMPLETE", 
    "unexpected_index_column_names": ["order_id"],
    "return_unexpected_index_query": True,
}

print("=== Spark Results ===")
spark_results = spark_validator.validate(result_format=result_format)
with open(os.path.join(current_dir, "result/temp_test_result_spark.json"), "w", encoding="utf-8") as f:
    f.write(str(spark_results))

print("=== Pandas Results ===")
pandas_results = pandas_validator.validate(result_format=result_format)
with open(os.path.join(current_dir, "result/temp_test_result_pandas.json"), "w", encoding="utf-8") as f:
    f.write(str(pandas_results))

print("Testing completed!")