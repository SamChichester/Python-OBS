
class Source:
    def __init__(self, client, scene_name, source_name):
        self._client = client
        self.scene_name = scene_name
        self.source_name = source_name
        

    # Translation
    async def translate(self, pixels_x, pixels_y):
        item_id = await self._get_scene_item_id()
        transform = await self._get_scene_item_transform(item_id)
        current_x = transform["positionX"]
        current_y = transform["positionY"]

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


    async def set_position(self, position_x, position_y):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "positionX": position_x,
                    "positionY": position_y
                }
            }
        )

    
    # Rotation
    async def rotate(self, degrees):
        item_id = await self._get_scene_item_id()
        transform = await self._get_scene_item_transform(item_id)
        current_rotation = transform["rotation"]

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "rotation": (current_rotation + degrees) % 360,
                }
            }
        )


    async def rotate_clockwise(self, degrees):
        await self.rotate(degrees)


    async def rotate_counterclockwise(self, degrees):
        await self.rotate(-degrees)


    async def set_rotation(self, orientation):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "rotation": orientation % 360,
                }
            }
        )


    # Scale
    async def scale(self, factor_X, factor_Y):
        item_id = await self._get_scene_item_id()
        transform = await self._get_scene_item_transform(item_id)
        current_scale_X = transform["scaleX"]
        current_scale_Y = transform["scaleY"]

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "scaleX": current_scale_X * factor_X,
                    "scaleY": current_scale_Y * factor_Y,
                }
            }
        )

    
    async def scale_X(self, factor_X):
        await self.scale(factor_X, 1)


    async def scale_Y(self, factor_Y):
        await self.scale(1, factor_Y)

    
    async def set_scale(self, scale_X, scale_Y):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "scaleX": scale_X,
                    "scaleY": scale_Y,
                }
            }
        )

    
    async def set_scale_X(self, scale_X):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "scaleX": scale_X,
                }
            }
        )


    async def set_scale_Y(self, scale_Y):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "scaleY": scale_Y,
                }
            }
        )

    
    # Crop
    async def crop(self, bottom, left, right, top):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "cropBottom": bottom,
                    "cropLeft": left,
                    "cropRight": right,
                    "cropTop": top,
                }
            }
        )


    async def crop_bottom(self, pixels):
        await self.crop(pixels, 0, 0, 0)


    async def crop_left(self, pixels):
        await self.crop(0, pixels, 0, 0)


    async def crop_right(self, pixels):
        await self.crop(0, 0, pixels, 0)


    async def crop_top(self, pixels):
        await self.crop(0, 0, 0, pixels)


    # Visibility
    async def hide(self):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemEnabled",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemEnabled": False
            }
        )

    async def show(self):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemEnabled",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemEnabled": True
            }
        )

    async def toggle_visiblity(self):
        item_id = await self._get_scene_item_id()
        is_enabled = await self._get_scene_item_enabled(item_id)

        await self._client.request(
            "SetSceneItemEnabled",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemEnabled": not is_enabled
            }
        )


    # Locking
    async def lock(self):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemLocked",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemLocked": True
            }
        )

    async def unlock(self):
        item_id = await self._get_scene_item_id()

        await self._client.request(
            "SetSceneItemLocked",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemLocked": False
            }
        )

    async def toggle_lock(self):
        item_id = await self._get_scene_item_id()
        is_locked = await self._get_scene_item_locked(item_id)

        await self._client.request(
            "SetSceneItemLocked",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id,
                "sceneItemLocked": not is_locked
            }
        )


    # Helper functions:
    async def _get_scene_item_id(self):
        data = await self._client.request(
            "GetSceneItemId",
            {
                "sceneName": self.scene_name,
                "sourceName": self.source_name
            }
        )
        return data["sceneItemId"]
    

    async def _get_scene_item_enabled(self, item_id):
        data = await self._client.request(
            "GetSceneItemEnabled",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id
            }
        )
        return data["sceneItemEnabled"]
    

    async def _get_scene_item_locked(self, item_id):
        data = await self._client.request(
            "GetSceneItemLocked",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id
            }
        )
        return data["sceneItemLocked"]
    

    async def _get_scene_item_transform(self, item_id):
        transform = await self._client.request(
            "GetSceneItemTransform",
            {
                "sceneName": self.scene_name,
                "sceneItemId": item_id
            }
        )
        return transform["sceneItemTransform"]
