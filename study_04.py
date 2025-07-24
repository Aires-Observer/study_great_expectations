import os
import pandas as pd
import great_expectations as gx
from great_expectations.datasource.fluent import Datasource, DataAsset, BatchRequest
from great_expectations.validator.validator import Validator
from customized_expectations import ExpectColumnValuesIsGreaterOrEqualToday

current_dir = os.path.dirname(os.path.realpath(__file__))

# 1. 读取测试数据
test_df = pd.read_csv(os.path.join(current_dir, "test_data_02.csv"))
print(test_df.to_markdown())

# 2. 获取GX context
context = gx.get_context()

# 3. 注册pandas数据源
source_name = "test_04_pandas_data_source"
data_source: Datasource = context.sources.add_or_update_pandas(name=source_name)

# 4、创建数据资产
data_asset: DataAsset = data_source.add_dataframe_asset(name="test_04_asset", dataframe=test_df)

# 5. 创建批处理请求
batch_request: BatchRequest = data_asset.build_batch_request()

# 6. 创建期望规则集
suite_name = "test_04_suite"
suite = context.add_or_update_expectation_suite(expectation_suite_name=suite_name)

# 7. 获取验证器
validator: Validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)

# 8. 添加期望规则
validator.expect_column_values_is_greater_or_equal_today(column="order_date", date = '2024-09-08', operator=">=")

# 10、统一设置输出格式
result_format = {
    "result_format": "COMPLETE", 
    "unexpected_index_column_names": ["order_id"],
    "return_unexpected_index_query": True,
}

# 10. 执行校验
results = validator.validate(result_format=result_format)

# 9. 输出校验结果
with open(os.path.join(current_dir, "test_result_04.json"), "w", encoding="utf-8") as f:
    f.write(str(results))

