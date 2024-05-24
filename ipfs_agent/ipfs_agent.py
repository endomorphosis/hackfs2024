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
        self.baseConfig = self.config.baseConfig
        for key, value in self.baseConfig.items():
            meta[key] = value
        self.orbitdb_kit = orbitdb_kit.orbitdb_kit(resources, meta)
        #self.model_manager = ipfs_model_manager.ipfs_model_manager(resources, meta)
        pass

    def __call__(self):
        config = self.config
        #models = self.model_manager.list_ipfs_models()
        orbitdb = self.orbitdb_kit.stop_orbitdb()
        orbitdb = self.orbitdb_kit.start_orbitdb()
        #connect = self.orbitdb_kit.connect_orbitdb()
        #print("connect")
        #print(connect)
        insert_key = { "test": "test document" }
        insert = self.orbitdb_kit.insert_orbitdb(insert_key)
        print("insert")
        print(insert)
        update_key = { "test": "test document @ update" }
        update = self.orbitdb_kit.update_orbitdb(update_key)
        print("update")
        print(update)
        select_key = "test"
        select = self.orbitdb_kit.select_orbitdb(select_key)
        print("select")
        print(select)
        delete_key = "test"
        delete = self.orbitdb_kit.delete_orbitdb(delete_key)
        print("delete")
        print(delete)
        orbitdb = self.orbitdb_kit.stop_orbitdb()
        results = {
            "config": config,
            "orbitdb": orbitdb,
            "connect": connect,
            "insert": insert,
            "update": update,
            "select": select,
            "delete": delete
        }
        return results
    
if __name__ == '__main__':
    meta = {}
    resources = {}
    ipfs_agent = ipfs_agent(resources, meta)
    print(ipfs_agent())