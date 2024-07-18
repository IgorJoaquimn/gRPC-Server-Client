import os
import sys
import grpc
from concurrent import futures 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))

import WalletService_pb2_grpc
from services.WalletService import WalletService

def read_command_line():
   m = WalletService()
   try:
        while True:
            line = input()
            if line:
               identifier, value = line.split()
               m.m.wallets[identifier] = int(value)
   except EOFError:
      pass
   return m

def serve():
   # O servidor usa um modelo de pool de threads do pacote concurrent
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   # O servidor precisa ser ligado ao objeto que identifica os
   #   procedimentos a serem executados.
   WalletService_pb2_grpc.add_WalletServicer_to_server(read_command_line(), server)
   server.add_insecure_port(f'localhost:{sys.argv[1]}')
   server.start()
   server.wait_for_termination()
   
if __name__ == '__main__':
   if len(sys.argv) != 2:
      print("make run_serve_banco arg1=<número do porto>")
      sys.exit(1)


   print("Serving...")
   serve()
