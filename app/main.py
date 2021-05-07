import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.users_management import UI_user_endpoints, users_api
from api.documents import documents

from api import (
    addition,
    current_time,
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
    app.include_router(UI_user_endpoints.router)
    app.include_router(users_api.router)
    app.include_router(documents.router)

    return app


app = configuration()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
