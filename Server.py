import asyncio
import websockets
import pyautogui
import socket
import qrcode

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

PORT = 8765


# detect local IP automatically
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


async def handler(websocket):

    print("📱 Phone connected")

    try:
        async for message in websocket:

            # ignore ping
            if message == "ping":
                continue

            # ensure correct format
            if ":" not in message:
                continue

            command, key = message.split(":", 1)

            if command == "down":
                pyautogui.keyDown(key)

            elif command == "up":
                pyautogui.keyUp(key)

    except Exception as e:
        print("⚠ Connection error:", e)

    finally:
        print("📴 Phone disconnected")


async def main():

    ip = get_local_ip()
    url = f"ws://{ip}:{PORT}"

    print("🚀 WebSocket controller server running")
    print("Listening on port", PORT)
    print("Controller URL:", url)

    # generate QR
    qr = qrcode.make(url)
    qr.show()

    print("📷 Scan the QR code with the phone app")

    async with websockets.serve(
        handler,
        "0.0.0.0",
        PORT,
        ping_interval=20,
        ping_timeout=30,
    ):
        await asyncio.Future()


asyncio.run(main())