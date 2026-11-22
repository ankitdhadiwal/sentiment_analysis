
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PORT=7860
ENV OMP_NUM_THREADS=2
ENV MKL_NUM_THREADS=2

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app

USER appuser

EXPOSE 7860

CMD ["gunicorn", "--workers", "1", "--threads", "2", "--timeout", "180", "--bind", "0.0.0.0:7860", "run:app"]
