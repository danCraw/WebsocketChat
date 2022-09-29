import asyncio
import websockets

from config import HOST, PORT

USERS = set()


async def addUser(websocket):
    USERS.add(websocket)


async def removeUser(websocket):
    USERS.remove(websocket)


async def socket(websocket):
    await addUser(websocket)
    try:
        while True:
            message = await websocket.recv()

            await asyncio.wait([user.send(message) for user in USERS])
    except:
        await removeUser(websocket)


start_server = websockets.serve(socket, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
