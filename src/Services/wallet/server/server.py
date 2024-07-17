import sys
import os
from concurrent import futures 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))

import grpc
import WalletService_pb2_grpc
from services.WalletService import WalletService

def serve():
   # O servidor usa um modelo de pool de threads do pacote concurrent
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   # O servidor precisa ser ligado ao objeto que identifica os
   #   procedimentos a serem executados.
   WalletService_pb2_grpc.add_WalletServicer_to_server(WalletService(), server)
   server.add_insecure_port('localhost:8888')
   server.start()
   server.wait_for_termination()
   
if __name__ == '__main__':
    serve()
