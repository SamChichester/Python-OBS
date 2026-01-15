"""
client.py

Low-level WebSocket client for communicating with OBS Studio via the
OBS WebSocket v5 protocol.
"""

import base64
import hashlib
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

        identify_data = {"rpcVersion": 1}

        auth = hello["d"].get("authentication")
        if auth:
            if not self.password:
                raise RuntimeError("OBS requires authentication but no password was provided.")

            challenge = auth["challenge"]
            salt = auth["salt"]

            secret = base64.b64encode(
                hashlib.sha256((self.password + salt).encode()).digest()
            ).decode()

            auth_response = base64.b64encode(
                hashlib.sha256((secret + challenge).encode()).digest()
            ).decode()

            identify_data["authentication"] = auth_response

        identify = {
            "op": 1,
            "d": identify_data
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
            if msg["op"] == 7 and msg["d"]["requestId"] == request_id:
                status = msg["d"]["requestStatus"]
                if not status["result"]:
                    raise RuntimeError(status["comment"])
                return msg["d"].get("responseData", {})
