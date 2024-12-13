import time

import ngrok
import requests


def start() -> None:
    listener = ngrok.forward(addr="localhost:5000", authtoken="1t43yy8gVlVvgdaKvobTQVH4UTS_4upRsHn8mjohW1WnBDVw5",
                             proto="tcp")
    while True:
        try:
            print(listener.url()[5:])
            res = requests.post(f"http://127.0.0.1:5000/ngrok{listener.url()[5:]}")
            print(res.status_code)
            if res.status_code == 200:
                break
        except Exception as err:
            print(err, end="\n");
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    start()