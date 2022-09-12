from enum import Enum

from fastapi import Response, HTTPException, status

from domain.services.use_cases import Result
from domain.services.errors import VideoclipNotFound


class HttpMethod(Enum):
    GET = 1
    POST = 2

def build_response(result: Result, method: HttpMethod) -> Response:
    response = Response()

    if isinstance(result, VideoclipNotFound):
        raise HTTPException(status_code=404, detail=f"Videoclip {result.videoclip_id} not found")
    
    if method is HttpMethod.GET:
        response.status_code = status.HTTP_200_OK
    elif method is HttpMethod.POST:
        response.status_code = status.HTTP_201_CREATED

    return response
