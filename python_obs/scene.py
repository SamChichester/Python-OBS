from python_obs.source import Source


class Scene:
    def __init__(self, client, name):
        self._client = client
        self.name = name


    def source(self, name):
        return Source(self._client, self.name, name)