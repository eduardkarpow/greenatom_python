import time
import argparse


def work(start: int):
    t = time.time()
    n = start
    while True and n < 20:
        if time.time() - t >= 1.0:
            t = time.time()
            print(n)
            n += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Задание стартового значния")
    parser.add_argument("start", help="стартовое знаачение")
    args = parser.parse_args()
    work(int(args.start))

