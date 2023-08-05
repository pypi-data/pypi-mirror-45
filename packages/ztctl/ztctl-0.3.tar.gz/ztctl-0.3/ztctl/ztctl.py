import aiohttp

from .query import BaseQuery


class Executor:
    def __init__(self, secret, controller_address):
        self.secret = secret
        self.controller_address = controller_address

    def construct_session(self):
        return aiohttp.ClientSession(headers={'X-ZT1-Auth': self.secret})


class ZTCTL:
    def __init__(self, secret, base_url, controller_address):
        self.controller_address = controller_address
        self.secret = secret
        self.base_url = base_url
        self.executor = Executor(secret, controller_address)
        self.query = BaseQuery(base_url, self.executor)

    @staticmethod
    async def create(secret=None, base_url='http://localhost:9993'):
        if secret is None:
            raise Exception('Secret missing')
        async with aiohttp.ClientSession(headers={'X-ZT1-Auth': secret}) as s:
            response = await s.get(f'{base_url}/status')
            data = await response.json()
            return ZTCTL(secret, f'{base_url}/controller', data['address'])


if __name__ == '__main__':
    import asyncio

    async def test():
        ztctl = await ZTCTL.create('SECRET')
        print(await ztctl.query.networks())
        # print(await ztctl.query.create_network('david'))
        # print(await ztctl.query.delete_network('90b65c38f7671519'))
        # for network_id in await ztctl.query.networks():
        #     network = await ztctl.query.network(network_id).get()
        #     print(network_id, network['name'])
        # print(await ztctl.query.network('90b65c38f76d4f44').members())
        # print(await ztctl.query.network('90b65c38f76d4f44').member('074bb9eb6f').authorize())
        # print(await ztctl.query.network('90b65c38f7334bfc').member('90b65c38f7').get())
        # print(await ztctl.query.network('90b65c38f7334bfc').member('90b65c38f7').authorize())
        # print(await ztctl.query.network('90b65c38f7334bfc').member('90b65c38f7').deauthorize())
    network = asyncio.run(test())
