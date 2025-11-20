from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from alembic_runner import run_alembic_migrations
from elasticmq.elasticmq_config import init_elasticmq
from exceptions.app_exception import QsmithAppException
from exceptions.exception_handler import app_exception_handler, generic_exception_handler

load_dotenv()
init_elasticmq()

from brokers.api.broker_api import router as brokers_connection_router
from brokers.api.broker_queues_api import router as brokers_router
from data_sources.api.json_array_data_source_api import router as json_array_router
from database.api.database_api import router as database_router
from elaborations.api.scenarios_api import router as scenarios_router
from elaborations.api.steps_api import router as steps_router
from elaborations.api.operations_api import router as operations_router
from json_utils.api.json_utils_api import router as json_utils_router
from logs.api.logs_api import router as logs_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting Alembic migrations...")
    try:
        run_alembic_migrations()
    except Exception as e:
        print(f"Error during Alembic migrations: {str(e)}")
        raise e
    print("Alembic migrations completed.")

    try:
        yield
    finally:
        print("Shutting down application...")


app = FastAPI(lifespan=lifespan)

app.include_router(brokers_router)
app.include_router(brokers_connection_router)
app.include_router(json_array_router)
app.include_router(database_router)
app.include_router(scenarios_router)
app.include_router(operations_router)
app.include_router(steps_router)
app.include_router(json_utils_router)
app.include_router(logs_router)

app.add_exception_handler(QsmithAppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
