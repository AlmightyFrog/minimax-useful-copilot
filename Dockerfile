FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir httpx fastapi uvicorn

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

COPY --chown=appuser:appuser minimax_proxy.py .

USER appuser

EXPOSE 3333

ENV MINIMAX_API_KEY=""

CMD python minimax_proxy.py --host 0.0.0.0
