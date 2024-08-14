import os
import sys
import grpc
from concurrent import futures 
import threading
from services.StoreService import StoreService

# Adiciona o diretório 'src/protos' ao caminho do sistema para importar o código gerado pelo protobuf.
sys.path.insert(0, os.path.abspath("src/protos"))
import StoreService_pb2_grpc

def serve():
   """
   O servidor é vinculado à implementação do StoreService, que lida com a lógica do serviço, 
   como leitura de preços de produtos, processamento de vendas e gerenciamento da finalização da execução.

   - product_price (str): O preço do produto sendo vendido.
   - port (str): A porta na qual o servidor irá escutar conexões.
   - my_id (str): O identificador da loja, usado na comunicação com o serviço de carteira.
   - wallet_addr (str): O endereço do serviço de carteira para lidar com transações de pagamento.
   """

   product_price = sys.argv[1]
   port = sys.argv[2]
   my_id = sys.argv[3]
   wallet_addr = sys.argv[4]
   
   # Cria um evento que pode ser usado para sinalizar quando o servidor deve parar.
   stop_event = threading.Event()
   # Registra o StoreService com o servidor, ligando a implementação do serviço ao servidor gRPC.
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   StoreService_pb2_grpc.add_StoreServicer_to_server(
      StoreService(stop_event, product_price, my_id, wallet_addr), server
   )
   # Vincula o servidor à porta especificada.
   server.add_insecure_port(f'localhost:{port}')
   server.start()
   # Aguarda até que o stop_event seja acionado, o que indicará que o servidor deve parar.
   stop_event.wait()
   server.stop(None)
   
if __name__ == '__main__':
   if len(sys.argv) != 5:
      print("Uso: make run_serv_loja arg1=10 arg2=6666 arg3=Papai_Noel arg4=localhost:5555")
      sys.exit(1)
   serve()