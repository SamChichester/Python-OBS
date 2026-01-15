from python_obs.source import Source
from python_obs.exceptions import OBSRequestError


class Scene:
    def __init__(self, client, name):
        self._client = client
        self.name = name


    def source(self, name):
        return Source(self._client, self.name, name)
    

    async def create_source(self, name, kind, settings=None, enabled=True):
        try:
            return await self._client.request(
                "CreateInput",
                {
                    "sceneName": self.name,
                    "inputName": name,
                    "inputKind": kind,
                    "inputSettings": settings or {},
                    "sceneItemEnabled": enabled
                }
            )
        
        except RuntimeError as e:
            raise OBSRequestError(
                f"Failed to create source '{name}' of kind '{kind}': {e}"
            ) from e


    async def delete_source(self, source_name):
        try:
            item_id = await self._get_scene_item_id(source_name)

            await self._client.request(
                "RemoveSceneItem",
                {
                    "sceneName": self.name,
                    "sceneItemId": item_id
                }
            )

        except RuntimeError as e:
            raise OBSRequestError(
                f"Failed to delete source '{source_name}' from scene '{self.name}': {e}"
            ) from e
        

    # Helper Functions
    async def _get_scene_item_id(self, name):
        try:
            data = await self._client.request(
                "GetSceneItemId",
                {
                    "sceneName": self.name,
                    "sourceName": name
                }
            )
            return data["sceneItemId"]
        
        except RuntimeError as e:
            raise OBSRequestError(
                f"Failed to find source '{name}' in scene '{self.name}': {e}"
            ) from e
