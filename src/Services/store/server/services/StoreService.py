import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../protos')))

import StoreService_pb2_grpc

class StoreService(StoreService_pb2_grpc.StoreService):
    def ReadPrice(self,request,context):
        pass
    def Sell(self,request,context):
        pass
    def EndExecution(self,request,context):
        pass