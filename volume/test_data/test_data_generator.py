import pandas as pd
import numpy as np
from faker import Faker
import os

"""
# Faker 是一个用于生成各种“假数据”的 Python 库，常用于测试、数据填充、演示等场景
# 它可以生成姓名、地址、日期、公司、邮箱、手机号、城市、文本等多种类型的随机数据，且支持多种语言和本地化

from faker import Faker

fake = Faker()

print(fake.name())         # 随机姓名
print(fake.address())      # 随机地址
print(fake.date())         # 随机日期
print(fake.email())        # 随机邮箱
print(fake.city())         # 随机城市
print(fake.company())      # 随机公司名
print(fake.phone_number()) # 随机手机号
"""

# fake = Faker() # 创建Faker实例，Faker库可以生成随机的假数据, 如姓名、地址、日期等
# np.random.seed(42) # 设置随机种子, 以确保每次运行生成相同的随机数据
# # 这说明np.random和random库一样都是伪随机生成

# n_rows = 30
# data = {
#     # np.arange()可以生成一个指定范围内的连续整数序列
#     # 等同于list(range(1001, 1001 + n_rows))
#     "order_id": np.arange(1001, 1001 + n_rows),
#     # np.random.uniform()可以生成指定范围内的多个随机浮点数
#     # 等同于[round(random.uniform(5, 500), 2) for _ in range(n_rows)]
#     "price": np.round(np.random.uniform(5, 500, n_rows), 2),
#     # np.random.choice()可以从指定的列表中随机选择多个元素
#     # 等同于[random.choice(["credit_card", "paypal", "bank_transfer", "cash"]) for _ in range(n_rows)]
#     "payment_method": np.random.choice(["credit_card", "paypal", "bank_transfer", "cash", ""], n_rows),
#     # np.random.randint()可以生成指定范围内的随机整数
#     # 等同于[random.randint(10000, 20000) for _ in range(n_rows)]
#     "user_id": np.random.randint(10000, 20000, n_rows),
#     "product_id": np.random.randint(100, 200, n_rows),
#     "quantity": np.random.randint(1, 10, n_rows),
#     # fake.date_between()可以生成指定范围内的随机日期，-1y表示从今天起往前一年
#     "order_date": [fake.date_between(start_date='-1y', end_date='today') for _ in range(n_rows)],
#     "status": np.random.choice(["paid", "pending", "cancelled", "refunded"], n_rows),
#     # fake.city()可以生成随机城市名称
#     "city": [fake.city() for _ in range(n_rows)],
#     "discount": np.round(np.random.uniform(0, 0.5, n_rows), 2)
# }

# current_dir = os.path.dirname(os.path.abspath(__file__))
# df = pd.DataFrame(data)
# df.to_csv(os.path.join(current_dir, "test_data_02.csv"), index=False, encoding="utf-8")

fake = Faker()
n_rows= 30
data = {
    "order_id": np.arange(1001, 1001 + n_rows),
    "product_date": [fake.date_between(start_date='-3w', end_date='today') for _ in range(n_rows)],
    "order_date": [fake.date_between(start_date='-3w', end_date='today') for _ in range(n_rows)]
}
current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.DataFrame(data)
df.to_csv(os.path.join(current_dir, "test_data_03.csv"), index=False, encoding="utf-8")