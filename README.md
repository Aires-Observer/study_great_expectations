# 概念

context：上下文，代表项目实例

asset：数据资产，代表数据源某一时刻的快照

batch：数据资产的快照，实际上数据资产除非覆写否则不会改变，但是只有batch能够参与校验

suite：规则集，数据质量校验规则的集合

validator：校验器，通过绑定suite和batch来执行校验，可以用它添加期望规则、执行数据质量校验、保存校验结果等，不能直接对suite来添加规则，怀疑可能是需要batch中的字段作为参考

checkpoint：可以通过绑定validator执行；也可以通过手动设置来批量校验自动生成数据文档并持久化

# GX初始化

在使用GX前需要初始化工作目录，目的是创建标准化的工作环境和配置文件，确保数据验证流程的规范性和可维护性

初始化命令：`great_exepectation init`

初始化后的目录如下

- `great_expectations/`：根目录，也可能就是 `gx/`，是项目的核心目录，所有配置，规则和输出都存储在这里，其中有一个关键的配置文件 `great_expectation.yml`，这是主配置文件，定义数据源、存储后端、插件等全局设置
- `expectations/`：存储所有的suite，每个suite保存为一个json文件
- `checkpoints/`：定义数据验证的触发点和执行流程，每个checkpoint是一个YAML文件
- `plugins/`：存放自定义的插件或者代码
- `uncommitted/`：存储临时或敏感文件
  - `data_docs/`：自动生成的数据文档（HTML报告），可视化验证结果
  - `validations`：每次验证运行时的详细结果（JSON格式）
  - `config_variables.yml`：敏感配置比如数据库密码，通过环境变量引用

[官方文档链接](https://docs.greatexpectations.io/docs/reference/learn/#)

# 项目环境搭建

项目相关依赖和环境已经写入Dockerfile，可以直接通过创建镜像并运行容器

构建镜像

```bash
docker build -t gx .
```

运行容器

```bash
docker run -it --name gx_test -v "./volume:/app/volume" gx
```

容器运行后会自动初始化GX并进入 `/app/volume`目录，该目录挂载了项目下的 `volume`目录

可以通过手动执行 `auto_testing.py`的方式进行GX验证测试，最终输出 `所有测试脚本均执行成功！`则表示环境搭建无误

同时可以观察到vakudate_result目录下的结果文件发生了修改，这是由于GX结果文件中的验证时间发生了改变

如果不对spark数据源进行测试，参考requirements.txt本地安装相关库依赖也可以运行，注意需要初始化GX
