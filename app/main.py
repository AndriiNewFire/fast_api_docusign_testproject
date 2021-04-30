import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    addition,
    current_time,
    users_and_documents,
                )


def configuration():

    app = FastAPI()
    app.add_middleware(
                        CORSMiddleware,
                        allow_origins=["*"],
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"],
                        )
    app.include_router(addition.router)
    app.include_router(current_time.router)
    app.include_router(users_and_documents.router)

    return app


app = configuration()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
