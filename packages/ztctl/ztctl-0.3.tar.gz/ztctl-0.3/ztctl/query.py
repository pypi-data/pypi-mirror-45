class ComposableQuery:
    def __init__(self, path, executor=None):
        self.path = path if type(path) is list else [path]
        self.executor = executor

    @property
    def full_path(self):
        return '/'.join(self.path)

    async def get(self):
        async with self.executor.construct_session() as session:
            response = await session.get(self.full_path)
            return await response.json()

    async def post(self, data={}):
        async with self.executor.construct_session() as session:
            response = await session.post(self.full_path, json=data)
            return await response.json()

    async def delete(self):
        async with self.executor.construct_session() as session:
            response = await session.delete(self.full_path)
            return await response.json()

    def join(self, path):
        if type(path) is list:
            return ComposableQuery(self.path + path, executor=self.executor)
        return ComposableQuery(self.path + [path], executor=self.executor)


class MemberQuery:
    def __init__(self, parentQuery, id):
        self.query = parentQuery.join(['member', id])

    async def get(self):
        return await self.query.get()

    async def authorize(self):
        return await self.query.post({'authorized': True})

    async def deauthorize(self):
        return await self.query.post({'authorized': False})


class NetworkQuery:
    def __init__(self, parentQuery, id):
        self.id = id
        self.query = parentQuery.join(['network', id])

    def member(self, id):
        return MemberQuery(self.query, id)

    def members(self):
        query = self.query.join('member')
        return query.get()

    async def get(self):
        return await self.query.get()

    async def delete(self):
        return await self.query.delete()


class BaseQuery:
    def __init__(self, base_url, executor):
        self.query = ComposableQuery(base_url, executor=executor)

    def network(self, id):
        return NetworkQuery(self.query, id)

    async def networks(self):
        query = self.query.join('network')
        return await query.get()
    
    async def create_network(self, name=None):
        query = self.query.join(
            ['network', f'{self.query.executor.controller_address}______'])
        return await query.post({'name': name})
    
    async def delete_network(self, id):
        query = self.query.join(['network', id])
        return await query.delete()
