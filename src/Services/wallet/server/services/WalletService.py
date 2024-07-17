import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../protos')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))

import WalletService_pb2_grpc
from Manager import Manager

class WalletService(WalletService_pb2_grpc.WalletServicer):
    def __init__(self) -> None:
        super().__init__()
        self.m = Manager()

    def ReadBalance(self, request, context):
        # WalletService_pb2_grpc.ReadBalanceResponse
        value = self.m.get_wallet(request.wallet)
        response = WalletService_pb2_grpc.ReadBalanceResponse(value = value)
        return response

    def CreatePaymentOrder(self, request, context):
        # WalletService_pb2_grpc.CreatePaymentOrderResponse
        status,order_id = self.m.create_payment_order(request.wallet)
        response = WalletService_pb2_grpc.CreatePaymentOrderResponse(status = status,order_id = order_id)
        return response

    def Transfer(self, request, context):
        # WalletService_pb2_grpc.TransferResponse
        status = self.m.start_transaction(request.wallet,request.value)
        response = WalletService_pb2_grpc.TransferResponse(status = status)
        return response

    def EndExecution(self, request, context):
        # WalletService_pb2_grpc.EndExecutionResponse
        return None