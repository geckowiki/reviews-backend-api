from fastapi import FastAPI

from adapters.http.api import api_router
from adapters.persistence.orm import map_to_domain


map_to_domain()
app = FastAPI()
app.include_router(api_router, prefix="/api/v1")