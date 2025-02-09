FROM ghcr.io/astral-sh/uv:python3.12-alpine

COPY . /valentine
WORKDIR /valentine
RUN uv sync --frozen
CMD ["uv", "run", "src/main.py"]
