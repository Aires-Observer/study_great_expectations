import pandas as pd
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "test_data_03.csv")

df = pd.read_csv(csv_path)

# 随机生成上架价格（100~500），折扣（0~0.5），销售价格=上架价格*(1-折扣)
np.random.seed(42)
# np.random.randint() 生成指定100-500内的随机整数，返回一个列表
df["list_price"] = np.random.randint(100, 501, size=len(df))
# np.random.uniform() 生成指定0.1-1内的随机浮点数
# np.round() 保留两位小数
df["discount"] = np.round(np.random.uniform(0.1, 0.9, size=len(df)), 2)
df["sale_price"] = np.round(df["list_price"] * (1 - df["discount"]), 2)

# 保存新文件
df.to_csv(csv_path, index=False, encoding="utf-8")