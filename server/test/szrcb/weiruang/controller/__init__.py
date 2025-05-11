from .embedding_controller import *
from .model_controller import *
from .reranker_controller import *
from fastapi import APIRouter
all_api=APIRouter(prefix="/api")
all_api.include_router(model_app)
all_api.include_router(embedding_app)
all_api.include_router(reranker_app)