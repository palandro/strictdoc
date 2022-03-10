from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


def create_app(_):
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def get_root():
        return {"Hello": "World"}

    return app


def strictdoc_production_app():
    # database = RealDatabase()
    # database.use_real_database()
    return create_app(None)
