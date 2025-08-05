# 自定义期望的继承关系

GX版本：0.18.21

```python
MetricProvider
    QueryMetricProvider
    TableMetricProvider
        ColumnAggregateExpectation
    MapMetricProvider
        ColumnMapMetricProvider
            RegexColumnMapMetricProvider
            SetColumnMapMetricProvide
        ColumnPairMapMetricProvider
        MulticolumnMapExpectation
	MulticolumnMapMetricProvider
```

## 单列值校验

### 普通校验

```python
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import ColumnMapMetricProvider, column_condition_partial
```

## 两列值校验

```python
from great_expectations.expectations.expectation import ColumnPairMapExpectation
from great_expectations.expectations.metrics.map_metric_provider import ColumnPairMapMetricProvider, column_pair_condition_partial
```

## 多列值校验

```python
from great_expectations.expectations.expectation import MulticolumnMapExpectation
from great_expectations.expectations.metrics.map_metric_provider import MulticolumnMapMetricProvider, multicolumn_condition_partial
```
