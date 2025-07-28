FROM python:3.11.7-slim
# 只需要单机spark环境测试不需要通过spark镜像构建
# 安装pyspark库即可
WORKDIR /app

RUN apt-get update && \
    apt-get install -y expect \
    openjdk-17-jre-headless

# 修改环境变量确保great_expectation初始化可以正常进行
ENV PATH="/.local/bin:$PATH"
# pyspark的运行需要java环境
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"

COPY utils/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY utils/init_gx.sh /app/init_gx.sh
RUN chmod +x /app/init_gx.sh && expect /app/init_gx.sh

CMD ["/bin/bash", "-c", "cd /app/volume && exec /bin/bash"]