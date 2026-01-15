"""
clients.py

High-level clients for communicating with OBS Studio.
"""

from python_obs.client import OBSClient
from python_obs.scene import Scene
from python_obs.exceptions import OBSRequestError
from python_obs.sync_utils import SyncProxy

class OBS:
    def __init__(self, host="localhost", port=4455, password=None):
        async_client = OBSAsync(host, port, password)
        self._proxy = SyncProxy(async_client)

    def __getattr__(self, name):
        return getattr(self._proxy, name)


class OBSAsync:
    def __init__(self, host="localhost", port=4455, password=None):
        self._client = OBSClient(host, port, password)


    async def connect(self):
        await self._client.connect()


    def scene(self, name):
        return Scene(self._client, name)
    

    async def set_scene(self, name):
        try:
            await self._client.request(
                "SetCurrentProgramScene",
                {"sceneName": name}
            )
        
        except RuntimeError as e:
            raise OBSRequestError(
                f"Failed to switch to scene '{name}': {e}"
            ) from e
    

    async def create_scene(self, name):
        await self._client.request(
            "CreateScene",
            {"sceneName": name}
        )

    
    async def delete_scene(self, name):
        try:
            await self._client.request(
                "RemoveScene",
                {"sceneName": name}
            )

        except RuntimeError as e:
            raise OBSRequestError(
                f"Failed to delete scene '{name}': {e}"
            ) from e