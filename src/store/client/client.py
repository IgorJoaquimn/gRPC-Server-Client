from __future__ import print_function  # usado internamente nos stubs
import os
import sys
import grpc

# Adiciona o diretório 'src/protos' ao caminho do sistema para importar o código gerado pelo protobuf.
sys.path.insert(0, os.path.abspath("src/protos"))
import WalletService_pb2_grpc
import StoreService_pb2_grpc
from services.calls import *

def process_command(command, wallet_stub, store_stub, client_id, product_price):
    """
    Processa o comando recebido do usuário e executa a ação correspondente.

    - command (str): O comando fornecido pelo usuário.
    - wallet_stub: O stub gRPC para o serviço Wallet.
    - store_stub: O stub gRPC para o serviço Store.
    - client_id (str): O identificador da carteira do cliente.
    - product_price (int): O preço do produto.

    Retorna True se o comando 'T' for processado e a execução do servidor deve ser finalizada.
    """
    parts = command.split()
    cmd = parts[0]
    
    if cmd == 'C':
        # Comando para comprar o produto
        buy_product(store_stub, wallet_stub, client_id, product_price)
    elif cmd == 'T':
        # Comando para finalizar o servidor
        return finish_server(store_stub, wallet_stub)
    
    return False

def run():
    """
    Função principal que configura os stubs e lida com a entrada do usuário.

    - Verifica se os argumentos de linha de comando estão corretos.
    - Cria canais para conectar-se aos servidores gRPC.
    - Obtém o preço do produto e inicia o loop de entrada do usuário.
    """
    if len(sys.argv) != 4:
        print("Uso: make run_cli_loja arg1=Dorgival arg2=localhost:5555 arg3=localhost:6666")
        sys.exit(1)

    client_id   = sys.argv[1]
    wallet_addr = sys.argv[2]
    store_addr  = sys.argv[3]

    # Cria canais para se conectar aos servidores gRPC de wallet e store
    with grpc.insecure_channel(wallet_addr) as channel_wallet, \
         grpc.insecure_channel(store_addr) as channel_store:

        wallet_stub     = WalletService_pb2_grpc.WalletStub(channel_wallet)
        store_stub      = StoreService_pb2_grpc.StoreStub(channel_store)
        product_price   = get_price(store_stub)

        
        try:
            for line in sys.stdin:
                if not line: continue
                if process_command(line, wallet_stub, store_stub, client_id, product_price): break
        except EOFError:
            pass

if __name__ == '__main__':
    run()
