from fastapi import FastAPI

from elasticmq.elasticmq_config import init_elasticmq
from exceptions.app_exception import QsmithAppException
from exceptions.exception_handler import app_exception_handler, generic_exception_handler
from sqlite_core.sqllite_config import init_db

init_db()
init_elasticmq()

from brokers.api.broker_api import router as brokers_connection_router
from brokers.api.broker_queues_api import router as brokers_router
from data_sources.api.json_array_data_source_api import router as json_array_router
from database.api.database_api import router as database_router
from elaborations.api.elaborations_api import router as elaborations_router
from json_utils.api.json_utils_api import router as json_utils_router
from logs.api.logs_api import router as logs_router

app = FastAPI()

app.include_router(brokers_router)
app.include_router(brokers_connection_router)
app.include_router(json_array_router)
app.include_router(database_router)
app.include_router(elaborations_router)
app.include_router(json_utils_router)
app.include_router(logs_router)

app.add_exception_handler(QsmithAppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
