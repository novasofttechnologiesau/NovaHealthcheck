from collections.abc import Callable

from fastapi import APIRouter

health_router = APIRouter()
_checks: list[tuple[str, Callable[[], object]]] = []


def register_check(name: str, check: Callable[[], object]) -> None:
    _checks.append((name, check))


@health_router.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@health_router.get("/health/ready")
async def ready() -> dict[str, object]:
    import inspect

    states = {}
    for name, check in _checks:
        try:
            result = check()
            result = await result if inspect.isawaitable(result) else result
            states[name] = "ok" if result is not False else "failed"
        except Exception:  # noqa: BLE001 - failed checks must fail readiness closed
            states[name] = "failed"
    return {
        "status": "ok"
        if all(value == "ok" for value in states.values())
        else "unavailable",
        "checks": states,
    }
