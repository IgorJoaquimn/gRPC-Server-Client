import sys
import os

sys.path.insert(0, os.path.abspath("src/protos"))
import WalletService_pb2_grpc
import StoreService_pb2_grpc
import StoreService_pb2
import WalletService_pb2
import grpc


class StoreService(StoreService_pb2_grpc.StoreServicer):
    def __init__(self, stop_event,product_price,my_id,wallet_addr):
        super().__init__()
        self._stop_event = stop_event
        self.product_price = int(product_price)
        self.my_id = my_id
        self.wallet_addr = wallet_addr
        self.balance = 0

    def ReadPrice(self,request,context):
        # StoreService_pb2.ReadPriceResponse
        response = StoreService_pb2.ReadPriceResponse(price = self.product_price)
        return response

    def Sell(self,request,context):
        # StoreService_pb2.SellResponse
        order_id = request.order_id

        with grpc.insecure_channel(self.wallet_addr) as channel:
            stub = WalletService_pb2_grpc.WalletStub(channel)
            req = WalletService_pb2.TransferRequest(order_id=order_id, conference_value=self.product_price, wallet=self.my_id)
            resp = stub.Transfer(req)
        
        if(resp.status > 0):
            self.balance += self.product_price

        response = StoreService_pb2.SellResponse(status = resp.status)
        return response

    def EndExecution(self, request, context):
        # StoreService_pb2.EndExecutionResponse

        with grpc.insecure_channel(self.wallet_addr) as channel:
            wallet_stub = WalletService_pb2_grpc.WalletStub(channel)
            wallet_request = WalletService_pb2.EndExecutionRequest()
            wallet_response = wallet_stub.EndExecution(wallet_request)

        self._stop_event.set()

        response = StoreService_pb2.EndExecutionResponse(
            balance=self.balance,
            status=wallet_response.pending_orders_count
        )
        return response