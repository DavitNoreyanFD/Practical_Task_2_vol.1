import websockets
import asyncio
import os
import moon
import datetime
import logging

logging.basicConfig(level=logging.INFO)


async def content(cur_time):
    obj = moon.Moon(cur_time)
    ob_for = obj.moon_coordinate_result_in_curr_time()
    obj_for_send = f"{ob_for}"
    return obj_for_send


async def handle(ws, path):
    logging.info(f'{ws.remote_address} -- connect')
    while True:
        curr_time = datetime.datetime.now()
        obj_for_send = await content(curr_time)
        await ws.send(obj_for_send)
        await asyncio.sleep(3)


def running_func(ip, prt):
    start_server = websockets.serve(handle, ip, prt)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


ip, prt = ('127.0.0.1', 5000)
try:
    running_func(ip, prt)
except KeyboardInterrupt:
    logging.info('the server was down')
