import ipfs_model_manager as ipfs_model_manager
import config as config
import orbitdb_kit_lib as orbitdb_kit

class ipfs_agent:
    def __init__(self, resources=None, meta=None):
        if meta is None:
            meta = {}
            meta['config'] = 'config/config.toml'
        else:
            if 'config' not in meta:
                meta['config'] = 'config/config.toml'
            else:
                meta['config'] = meta['config']
        if resources is None:
            resources = {}

        self.config = config.config({}, meta=meta)
        self.config = self.config.load_config()

        self.model_manager = ipfs_model_manager.ipfs_model_manager(resources, meta)
        self.orbitdb_kit = orbitdb_kit.orbitdb_kit(resources, meta)
        pass

    def __call__(self, input):
        config = self.config
        models = self.model_manager.list_ipfs_models()
        orbitdb = self.orbitdb_kit.start_orbitdb()
        results = {
            "config": config,
            "models": models,
            "orbitdb": orbitdb
        }
        return results
    
if __name__ == '__main__':
    meta = {}
    resources = {}
    ipfs_agent = ipfs_agent(resources, meta)
    print(ipfs_agent())