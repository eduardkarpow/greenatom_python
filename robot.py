import time
import argparse
import requests


BASE_URL = "http://localhost:8000"

def work(start: int):
    t = time.time()
    n = start
    while True:
        if time.time() - t >= 1.0:
            t = time.time()

            r = requests.get(BASE_URL+"/isStopped", headers={'Accept': 'application/json'}).json()
            if r['stopFlag'] == 1:
                return
            print(n)
            n += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Задание стартового значния")
    parser.add_argument("start", help="стартовое знаачение")
    args = parser.parse_args()
    work(int(args.start))

