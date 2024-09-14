from fastapi import FastAPI
from .routers import auth, tasks
from .database import database, metadata, engine, connect_to_database, close_database_connection
from .models import task, user
from .utils import init_roles

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Connect to the database
    await database.connect()
    connect_to_database()
    
    # Create all tables
    metadata.create_all(engine)
    
    session = engine.connect()
    
    await init_roles(session)

@app.on_event("shutdown")
async def shutdown():
    # metadata.drop_all(bind=engine)

    await database.disconnect()
    await close_database_connection()

app.include_router(auth.router)
app.include_router(tasks.router)
