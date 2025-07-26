FROM bitnami/spark:3.3.0

WORKDIR /app

ENV PATH="/.local/bin:$PATH"
COPY utils/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


COPY utils/init_gx.sh /app/init_gx.sh
COPY volume/auto_testing.sh /app/auto_testing.sh

USER root
RUN apt-get update && \
    apt-get install -y expect dos2unix && \
    dos2unix /app/auto_testing.sh && \
    chmod +x /app/init_gx.sh /app/auto_testing.sh

CMD ["/bin/bash", "-c", "\
    expect /app/init_gx.sh && \
    /app/auto_testing.sh && \
    cd /app/volume && \
    exec /bin/bash"]