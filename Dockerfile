FROM nvidia/cuda:12.0.1-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 \
    pip

COPY requirements.txt /

RUN pip install --upgrade pip && \
    pip install --root-user-action=ignore -r /requirements.txt

COPY flan_t5_server.py /

ARG MODEL_NAME=google/flan-t5-small
ENV MODEL_NAME=$MODEL_NAME
RUN python3 /flan_t5_server.py "$MODEL_NAME" init

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["python3 /flan_t5_server.py ${MODEL_NAME} run"]
