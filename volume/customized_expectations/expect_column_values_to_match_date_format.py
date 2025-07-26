import pandas as pd
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.execution_engine import PandasExecutionEngine, SparkDFExecutionEngine
from great_expectations.expectations.metrics import ColumnMapMetricProvider, column_condition_partial
import pyspark.sql.functions as F
from pyspark.sql.column import Column as SparkColumn

class ColumnValuesMatchDateFormat(ColumnMapMetricProvider):
    condition_metric_name = "column_values.match_date_format"
    condition_value_keys = ("date_format",)

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column: pd.Series, date_format: str, **kwargs):
        cls._validate_format(date_format)
        date_format = date_format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
        col_dates = pd.to_datetime(column, format=date_format, errors="coerce")
        mask = col_dates.notna()
        return mask

    @column_condition_partial(engine=SparkDFExecutionEngine)
    def _spark(cls, column: SparkColumn, date_format: str, **kwargs):
        cls._validate_format(date_format)
        date_format = date_format.replace("YYYY", "yyyy").replace("DD", "dd")
        regex_map = {
            "yyyy-MM-dd": r"^\d{4}-\d{2}-\d{2}$",
            "yyyy-MM": r"^\d{4}-\d{2}$",
            "yyyy": r"^\d{4}$"
        } # Spark 3.x版本中的新解析器的to_date在遇到无法解析的字符串时会直接抛异常而不是像pandas一样返回空值
        mask = F.when(column.rlike(regex_map[date_format]), \
                      F.to_date(column, date_format).isNotNull()).otherwise(F.lit(False))
        return mask

    @staticmethod
    def _validate_format(date_format: str):
        if date_format not in ["YYYY-MM-DD", "YYYY-MM", "YYYY"]:
            raise ValueError(f"date_format only supports 'YYYY-MM-DD', 'YYYY-MM', 'YYYY'.\
                              The input format is: '{date_format}'")
    
class ExpectColumnValuesToMatchDateFormat(ColumnMapExpectation):
    """
    验证列值是否符合指定的日期格式

    - 默认格式为YYYY-MM-DD，支持YYYY-MM和YYYY格式
    - 支持验证pandas和Spark DataFrame

    示例:
        expect_column_values_to_match_date_format(column="date_column")
        验证当前列的值是否符合YYYY-MM-DD格式
        expect_column_values_to_match_date_format(column="date_column", date_format="YYYY-MM")
        验证当前列的值是否符合YYYY-MM格式
        expect_column_values_to_match_date_format(column="date_column", date_format="YYYY")
        验证当前列的值是否符合YYYY格式

    其他:
        如果需要在result的kwargs中显示参数的值比如date和operator需要显式传入参数而不是使用默认值
    """
    map_metric = "column_values.match_date_format"
    success_keys = ("mostly", "date_format")
    default_kwarg_values = {
        "mostly": 1.0,
        "date_format": "YYYY-MM-DD"
    }

