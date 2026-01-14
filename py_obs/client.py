"""
client.py

Low-level WebSocket client for communicating with OBS Studio via the
OBS WebSocket v5 protocol.
"""

import json
import uuid
import websockets


class OBSClient:
    def __init__(self, host="localhost", port=4455, password=None):
        self.url = f"ws://{host}:{port}"
        self.password = password
        self.ws = None


    async def _identify(self) -> None:
        hello = json.loads(await self.ws.recv())

        if hello["op"] !=  0:
            raise RuntimeError("Invalid OBS hello.")

        identify = {
            "op": 1,
            "d": {
                "rpcVersion": 1,
            }
        }

        await self.ws.send(json.dumps(identify))
        await self.ws.recv()


    async def connect(self):
        self.ws = await websockets.connect(self.url)
        await self._identify()
        print("CONNECTED SUCCESSFULLY!")


    async def request(self, request_type, request_data=None):
        request_id = str(uuid.uuid4())

        payload = {
            "op": 6,
            "d": {
                "requestType": request_type,
                "requestId": request_id,
                "requestData": request_data or {}
            }
        }

        await self.ws.send(json.dumps(payload))

        while True:
            msg = json.loads(await self.ws.recv())
            if msg["op"] == 7 or msg["d"]["requestId"] == request_id:
                if not msg["d"]["requestStatus"]["result"]:
                    raise RuntimeError(msg["d"]["requestStatus"]["comment"])
                return msg["d"].get("responseData")
