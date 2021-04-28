import uvicorn
from fastapi import FastAPI

from app.addition.routers import addition_router
from app.current_time.routers import current_time_router

app = FastAPI()


def configuration():
    app.include_router(addition_router)
    app.include_router(current_time_router)


configuration()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
