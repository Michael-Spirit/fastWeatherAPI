from importlib import import_module
from typing import Any
from typing import Dict

from fastapi import FastAPI

from config.main import settings


def init_middlewares(app: FastAPI):
    for app_module in settings.MIDDLEWARES:
        params: Dict[str, Any] = {}

        if isinstance(app_module, tuple):
            app_module, params = app_module

        middleware_path, middleware_class = app_module.rsplit('.', 1)

        middleware_module = import_module(middleware_path)

        app.add_middleware(
            getattr(middleware_module, middleware_class),
            **params,
        )
