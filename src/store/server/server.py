import os
import sys
import grpc
from concurrent import futures 
import threading

sys.path.insert(0, os.path.abspath("src/protos"))
import StoreService_pb2_grpc
from services.StoreService import StoreService

def serve():
   product_price = sys.argv[1]
   port = sys.argv[2]
   my_id = sys.argv[3]
   wallet_addr = sys.argv[4]
   # O servidor usa um modelo de pool de threads do pacote concurrent
   stop_event = threading.Event()
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   # O servidor precisa ser ligado ao objeto que identifica os
   #   procedimentos a serem executados.
   StoreService_pb2_grpc.add_StoreServicer_to_server(StoreService(stop_event,product_price,my_id,wallet_addr), server)
   server.add_insecure_port(f'localhost:{port}')
   server.start()
   stop_event.wait()
   server.stop(None)
   
if __name__ == '__main__':
   if len(sys.argv) != 5:
      print("Uso: make run_serv_loja arg1=10 arg2=6666 arg3=Papai_Noel arg4=localhost:5555")
      sys.exit(1)
   serve()