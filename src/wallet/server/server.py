import os
import sys
import grpc
from concurrent import futures
import threading

# Adiciona o diretório 'src/protos' ao caminho do sistema para importar o código gerado pelo protobuf.
sys.path.insert(0, os.path.abspath("src/protos"))

import WalletService_pb2_grpc
from services.WalletService import WalletService

def read_command_line(stop_event):
   """
   Lê comandos da linha de comando para adicionar saldos às carteiras.

   - stop_event (threading.Event): Evento usado para sinalizar quando o servidor deve parar.

   Retorna uma instância de WalletService inicializada com os valores lidos.
   """
   wallet_service = WalletService(stop_event)
   try:
      for line in sys.stdin:
         identifier, value = line.split()
         wallet_service.m.wallets[identifier] = int(value)
   except EOFError:
      pass

   return wallet_service

def serve():
   """
   Configura e inicia o servidor gRPC para o serviço WalletService.

   - O servidor é configurado para utilizar um pool de threads e espera até
   que o evento stop_event seja acionado para finalizar sua execução.
   """
   # Cria um evento que pode ser usado para sinalizar quando o servidor deve parar.
   stop_event = threading.Event()
   # Registra o WalletService com o servidor, ligando a implementação do serviço ao servidor gRPC.
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   WalletService_pb2_grpc.add_WalletServicer_to_server(read_command_line(stop_event), server)
   # Vincula o servidor à porta especificada pelo argumento da linha de comando.
   server.add_insecure_port(f'0.0.0.0:{sys.argv[1]}')
   server.start()
   # Aguarda até que o stop_event seja acionado, o que indicará que o servidor deve parar.
   stop_event.wait()
   server.stop(None)

if __name__ == '__main__':
    # Verifica se o número correto de argumentos foi fornecido.
    if len(sys.argv) != 2:
        print("Uso: make run_serve_banco arg1=<número do porto>")
        sys.exit(1)
    serve()
