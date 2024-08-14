import WalletService_pb2
import StoreService_pb2


def get_price(store_stub):
    request  = StoreService_pb2.ReadPriceRequest()
    response = store_stub.ReadPrice(request)
    print(response.price)
    return response.price

def buy_product(store_stub,wallet_stub,client_id,product_price):
    status  = create_payment_order(wallet_stub,client_id,product_price)
    if(status > 0):
        request = StoreService_pb2.SellRequest(order_id = status)
        response = store_stub.Sell(request)
        print(response.status)


def create_payment_order(stub, client_id, value):
    request = WalletService_pb2.CreatePaymentOrderRequest(wallet=client_id, value=value)
    response = stub.CreatePaymentOrder(request)
    print(response.status)
    return response.status

def finish_server(store_stub, wallet_stub):
    """Finish execution on both the store and wallet servers and print results."""
    
    # Finish execution for the store server
    store_request = StoreService_pb2.EndExecutionRequest()  # Assuming similar request for store
    store_response = store_stub.EndExecution(store_request)
    print(store_response.status)
    return store_response.status