"""

"""
import urllib.error
import pyngrok.exception
import websockets
import asyncio
import moon
import logging
from pyngrok import ngrok
import datetime as dt


logging.basicConfig(level=logging.INFO)


async def content(cur_time):
    """

    :param cur_time:
    :return:
    """
    obj = moon.Moon(cur_time)
    ob_for = obj.moon_ra_dec_calc()
    obj_for_send = f"{ob_for}"
    return obj_for_send


async def handle(ws, path):
    """

    :param ws:
    :param path:
    :return:
    """
    try:
        logging.info(f'{ws.remote_address} -- connect')
        while True:
            curr_time = dt.datetime.now()
            obj_for_send = await content(curr_time)
            await ws.send(obj_for_send)
            await asyncio.sleep(3)
    except websockets.ConnectionClosedError:
        logging.info(f'{ws.remote_address} -- disconnect')
    except websockets.ConnectionClosedOK:
        logging.info(f'{ws.remote_address} -- disconnect1')


def running_func(ip, prt):
    """

    :param ip:
    :param prt:
    :return:
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
