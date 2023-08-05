

__all__ = ('Seed',)


class Seed:

    __slots__ = ('_access', '_parse')

    def __init__(self, access, parse):

        self._access = access

        self._parse = parse

    @property
    def access(self):

        return self._access

    async def get(self, keys, names):

        data = await self._access.get(keys,*names)

        return self._parse(data)

    async def create(self, keys, data):

        await self._access.create(keys, data)

        data = await self._access.get(keys)

        return self._parse(data)

    async def update(self, keys, data):

        await self._access.update(keys, data)

        names = data.keys()

        data = await self._access.get(keys, names)

        return self._parse(data)

    async def delete(self, keys):

        data = await self._access.get(keys)

        await self._access.delete(keys)

        return self._parse(data)
