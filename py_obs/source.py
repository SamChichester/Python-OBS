
class Source:
    def __init__(self, client, scene_name, source_name):
        self._client = client
        self.scene_name = scene_name
        self.source_name = source_name
        

    async def translate(self, pixels_x, pixels_y):
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
        current_y = transform["sceneItemTransform"]["positionY"]

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "positionX": current_x + pixels_x,
                    "positionY": current_y + pixels_y
                }
            }
        )


    async def translate_right(self, pixels_x):
        await self.translate(pixels_x, 0)


    async def translate_left(self, pixels_x):
        await self.translate(-pixels_x, 0)

    
    async def translate_up(self, pixels_y):
        await self.translate(0, -pixels_y)


    async def translate_down(self, pixels_y):
        await self.translate(0, pixels_y)
