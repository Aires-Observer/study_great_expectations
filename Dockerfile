FROM python:3.11.7-slim
# 只需要单机spark环境测试不需要通过spark镜像构建
# 安装pyspark库即可
WORKDIR /app

RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# apt-get安装后清理apt缓存减小镜像体积

# 修改环境变量确保great_expectation初始化可以正常进行
ENV PATH="/.local/bin:$PATH"
# pyspark的运行需要java环境
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
# --no-cache-dir选项可以避免pip缓存，减小镜像体积

CMD ["/bin/bash", "-c", "cd /app/study_great_expectations && exec /bin/bash"]