
auth_key = ""
room_address = ""
msg = "hello there"

import asyncio
import websockets
import json

websocket_url = "wss://prod-api.kosetto.com/?authorization=" + auth_key


async def ping_server(websocket):
    while True:
        try:
            await websocket.send(json.dumps({"action": "ping"}))
            await asyncio.sleep(2)  # Send a ping every 2 seconds
        except websockets.exceptions.ConnectionClosed:
            print("Connection to the WebSocket server closed.")
            break


async def websocket_listener():
   
   while True:
        try: 
            async with websockets.connect(websocket_url) as websocket:
                print(f"Connected to {websocket_url}")
                
                asyncio.create_task(ping_server(websocket))

                while True:
                    message = await websocket.recv()
                    print(message)
                    try: 
                        json_object = json.loads(message)

                        if json_object["type"] == "receivedMessage" and json_object["chatRoomId"].upper() == room_address.upper():
                            print("received new message in current room")
                            # make sure it does not reply to the owner
                            if json_object["sendingUserId"].upper() != room_address.upper():
                                print("Not by owner")
                                try:
                                    msg_to_send = {
                                        "action": "sendMessage",
                                        "text": msg,
                                        "imagePaths": [],
                                        "chatRoomId": json_object["chatRoomId"],
                                        "clientMessageId": "87e8a533935",
                                        "replyingToMessageId": json_object["messageId"]
                                    }

                                    await websocket.send(json.dumps(msg_to_send))
                                    print(f"Sent response: {msg_to_send}")
                                except:
                                    print("error when sending")
                    except:
                        print("binary")

        except websockets.exceptions.ConnectionClosed:
            print("Connection to the WebSocket server closed.")
            await asyncio.sleep(2)


def run():

    asyncio.get_event_loop().run_until_complete(websocket_listener())


if __name__ == "__main__":
    run()