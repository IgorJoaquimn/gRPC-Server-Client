import WalletService_pb2

def get_balance(stub, client_id):
    """
    Solicita o saldo da carteira para um cliente e imprime o valor.

    - stub: O stub gRPC para o serviço Wallet.
    - client_id (str): O identificador da carteira do cliente.

    Retorna o saldo da carteira.
    """
    request = WalletService_pb2.ReadBalanceRequest(wallet=client_id)
    response = stub.ReadBalance(request)
    print(response.value)
    return response.value

def create_payment_order(stub, client_id, value):
    """
    Cria uma ordem de pagamento para um cliente e imprime o status da criação.

    - stub: O stub gRPC para o serviço Wallet.
    - client_id (str): O identificador da carteira do cliente.
    - value (int): O valor da ordem de pagamento.

    Retorna o status da criação da ordem de pagamento.
    """
    request = WalletService_pb2.CreatePaymentOrderRequest(wallet=client_id, value=value)
    response = stub.CreatePaymentOrder(request)
    print(response.status)
    return response.status

def transfer(stub, order_id, conference_value, dest_id):
    """
    Realiza uma transferência de valor para uma carteira destino e imprime o status da transferência.

    - stub: O stub gRPC para o serviço Wallet.
    - order_id (int): O identificador da ordem de pagamento.
    - conference_value (int): O valor da conferência.
    - dest_id (str): O identificador da carteira destino.

    Retorna o status da transferência.
    """
    request = WalletService_pb2.TransferRequest(order_id=order_id, conference_value=conference_value, wallet=dest_id)
    response = stub.Transfer(request)
    print(response.status)
    return response.status

def finish_server(stub):
    """
    Solicita a finalização do servidor e imprime o número de ordens pendentes.

    - stub: O stub gRPC para o serviço Wallet.

    Retorna o número de ordens pendentes.
    """
    request = WalletService_pb2.EndExecutionRequest()
    response = stub.EndExecution(request)
    print(response.pending_orders_count)
    return response.pending_orders_count
