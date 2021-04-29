import uvicorn
from fastapi import FastAPI

from api import (
    addition,
    current_time,
    users_and_documents,
                )


def configuration():

    app = FastAPI()
    app.include_router(addition.router)
    app.include_router(current_time.router)
    app.include_router(users_and_documents.router)

    return app


app = configuration()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
