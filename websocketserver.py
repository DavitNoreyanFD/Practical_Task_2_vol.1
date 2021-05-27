import urllib.error
import pyngrok.exception
import websockets
import asyncio
import moon
import datetime
import logging
from pyngrok import ngrok


logging.basicConfig(level=logging.INFO)


async def content(cur_time):
    obj = moon.Moon(cur_time)
    ob_for = obj.moon_coordinate_result_in_curr_time()
    obj_for_send = f"{ob_for}"
    return obj_for_send


async def handle(ws, path):
    try:
        logging.info(f'{ws.remote_address} -- connect')
        while True:
            curr_time = datetime.datetime.now()
            obj_for_send = await content(curr_time)
            await ws.send(obj_for_send)
            await asyncio.sleep(3)
    except websockets.ConnectionClosedError:
        logging.info(f'{ws.remote_address} -- disconnect')
    except websockets.ConnectionClosedOK:
        logging.info(f'{ws.remote_address} -- disconnect1')


def running_func(ip, prt):
    try:
        ngrok_tunell = ngrok.connect(5000)
        start_server = websockets.serve(handle, ip, prt)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        ngrok.disconnect(ngrok_tunell.public_url)
    except (ConnectionResetError, urllib.error.URLError, pyngrok.exception.PyngrokNgrokURLError):
        pass
    except KeyboardInterrupt:
        logging.info('the server was down')
