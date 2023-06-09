from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.exceptions.exceptions import JSONException
from .database import tables
from .database.database import engine, drop_table, get_db, SessionLocal
from .config.config import settings
from .utils.authentication import Authenticator

tables.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

origins = [
    '*',
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(JSONException)
async def unicorn_exception_handler(request: Request, exc: JSONException):
    return JSONResponse(
        status_code=exc.code,
        content=exc.data,
    )

app.include_router(api_router)


@app.on_event('shutdown')
async def on_app_shutdown():
    # for tbl in reversed(tables.Base.metadata.sorted_tables):
    #     drop_table(f"{tbl}")
    pass

@app.on_event('startup')
async def on_app_startup():
    # admin_user = tables.User(username='admin', 
    #                          email='ark.nameless.zero@gmail.com', 
    #                          password=Authenticator.hash_password('admin'),
    #                          access=['admin', 'employee']
    #                         )
    # db = SessionLocal()
    # db.add(admin_user)
    # db.commit()
    # db.refresh(admin_user)
    # print(admin_user)
    pass