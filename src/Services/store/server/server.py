import os
import sys
import grpc
from concurrent import futures 
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))

import StoreService_pb2_grpc
from services.StoreService import StoreService

def serve():
   # O servidor usa um modelo de pool de threads do pacote concurrent
   stop_event = threading.Event()
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   # O servidor precisa ser ligado ao objeto que identifica os
   #   procedimentos a serem executados.
   StoreService_pb2_grpc.add_StoreServicer_to_server(StoreService(stop_event), server)
   server.add_insecure_port(f'localhost:{sys.argv[1]}')
   server.start()
   stop_event.wait()
   server.stop(None)
   
if __name__ == '__main__':
   if len(sys.argv) != 4:
      print("make run_serve_banco arg1=<número do porto>")
      sys.exit(1)
   serve()