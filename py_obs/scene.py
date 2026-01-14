from py_obs.source import Source


class Scene:
    def __init__(self, client, name):
        self._client = client
        self.name = name


    async def switch_to(self):
        await self._client.request(
            "SetCurrentProgramScene",
            {"sceneName": self.name}
        )


    def source(self, name):
        return Source(self._client, self.name, name)