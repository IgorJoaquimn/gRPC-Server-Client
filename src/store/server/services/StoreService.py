import sys
import os

# Adiciona o diretório 'src/protos' ao caminho do sistema para importar o código gerado pelo protobuf.
sys.path.insert(0, os.path.abspath("src/protos"))
import WalletService_pb2_grpc
import StoreService_pb2_grpc
import StoreService_pb2
import WalletService_pb2
import grpc


class StoreService(StoreService_pb2_grpc.StoreServicer):
    def __init__(self, stop_event, product_price, my_id, wallet_addr):
        """
        Inicializa o StoreService com os parâmetros necessários e define variáveis internas.

        - stop_event (threading.Event): Evento usado para sinalizar quando o servidor deve parar.
        - product_price (int): O preço do produto sendo vendido.
        - my_id (str): O identificador da loja, usado na comunicação com o serviço de carteira.
        - wallet_addr (str): O endereço do serviço de carteira para lidar com transações de pagamento.
        """
        super().__init__()
        self._stop_event = stop_event
        self.product_price = int(product_price)
        self.my_id = my_id
        self.wallet_addr = wallet_addr
        self.balance = 0  # Saldo interno da conta do vendedor

    def ReadPrice(self, request, context):
        """
        Retorna uma resposta ReadPriceResponse com o preço do produto.
        """
        response = StoreService_pb2.ReadPriceResponse(price=self.product_price)
        return response

    def Sell(self, request, context):
        """
        Processa uma solicitação de venda, comunicando-se com o serviço de carteira
        para transferir o valor correspondente ao produto vendido.

        - request.order_id (int): O ID do pedido recebido do cliente.

        Retorna uma resposta SellResponse com o status da transferência.
        Se a transferência for bem-sucedida (resp.status > 0), o saldo interno 
        da conta do vendedor (self.balance) é atualizado.
        """
        order_id = request.order_id  # ID do pedido recebido na solicitação

        # Abre um canal inseguro com o serviço de carteira para realizar a transferência
        with grpc.insecure_channel(self.wallet_addr) as channel:
            stub = WalletService_pb2_grpc.WalletStub(channel)
            req = WalletService_pb2.TransferRequest(
                order_id=order_id, 
                conference_value=self.product_price, 
                wallet=self.my_id
            )
            resp = stub.Transfer(req)
        
        # Atualiza o saldo do vendedor se a transferência for bem-sucedida
        if resp.status > 0:
            self.balance += self.product_price

        response = StoreService_pb2.SellResponse(status=resp.status)
        return response

    def EndExecution(self, request, context):
        """
        Finaliza a execução do servidor, comunicando-se primeiro com o serviço de carteira
        para obter o número de pedidos pendentes e, em seguida, sinaliza a parada do servidor.

        Retorna uma resposta EndExecutionResponse contendo:
        - balance (int): O saldo interno da conta do vendedor.
        - status (int): O número de pedidos pendentes retornado pelo serviço de carteira.
        """
        # Comunicação com o serviço de carteira para finalizar sua execução e obter status
        with grpc.insecure_channel(self.wallet_addr) as channel:
            wallet_stub = WalletService_pb2_grpc.WalletStub(channel)
            wallet_request = WalletService_pb2.EndExecutionRequest()
            wallet_response = wallet_stub.EndExecution(wallet_request)

        # Sinaliza que o servidor deve parar
        self._stop_event.set()

        response = StoreService_pb2.EndExecutionResponse(
            balance=self.balance,
            status=wallet_response.pending_orders_count
        )
        return response
