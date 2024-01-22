from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime
from db import create_tables
from public.users import users_router
import uvicorn

app = FastAPI()

app.include_router(users_router)

@app.on_event("startup")
def on_startup():
    open("files/log_p.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    create_tables()


@app.on_event("shutdown")
def shutdown():
    open("files/log_p.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

@app.get('/')
def main():
    return FileResponse("files/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)