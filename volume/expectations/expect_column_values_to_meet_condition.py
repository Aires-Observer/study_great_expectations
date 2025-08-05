import pandas as pd
from great_expectations.expectations.expectation import ColumnPairMapExpectation
from great_expectations.execution_engine import PandasExecutionEngine, SparkDFExecutionEngine
from great_expectations.expectations.metrics.map_metric_provider import ColumnPairMapMetricProvider, column_pair_condition_partial
from pyspark.sql.column import Column as SparkColumn
from pyspark.sql import functions as F

class ColumnValuesCompareCondition(ColumnPairMapMetricProvider):
    condition_metric_name = "column_values.compare_condition"
    condition_value_keys = ("operator",)  # 只需要比较符

    @column_pair_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column_A: pd.Series, column_B: pd.Series, **kwargs):
        operator = kwargs["operator"]
        col_A = pd.to_numeric(column_A, errors="coerce")
        col_B = pd.to_numeric(column_B, errors="coerce")
        mask = col_A.notna() & col_B.notna() & cls._get_operator(col_A, col_B, operator)
        return mask

    @column_pair_condition_partial(engine=SparkDFExecutionEngine)
    def _spark(cls, column_A: SparkColumn, column_B: SparkColumn, **kwargs):
        operator = kwargs["operator"]
        col_A = F.when(F.trim(column_A) != "", F.col(column_A).cast("double")).otherwise(None)
        col_B = F.when(F.trim(column_B) != "", F.col(column_B).cast("double")).otherwise(None)
        mask = col_A.isNotNull() & col_B.isNotNull() & cls._get_operator(col_A, col_B, operator)
        return mask

    @staticmethod
    def _get_operator(a, b, operator):
        ops = {
            ">=": a >= b,
            "<=": a <= b,
            ">": a > b,
            "<": a < b,
            "==": a == b
        }
        if operator not in ops:
            raise ValueError(f"Unsupported operator: {operator}. Supported operators are: {', '.join(ops.keys())}")
        return ops[operator]

class ExpectColumnValuesToMeetCompareCondition(ColumnPairMapExpectation):
    """
    比较两列数值大小关系

    - 默认比较符为"==", 支持">=", "<=", ">", "<", "=="

    示例:
        expect_column_values_to_meet_compare_condition(column_A="list_price", column_B="sale_price", operator=">=")
    """
    map_metric = "column_values.compare_condition"
    success_keys = ("mostly", "column_A", "column_B", "operator", "ignore_row_if")
    default_kwarg_values = {
        "mostly": 1.0,
        "operator": "==",
        "ignore_row_if": "either_value_is_missing"
    }