import os
import sys
import subprocess as process 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import websockets as ws 
from config import config

class orbitdb_kit():
    def __init__(self,  resources=None, meta=None):
        self.resources = resources
        self.meta = meta
        self.config = config
        self.orbitdb_args = {}
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        if self.meta is None:
            self.meta = {}
            self.orbitdb_args['ipaddress'] = None
            self.orbitdb_args['orbitdbAddress'] = None
            self.orbitdb_args['index'] = None
            self.orbitdb_args['chunkSize'] = None
            self.orbitdb_args['swarmName'] = None

        else:
            if 'ipaddress' in self.meta:
                self.orbitdb_args['ipaddress'] = self.meta['ipaddress']
            else:
                self.orbitdb_args['ipaddress'] = None
            
            if 'orbitdbAddress' in self.meta:
                self.orbitdb_args['orbitdbAddress'] = self.meta['orbitdbAddress']
            else:
                self.orbitdb_args['orbitdbAddress'] = None
            
            if 'index' in self.meta:
                self.orbitdb_args['index'] = self.meta['index']
            else:
                self.orbitdb_args['index'] = None
            
            if 'chunkSize' in self.meta:
                self.orbitdb_args['chunkSize'] = self.meta['chunkSize']
            else:
                self.orbitdb_args['chunkSize'] = None

            if 'swarmName' in self.meta:
                self.orbitdb_args['swarmName'] = self.meta['swarmName']
            else:
                self.orbitdb_args['swarmName'] = None

            if 'port' in self.meta:
                self.orbitdb_args['port'] = self.meta['port']
            else:
                self.orbitdb_args['port'] = 50001
        
        if self.orbitdb_args['ipaddress'] is None:
            self.orbitdb_args['ipaddress'] = '127.0.0.1'
        if self.orbitdb_args['orbitdbAddress'] is None:
            self.orbitdb_args['orbitdbAddress'] = None
        if self.orbitdb_args['index'] is None:
            self.orbitdb_args['index'] = 1
        if self.orbitdb_args['chunkSize'] is None:
            self.orbitdb_args['chunkSize'] = 8
        if self.orbitdb_args['swarmName'] is None:
            self.orbitdb_args['swarmName'] = "caselaw"
        if self.orbitdb_args['port'] is None:
            self.orbitdb_args['port'] = 50001
        pass

    def start_orbitdb(self):
        start_args = self.orbitdb_args
        start_argstring = ''
        for key, value in start_args.items():
            start_argstring += ' --' + key + '=' + str(value) + ' '
        start_cmd = 'node ' + os.path.join(self.this_dir, 'orbitv3-slave-swarm.js') + ' ' + start_argstring  
        start_orbitdb = process.Popen(start_cmd, stdout=process.PIPE, stderr=process.PIPE)
        return start_orbitdb
        pass

    def stop_orbitdb(self):
        start_args = self.orbitdb_args
        start_argstring = ''
        ps_orbitdb = 'ps -ef | grep orbitdb | grep -v grep | awk \'{print $2}\' | grep --port=' + start_args['port'] + ' | xargs kill -9'
        stop_orbitdb = process.Popen(ps_orbitdb, stdout=process.PIPE, stderr=process.PIPE)
        pass

    def get_resources(self):
        return self.resources
    
if __name__ == '__main__':
    resources = {}
    meta = {}
    orbitdb_kit = orbitdb_kit(resources, meta)
    print(orbitdb_kit.start_orbitdb())

