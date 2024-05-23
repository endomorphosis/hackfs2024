import ipfs_model_manager as model_manager
import config as config
import orbitdb_kit_lib as orbitdb_kit
class ipfs_agent:
    def __init__(self, resources=None, meta=None):
        self.config = config.config()
        self.model_manager = model_manager.model_manager(resources, meta)
        pass

    def __call__(self, input):
        config = self.config
        models = self.model_manager.list_ipfs_models()
        results = {
            "config": config,
            "models": models
        }
        return results
    
if __name__ == '__main__':
    meta = {}
    resources = {}
    ipfs_agent = ipfs_agent(resources, meta)
    print(ipfs_agent())