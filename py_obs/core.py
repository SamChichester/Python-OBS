"""
core.py

High-level client for communicating with OBS Studio.
"""

from .client import OBSClient


class OBS:
    def __init__(self, host="localhost", port=4455, password=None):
        self._client = OBSClient(host, port, password)


    async def connect(self):
        self._client.connect()


    def scene(self):
        raise NotImplementedError("Will be implemented later.")
