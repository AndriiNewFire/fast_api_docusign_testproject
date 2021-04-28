import uvicorn
from fastapi import FastAPI
import os

from api import (
    addition,
    current_time,
                )


def configuration():

    app = FastAPI()
    app.include_router(addition.router)
    app.include_router(current_time.router)

    return app


app = configuration()

if __name__ == "__main__":
    print(os.environ)
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
