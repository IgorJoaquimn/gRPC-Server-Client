from __future__ import print_function  # usado internamente nos stubs
import os
import sys
import grpc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))
import WalletService_pb2_grpc
from services.calls import *

def process_command(command, stub, client_id):
    parts = command.split()
    cmd = parts[0]
    
    if cmd == 'S':
        get_balance(stub, client_id)
    elif cmd == 'O' and len(parts) == 2:
        value = int(parts[1])
        create_payment_order(stub, client_id, value)
    elif cmd == 'X' and len(parts) == 4:
        order_id = int(parts[1])
        conference_value = int(parts[2])
        dest_id = parts[3]
        transfer(stub, order_id, conference_value, dest_id)
    elif cmd == 'F':
        return finish_server(stub)
    return False

def run():
    if len(sys.argv) != 3:
        print("Uso: python client.py <id_carteira> <endereço_servidor>")
        sys.exit(1)
        
    client_id = sys.argv[1]
    server_address = sys.argv[2]

    # Cria um canal para se conectar ao servidor gRPC
    with grpc.insecure_channel(server_address) as channel:
        stub = WalletService_pb2_grpc.WalletStub(channel)
        print("Running...")

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
