from __future__ import print_function  # usado internamente nos stubs
import os
import sys
import grpc

sys.path.insert(0, os.path.abspath("src/protos"))
import WalletService_pb2_grpc
import StoreService_pb2_grpc
from services.calls import *

def process_command(command, wallet_stub,store_stub, client_id,product_price):
    parts = command.split()
    cmd = parts[0]
    if cmd == 'C':
        buy_product(store_stub,wallet_stub,client_id,product_price)
    elif cmd == 'T':
        return finish_server(store_stub, wallet_stub)
    return False

def run():
    if len(sys.argv) != 4:
        print("Uso: make run_cli_loja arg1=Dorgival arg2=localhost:5555 arg3=localhost:6666")
        sys.exit(1)

    client_id   = sys.argv[1]
    wallet_addr = sys.argv[2]
    store_addr  = sys.argv[3]

    # Cria um canal para se conectar ao servidor gRPC
    with grpc.insecure_channel(wallet_addr) as channel_wallet, \
         grpc.insecure_channel(store_addr) as channel_store:

        wallet_stub     = WalletService_pb2_grpc.WalletStub(channel_wallet)
        store_stub      = StoreService_pb2_grpc.StoreStub(channel_store)
        product_price   = get_price(store_stub)

        try:
            while True:
                line = input()
                if not line: continue
                if process_command(line, wallet_stub,store_stub, client_id,product_price): break
        except EOFError:
            pass

if __name__ == '__main__':
    run()
