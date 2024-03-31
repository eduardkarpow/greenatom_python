import time
import argparse
import requests
import asyncio
import threading

BASE_URL = "http://localhost:8000"
stopFlag = 0

def req():
    global stopFlag
    r = requests.get(BASE_URL + "/isStopped", headers={'Accept': 'application/json'}).json()
    stopFlag = r["stopFlag"]
    return


async def work(start: int):
    t = time.time()
    n = start
    while True:
        if time.time() - t >= 1.0:
            t = time.time()

            threading.Thread(target=req, args=()).start()
            if stopFlag:
                return
            print(n)
            n += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Задание стартового значния")
    parser.add_argument("start", help="стартовое знаачение")
    args = parser.parse_args()
    asyncio.run(work(int(args.start)))


