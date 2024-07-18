import WalletService_pb2

def get_balance(stub, client_id):
    request = WalletService_pb2.ReadBalanceRequest(wallet=client_id)
    response = stub.ReadBalance(request)
    print(response.value)

def create_payment_order(stub, client_id, value):
    request = WalletService_pb2.CreatePaymentOrderRequest(wallet=client_id, value=value)
    response = stub.CreatePaymentOrder(request)
    print(response.status)

def transfer(stub, order_id, conference_value, dest_id):
    request = WalletService_pb2.TransferRequest(order_id=order_id, conference_value=conference_value, wallet=dest_id)
    response = stub.Transfer(request)
    print(response.status)

def finish_server(stub):
    request = WalletService_pb2.EndExecutionRequest()
    response = stub.EndExecution(request)
    for wallet_balance in response.wallet_balances:
        print(f"{wallet_balance.wallet}: {wallet_balance.value}")
    print(f"Pending orders: {response.pending_orders_count}")
    return True
