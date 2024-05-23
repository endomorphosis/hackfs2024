import ipfs_model_manager as model_manager

class ipfs_agent:
    def __init__(self, resources=None, meta=None):
        self.model_manager = model_manager.model_manager(resources, meta)
        pass


    def __call__(self, input):
        return input
    
if __name__ == '__main__':
    meta = {}
    resources = {}
    ipfs_agent = ipfs_agent(resources, meta)
    print(ipfs_agent("Hello, world!"))