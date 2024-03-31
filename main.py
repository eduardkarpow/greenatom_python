from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os
import sqlite3

CREATE_TABLE_SCRIPT = "CREATE TABLE IF NOT EXISTS logs(" \
                      "_id INTEGER PRIMARY KEY," \
                      "start DATETIME NOT NULL," \
                      "end DATETIME," \
                      "start_index int NOT NULL" \
                      ");"
curId = None
connection = sqlite3.connect("logs.db")
cursor = connection.cursor()
cursor.execute(CREATE_TABLE_SCRIPT)


def insertScript(startIndex: int):
    global curId
    sql = "INSERT INTO logs (start, start_index) VALUES ('{}', {});".format(datetime.now(), startIndex)
    cursor.execute(sql)
    connection.commit()
    getIdx = "SELECT _id FROM logs ORDER BY _id DESC LIMIT 1;"
    res = cursor.execute(getIdx)
    curId = res.fetchone()[0]


def updateScript():
    sql = "UPDATE logs SET end = '{}' WHERE _id = {};".format(datetime.now(), curId)
    cursor.execute(sql)
    connection.commit()


def prepareData(el: list):
    dct = {"id": el[0], "start_datetime": el[1], "end_datetime": el[2], "start_index": el[3]}
    return dct

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
    updateScript()
    stopFlag = 1


@app.post("/start")
async def start(startModel: StartModel):
    global stopFlag
    stopFlag = 0
    insertScript(startModel.startN)
    os.system("start cmd /k python robot.py " + str(startModel.startN))
    return JSONResponse(content=jsonable_encoder({"message": "success"}))


@app.get("/isStopped")
async def isStopped():
    return JSONResponse(content=jsonable_encoder({"stopFlag": stopFlag}))


@app.get("/getLogs")
async def getLogs():
    sql = "SELECT * FROM logs;"
    res = cursor.execute(sql)
    return JSONResponse(content=jsonable_encoder(list(map(prepareData, res.fetchall()))))
if __name__ == '__main__':
    print("Working")

