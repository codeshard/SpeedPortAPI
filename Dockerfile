FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
LABEL org.opencontainers.image.source="https://github.com/codeshard/SpeedPortAPI"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /speedport
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /speedport
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm

RUN groupadd -g 10001 speedport && \
    useradd -u 10000 -g speedport speedport

USER speedport:speedport

COPY --from=builder --chown=speedport:speedport /speedport /speedport

ENV PATH="/speedport/.venv/bin:$PATH"

CMD ["fastapi", "prod", "--host", "0.0.0.0", "/speedport/app"]
