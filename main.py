from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os

stopFlag = 1

app = FastAPI()

app.middleware(
    CORSMiddleware
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
    os.system("start cmd /k python robot.py " + str(startModel.startN))
    return JSONResponse(content=jsonable_encoder({"message": "success"}))

@app.get("/isStopped")
async def isStopped():
    return JSONResponse(content=jsonable_encoder({"stopFlag": stopFlag}))

if __name__ == '__main__':
    print("Working")

