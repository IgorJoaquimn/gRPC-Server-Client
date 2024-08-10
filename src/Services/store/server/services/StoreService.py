import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../protos')))
sys.path.insert(0, os.path.abspath("src/Services/wallet/protos"))

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
            resp = stub.Transfer(request)

        response = StoreService_pb2.SellResponse(status = resp.status)
        return response

    def EndExecution(self, request, context):
        # StoreService_pb2.EndExecutionResponse
        self._stop_event.set()
        return StoreService_pb2.EndExecutionResponse()