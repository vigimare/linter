FROM astral/uv:python3.12-bookworm-slim

ARG WORKDIR=/home/linter

RUN apt update -y \
    && apt install vim -y \
    && mkdir -p $WORKDIR

COPY pyproject.toml $WORKDIR

WORKDIR $WORKDIR

RUN ["uv", "sync"]

COPY api.py app.py $WORKDIR
COPY linter/ $WORKDIR/linter
COPY xsd/ $WORKDIR/xsd
COPY assets/ $WORKDIR/assets

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["uv", "run", "streamlit", "run", "app.py"]
