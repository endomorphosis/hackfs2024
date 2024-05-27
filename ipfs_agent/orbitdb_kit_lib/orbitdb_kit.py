import os
import sys
import subprocess as process 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import websockets as ws 
import asyncio
from config import config
import json
from websocket_kit import WebSocketClient
import datetime
import time

class orbitdb_kit():
    def __init__(self,  resources=None, meta=None):
        self.resources = resources
        self.meta = meta
        self.config = config
        self.connection = None
        self.orbitdb_args = {}
        self.peers = []
        self.ping = {}
        self.state = {
            "status": "disconnected"
        }
        self.ws = None
        self.url = None
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

    def start_orbitdb(self , args = None):
        start_args = self.orbitdb_args
        if args is not None:
            for key, value in args.items():
                start_args[key] = value
        start_argstring = ''
        for key, value in start_args.items():
            start_argstring += ' --' + key + '=' + str(value) + ' '
        start_cmd = 'node ' + os.path.join(self.this_dir, 'orbitv3-slave-swarm.js') + ' ' + start_argstring  
        print(start_cmd)
        start_cmd = start_cmd.split(' ')
        start_orbitdb = process.Popen(start_cmd)
        # start_orbitdb = process.Popen(start_cmd, shell=True)
        # start_orbitdb = process.run(start_cmd, stdout=process.PIPE, stderr=process.PIPE)
        # pause for 5 seconds to allow orbitdb to start
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(5))
        asyncio.get_event_loop().run_until_complete(self.connect_orbitdb())
        return start_orbitdb
        pass

    async def connect_orbitdb(self, args = None):
        self.url = 'ws://' + self.orbitdb_args['ipaddress'] + ':' + str(self.orbitdb_args['port'])
        self.ws = WebSocketClient(self.url, 
            {
            "on_open" : self.on_open,
            "on_message" : self.on_message,
            "on_error" : self.on_error,
            "on_close" : self.on_close
            }
        )
        return self.ws
    
    def on_pong_message(self, ws, message):
        self.pong = message['pong']
        pass

    def on_ping_message(self, ws, recv):
        self.ping = recv['ping']
        pass

    def on_peers_message(self, ws, recv):
        self.peers = recv['peers']
        return self.peers
    
    def select_all(self, ws, recv):
        self.orbitdb = recv['select_all']
        return self.orbitdb
    
    def orbitdb_hash_list(self, ws, recv):
        hash_list = list(map(lambda x: x['hash'], self.orbitdb))
        return hash_list

    def insert(self, ws, recv):
        hash_list = self.orbitdb_hash_list(ws, recv)
        insert = recv['insert']
        hash = insert['hash']
        if hash not in hash_list:
            self.orbitdb.append(insert)

    def update(self, ws, recv):
        hash_list = self.orbitdb_hash_list(ws, recv)
        update = recv['update']
        hash = update['hash']
        if hash in hash_list:
            index = hash_list.index(hash)
            self.orbitdb[index] = update
        
    def delete(self, ws, recv):
        hash_list = self.orbitdb_hash_list(ws, recv)
        delete = recv['delete']
        hash = delete['hash']
        if hash in hash_list:
            index = hash_list.index(hash)
            self.orbitdb.pop(index)


    def on_message(self, ws, message):
        print(f"Received message: message = '{message}')")
        recv = json.loads(message)
        results = ""
        if 'pong' in recv:
            results = self.on_pong_message(
                ws, recv
            )
            
        if 'ping' in recv:
            results = self.on_ping_message(
                ws, recv
            )

        if 'peers' in recv:
            results = self.on_peers_message(
                ws, recv
            )
        
        if 'insert' in recv:
            results = self.insert(
                ws, recv
            )
        
        if 'select_all' in recv:
            results = self.select_all(
                ws, recv
            )
        
        if 'update' in recv:
            results = self.update(
                ws, recv
            )
        
        if 'delete' in recv:
            results = self.delete(
                ws, recv
            )
        


        print(results)
        return results
    
    def on_error(self, ws, error):
        print(f"Error occurred: {error}")
        return error

    def on_close(self, ws, arg1, arg2):
        print("Connection closed")
        return ws
    
    def on_open(self, ws):
        print('connection accepted')
        # ws.send(json.dumps({
        #     'event': 'init',
        #     'status': self.state['status']
        # }))
        ws.send(json.dumps({
            'peers': 'ls'
        }))
        ws.send(json.dumps({
            'ping': datetime.datetime.now().isoformat()
        }))
        ws.send(json.dumps({
            'insert': {
                'test': 'test document'
            }
        }))
        ws.send(json.dumps({
            'insert': {
                'test1': 'test document'
            }
        }))
        ws.send(json.dumps({
            'insert': {
                'test2': 'test document'
            }
        }))
        ws.send(json.dumps({
            'insert': {
                'test3': 'test document'
            }
        }))


        ws.send(json.dumps({
            'update': {
                'test': 'update document'
            }
        }))
        ws.send(json.dumps({
            'update': {
                'test1': 'update document'
            }
        }))
        ws.send(json.dumps({
            'update': {
                'test2': 'update document'
            }
        }))
        ws.send(json.dumps({
            'update': {
                'test3': 'update document'
            }
        }))


        ws.send(json.dumps({
            'select_all':  "*"
        }))
        results = self.main()
        print(results)
        return results


    async def send_recv(self,data_type, data, args):
        try:
            payload = {
                data_type: data
            }
            response = None
            payload = json.dumps(payload)
            if self.ws is not None:
                self.ws.send(payload)
                response = await self.ws.recv()
            return response
        except Exception as e:
            print(e)
            raise e
        finally:
            pass

    async def insert_orbitdb(self, data, args = None):
        try:
            results = await self.send_recv('insert', data, args)
            return results
        except Exception as e:
            print(e)
            raise e
        finally:
            pass

    def update_orbitdb(self, data, args = None):
        try:
            results = self.send_recv('update', data, args)
            return results
        except Exception as e:
            print(e)
            raise e
        finally:
            pass

    def select_orbitdb(self, data, args = None):
        try:
            results = self.send_recv('select', data, args)
            return results
        except Exception as e:
            print(e)
            raise e
        finally:
            pass

    def delete_orbitdb(self, data, args = None):
        try:
            results = self.send_recv('delete', data, args)
            return results
        except Exception as e:
            print(e)
            raise e
        finally:
            pass

    def select_all_orbitdb(self, args = None):
        try:
            results = self.send_recv('select_all', None, args)
            return results
        except Exception as e:
            print(e)
            raise e
        finally:
            pass

    def stop_orbitdb(self, args = None):
        ps_orbitb_results = None
        stop_orbitdb_results = None

        start_args = self.orbitdb_args
        if args is not None:
            for key, value in args.items():
                start_args[key] = value
        start_argstring = ''
        ps_orbitdb = 'ps -ef | grep orbitdb | grep -v grep | awk \'{print $2}\' | grep port=' + str(start_args['port']) + " "
        stop_orbitdb = 'ps -ef | grep orbitdb | grep -v grep | awk \'{print $2}\' | grep port=' + str(start_args['port']) + ' | xargs kill -9'
        print(ps_orbitdb)
        print(stop_orbitdb)
        try:
            ps_orbitb_results = process.check_output(ps_orbitdb, shell=True)
        except Exception as e:
            print(e)
            ps_orbitb_results = e
            pass
        finally:
            if ps_orbitb_results is not None and ( type == bytes or type == str):
                try:
                    stop_orbitdb_results = process.check_output(stop_orbitdb, shell=True)
                except Exception as e:
                    print(e)
                    raise e
                finally:
                    pass

        results = {
            'ps_orbitdb': ps_orbitb_results,
            'stop_orbitdb': stop_orbitdb_results
        }
        return results

    def get_resources(self):
        return self.resources
    
    def main(self):
        print("main")
        pass

    async def test(self):
        print("testing")
        await orbitdb_kit.connect_orbitdb()
    
if __name__ == '__main__':
    resources = {}
    meta = {}
    orbitdb_kit = orbitdb_kit(resources, meta)
    results = asyncio.run(orbitdb_kit.test())
    print("done")

