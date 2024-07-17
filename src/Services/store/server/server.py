import sys
import os
from concurrent import futures 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))

import StoreService_pb2_grpc
import services.StoreService


def serve():
   pass
if __name__ == '__main__':
    serve()
