import os
import picologging as logging
from pymongo import MongoClient
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME')
MONGODB_DB_COLLECTION_NAME = os.getenv('MONGODB_DB_COLLECTION_NAME')

mdb_collection = None

async def connect_db():
    db_client = MongoClient(MONGODB_URI)
    db_collection = db_client[MONGODB_DB_NAME][MONGODB_DB_COLLECTION_NAME]
    logging.info("Connected to DB.")

    return db_client, db_collection

async def disconnect_db(db_client) -> None:
    await db_client.close()
    logging.info("Disconnected from DB.")

@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    global mdb_collection
    mdb_client = None

    if mdb_collection is None:
        mdb_client = await connect_db(mdb_collection)

    try:
        yield

    finally:
        await disconnect_db(mdb_client)
