# Improved Reports API package
from fastapi import FastAPI

app = FastAPI(title="Improved Reports API")

from . import main  # noqa: E402,F401
