import asyncio
import websockets

async def play():
    async with websockets.connect("ws://localhost:8765") as ws:
        async for message in ws:
            print(message)
            move = input("Enter move (e.g., e2e4): ")
            await ws.send(move)

asyncio.run(play())

