import peewee


__all__ = ('Handle',)


class Handle:

    __slots__ = ('_seed', '_authorize', '_error')

    def __init__(self, seed, authorize, error):

        self._seed = seed

        self._authorize = authorize

        self._error = error

    @property
    def seed(self):

        return self._seed

    async def _execute(self, action, request, accept):

        self._authorize(request)

        try:

            data = await request.json()

        except:

            raise self._error('invalid data')

        if not len(data) == len(accept):

            raise self._error('invalid data length')

        values = []

        for (data, cls) in zip(data, accept):

            if not isinstance(data, cls):

                # IDEA: better schema checking

                raise self._error('invalid data type')

            values.append(data)

        try:

            data = await action(*values)

        except peewee.DatabaseError as error:

            raise self._error('database fail', str(error))

        return data

    def get(self, request):

        accept = (list, list) # [keys, names]

        return self._execute(self._seed.get, request, accept)

    def create(self, request):

        accept = (list, dict) # [keys, data]

        return self._execute(self._seed.create, request, accept)

    def update(self, request):

        accept = (list, dict) # [keys, data]

        return self._execute(self._seed.update, request, accept)

    def delete(self, request):

        accept = (list,) # [keys]

        return self._execute(self._seed.delete, request, accept)
