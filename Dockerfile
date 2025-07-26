FROM bitnami/spark:3.3.0

WORKDIR /app

ENV PATH="/.local/bin:$PATH"
COPY utils/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY utils/init_gx.sh /app/init_gx.sh
USER root
RUN apt-get update && apt-get install -y expect
RUN chmod +x /app/init_gx.sh && expect /app/init_gx.sh

CMD ["/bin/bash", "-c", "cd /app/volume && exec /bin/bash"]