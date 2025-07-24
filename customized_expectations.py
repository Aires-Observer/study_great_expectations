import pendulum
import pandas as pd
from great_expectations.expectations.expectation import Expectation

class ExpectColumnValuesIsGreaterOrEqualToday(Expectation):
    """验证列值是否符合YYYY-MM-DD格式并且大于等于传入日期（默认今天）"""
    metric_dependencies = ()
    success_keys = ("column", "mostly")

    def _validate(self, configuration, metrics, runtime_configuration=None, execution_engine=None):
        column = configuration.kwargs["column"]
        default_date = pendulum.now("Asia/Hong_Kong").date().to_date_string()
        date: str = configuration.kwargs.get("date", default_date) # 默认为香港的当天日期
        operator = configuration.kwargs.get("operator", "==") # 支持">=", "<=", ">", "<", "=="
        mostly = configuration.kwargs.get("mostly", 1.0)
        df = execution_engine.dataframe

        if isinstance(df, pd.DataFrame):
            success, element_count, unexpected_count, unexpected_percent, \
            unexpected_list, unexpected_index_list = self._pandas_grammar(df, column, mostly, date, operator)
        
        return {
            "success": success,
            "result": {
                "element_count": element_count,
                "unexpected_count": unexpected_count,
                "unexpected_percent": unexpected_percent,
                "unexpected_list": unexpected_list,
                "unexpected_index_list": unexpected_index_list
            }
        }

    @staticmethod
    def _pandas_grammar(df, column, mostly, date: str, operator: str):
        col_dates = pd.to_datetime(df[column], format="%Y-%m-%d", errors="coerce")
        date = pd.to_datetime(date)
        ops = {
            ">=": col_dates >= date,
            "<=": col_dates <= date,
            ">": col_dates > date,
            "<": col_dates < date,
            "==": col_dates == date
        }
        if operator not in ops:
            raise ValueError(f"Unsupported operator: {operator}. Supported operators are: {', '.join(ops.keys())}")
        
        condition_mask = col_dates.notna() & ops[operator] # 101100011...
        expected_percent = condition_mask.mean()
        success = expected_percent >= mostly
        unexpected_percent = round((1 - expected_percent) * 100, 1)
        element_count = len(df)
        unexpected_list = df.loc[~condition_mask, column].tolist()
        unexpected_count = len(unexpected_list)
        unexpected_index_list = df.index[~condition_mask].tolist()
        return success, element_count, unexpected_count, unexpected_percent, unexpected_list, unexpected_index_list
