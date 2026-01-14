"""
core.py

High-level client for communicating with OBS Studio.
"""

from py_obs.client import OBSClient
from py_obs.scene import Scene


class OBS:
    def __init__(self, host="localhost", port=4455, password=None):
        self._client = OBSClient(host, port, password)


    async def connect(self):
        await self._client.connect()


    def scene(self, name):
        return Scene(self._client, name)