# app/utils/metrics.py

from fastapi import Request
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency in seconds",
    ["path"]
)


def setup_request_metrics(app):
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        import time
        start = time.time()

        response = await call_next(request)

        duration = time.time() - start

        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status_code=str(response.status_code)
        ).inc()

        REQUEST_LATENCY.labels(
            path=request.url.path
        ).observe(duration)

        return response
