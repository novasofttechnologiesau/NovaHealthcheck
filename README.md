# NovaHealthcheck

Tiny ASGI health endpoints for Python services. Import `health_router` and include it in a FastAPI application to expose `/health/live` and `/health/ready`. Readiness checks are caller-supplied async or sync functions. No external service dependencies.
