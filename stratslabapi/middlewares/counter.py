from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.requests import Request



from stratslabapi.repositories.models import RequestCounterModel


def _get_url(request: Request) -> str:
    return request.url.__str__().split("?")[0][:64]


class APIRequestCounter(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path.startswith("/api"):
            await RequestCounterModel.count_url(_get_url(request))

        return await call_next(request)
