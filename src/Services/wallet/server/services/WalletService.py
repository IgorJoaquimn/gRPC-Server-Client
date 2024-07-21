import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../protos')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))

import WalletService_pb2_grpc
import WalletService_pb2
from Manager import Manager

class WalletService(WalletService_pb2_grpc.WalletServicer):
    def __init__(self, stop_event):
        super().__init__()
        self._stop_event = stop_event
        self.m = Manager()

    def ReadBalance(self, request, context):
        # WalletService_pb2_grpc.ReadBalanceResponse
        value = self.m.get_wallet(request.wallet)
        response = WalletService_pb2.ReadBalanceResponse(value = value)
        return response

    def CreatePaymentOrder(self, request, context):
        # WalletService_pb2.CreatePaymentOrderResponse
        status = self.m.create_payment_order(request.wallet,request.value)
        response = WalletService_pb2.CreatePaymentOrderResponse(status = status)
        return response

    def Transfer(self, request, context):
        # WalletService_pb2.TransferResponse
        status = self.m.start_transaction(request.order_id,request.conference_value,request.wallet)
        response = WalletService_pb2.TransferResponse(status = status)
        return response

    def EndExecution(self, request, context):
        # WalletService_pb2.EndExecutionResponse
        self._stop_event.set()
        return WalletService_pb2.ShutdownResponse()