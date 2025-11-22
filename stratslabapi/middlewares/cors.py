from fastapi.middleware.cors import CORSMiddleware


class CORSMiddleware(CORSMiddleware):
    def is_allowed_origin(self, origin: str) -> bool:
        return True