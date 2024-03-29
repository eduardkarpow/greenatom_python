from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

stopFlag = 1

app = FastAPI()

app.middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST, GET"],
    allow_headers=["*"]
)

class StartModel(BaseModel):
    startN: int


@app.get("/stop")
async def stop():
    global stopFlag
    stopFlag = 1


@app.post("/start")
async def start(startModel: StartModel):
    global stopFlag
    stopFlag = 0
    os.system("python robot.py " + str(startModel.startN))


if __name__ == '__main__':
    print("Working")

