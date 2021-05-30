"""
weboketserver module is the logic of the server for responding to requests, 3 functions are written here content,
handle and running_func
"""
import datetime
import urllib.error
import pyngrok.exception
import websockets
import asyncio
import moon
import logging
from pyngrok import ngrok
import datetime as dt


logging.basicConfig(level=logging.INFO)


async def content(cur_time: datetime.datetime) -> str:
    """
    it is an asynchronous function designed to process the content of the request response
    """
    obj = moon.Moon(cur_time)
    obj_for_send = obj.moon_ra_dec_calc()

    return obj_for_send


async def handle(ws: websockets.WebSocketServerProtocol, path) -> None:
    """
    this is an asynchronous function for processing a request that returns content on a request
    response periodically every 10 seconds
    """
    try:
        logging.info(f'{ws.remote_address} -- connect')
        while True:
            curr_time = dt.datetime.now()
            obj_for_send = await content(curr_time)
            await ws.send(obj_for_send)
            await asyncio.sleep(10)
    except websockets.ConnectionClosedError:
        logging.info(f'{ws.remote_address} -- disconnect')
    except websockets.ConnectionClosedOK:
        logging.info(f'{ws.remote_address} -- disconnect1')


def running_func(ip: str, prt: int) -> None:
    """
    this is a function for starting the server, during startup the function automatically
    makes the localhost public using pyngrok
    """
    try:
        ngrok_tunnel = ngrok.connect(prt)
        start_server = websockets.serve(handle, ip, prt)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        ngrok.disconnect(ngrok_tunnel.public_url)
    except (ConnectionResetError, urllib.error.URLError, pyngrok.exception.PyngrokNgrokURLError):
        pass
    except KeyboardInterrupt:
        logging.info('the server was down')
