class Network:
    base_endpoint = '/controller/network'

    def __init__(self):
        # init

    @staticmethod
    def from_raw(object, executor=None):
        network = Network()
        network.executor = executor
        for k, v in object.items():
            setattr(network, k, v)
        return network

    def __repr__(self):
        return f'<Network id={repr(self.id)} name={repr(self.name)}>'