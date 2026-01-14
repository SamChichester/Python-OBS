
class Source:
    def __init__(self, client, scene_name, source_name):
        self._client = client
        self.scene_name = scene_name
        self.source_name = source_name


    async def translate_right(self, pixels):
        data = await self._client.request(
            "GetSceneItemId",
            {
                "sceneName": self.scene_name,
                "sourceName": self.source_name
            }
        )
        item_id = data["sceneItemId"]

        transform = await self._client.request(
            "GetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id
            }
        )
        current_x = transform["sceneItemTransform"]["positionX"]

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "positionX": current_x + pixels
                }
            }
        )
