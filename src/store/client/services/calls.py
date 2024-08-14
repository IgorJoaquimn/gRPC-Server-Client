import WalletService_pb2
import StoreService_pb2


def get_price(store_stub):
    request  = StoreService_pb2.ReadPriceRequest()
    response = store_stub.ReadPrice(request)
    print("Price",response.price)
    return response.price

def buy_product(store_stub,wallet_stub,client_id,product_price):
    status  = create_payment_order(wallet_stub,client_id,product_price)
    request = StoreService_pb2.SellRequest(order_id = status)
    response = store_stub.Sell(request)
    print("Resp",status,response)


def create_payment_order(stub, client_id, value):
    request = WalletService_pb2.CreatePaymentOrderRequest(wallet=client_id, value=value)
    response = stub.CreatePaymentOrder(request)
    return response.status

def finish_server(store_stub, wallet_stub):
    """Finish execution on both the store and wallet servers and print results."""
    
    # Finish execution for the wallet server
    wallet_request = WalletService_pb2.EndExecutionRequest()
    wallet_response = wallet_stub.EndExecution(wallet_request)
    for wallet_balance in wallet_response.wallet_balances:
        print(f"{wallet_balance.wallet}: {wallet_balance.value}")
    print(f"Pending orders: {wallet_response.pending_orders_count}")

    # Finish execution for the store server
    store_request = StoreService_pb2.EndExecutionRequest()  # Assuming similar request for store
    store_response = store_stub.EndExecution(store_request)
    return True