from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from routes.upload import router
app=FastAPI()
app.include_router(router)