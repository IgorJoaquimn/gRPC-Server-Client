from __future__ import print_function
import os
import sys
import grpc

# Adiciona o diretório 'src/protos' ao caminho do sistema para importar o código gerado pelo protobuf.
sys.path.insert(0, os.path.abspath("src/protos"))
import WalletService_pb2_grpc
from services.calls import *

def process_command(command, stub, client_id):
    """
    Processa um comando recebido e executa a ação correspondente usando o stub do serviço Wallet.

    - command (str): O comando a ser processado.
    - stub: O stub gRPC para o serviço Wallet.
    - client_id (str): O identificador da carteira do cliente.

    Retorna True se a execução de um comando específico (como 'F') indicar que o servidor deve ser finalizado,
    e False caso contrário.
    """
    parts = command.split()
    cmd = parts[0]
    
    if cmd == 'S':
        # Solicita o saldo da carteira.
        get_balance(stub, client_id)
    elif cmd == 'O' and len(parts) == 2:
        # Cria uma ordem de pagamento com o valor fornecido.
        value = int(parts[1])
        create_payment_order(stub, client_id, value)
    elif cmd == 'X' and len(parts) == 4:
        # Realiza uma transferência com os parâmetros fornecidos.
        order_id = int(parts[1])
        conference_value = int(parts[2])
        dest_id = parts[3]
        transfer(stub, order_id, conference_value, dest_id)
    elif cmd == 'F':
        # Solicita a finalização do servidor.
        return finish_server(stub)
    
    return False

def run():
    """
    Função principal que inicializa o cliente gRPC, conecta ao servidor e processa comandos do usuário.
    """
    if len(sys.argv) != 3:
        print("Uso: python client.py <id_carteira> <endereço_servidor>")
        sys.exit(1)
    
    client_id = sys.argv[1]
    server_address = sys.argv[2]

    # Cria um canal para se conectar ao servidor gRPC
    with grpc.insecure_channel(server_address) as channel:
        stub = WalletService_pb2_grpc.WalletStub(channel)

        try:
            while True:
                line = input()
                if not line:
                    continue
                if process_command(line, stub, client_id):
                    break
        except EOFError:
            pass

if __name__ == '__main__':
    run()
