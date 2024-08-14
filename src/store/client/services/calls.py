import WalletService_pb2
import StoreService_pb2

def get_price(store_stub):
    """
    Solicita o preço atual do produto da loja e imprime o resultado.

    - store_stub: O stub gRPC para o serviço Store.

    Retorna o preço do produto.
    """
    request = StoreService_pb2.ReadPriceRequest()
    response = store_stub.ReadPrice(request)
    print(response.price)
    return response.price

def buy_product(store_stub, wallet_stub, client_id, product_price):
    """
    Realiza a compra de um produto, criando uma ordem de pagamento e
    processando a venda na loja.

    - store_stub: O stub gRPC para o serviço Store.
    - wallet_stub: O stub gRPC para o serviço Wallet.
    - client_id (str): O identificador da carteira do cliente.
    - product_price (int): O preço do produto a ser comprado.

    A função cria uma ordem de pagamento e, se a ordem for bem-sucedida,
    processa a venda do produto.
    """
    status = create_payment_order(wallet_stub, client_id, product_price)
    if status > 0:
        request = StoreService_pb2.SellRequest(order_id=status)
        response = store_stub.Sell(request)
        print(response.status)

def create_payment_order(stub, client_id, value):
    """
    Cria uma ordem de pagamento para o valor especificado e imprime o status da operação.

    - stub: O stub gRPC para o serviço Wallet.
    - client_id (str): O identificador da carteira do cliente.
    - value (int): O valor da ordem de pagamento.

    Retorna o status da criação da ordem de pagamento.
    """
    request = WalletService_pb2.CreatePaymentOrderRequest(wallet=client_id, value=value)
    response = stub.CreatePaymentOrder(request)
    print(response.status)
    return response.status

def finish_server(store_stub, wallet_stub):
    """
    Finaliza a execução tanto no servidor da loja quanto no servidor de carteiras
    e imprime os resultados.

    - store_stub: O stub gRPC para o serviço Store.
    - wallet_stub: O stub gRPC para o serviço Wallet.

    Retorna o status da finalização do servidor da loja.
    """
    # Solicita a finalização do servidor da loja
    store_request = StoreService_pb2.EndExecutionRequest()  # Supondo uma solicitação semelhante para a loja
    store_response = store_stub.EndExecution(store_request)
    print(store_response.status)
    return store_response.status
