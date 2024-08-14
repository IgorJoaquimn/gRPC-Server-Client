import sys
import os

# Adiciona o diretório 'protos'ao caminho do sistema para importar o código necessário.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))

import WalletService_pb2_grpc
import WalletService_pb2
from Manager import Manager

class WalletService(WalletService_pb2_grpc.WalletServicer):
    def __init__(self, stop_event):
        """
        Inicializa o WalletService com um evento de parada e uma instância do gerenciador de transações.

        - stop_event (threading.Event): Evento usado para sinalizar quando o servidor deve parar.
        """
        super().__init__()
        self._stop_event = stop_event
        self.m = Manager()

    def ReadBalance(self, request, context):
        """
        Retorna o saldo da carteira solicitada.

        - request.wallet (str): O identificador da carteira para a qual o saldo é solicitado.

        Retorna uma resposta ReadBalanceResponse com o saldo da carteira.
        """
        value = self.m.get_wallet(request.wallet)
        response = WalletService_pb2.ReadBalanceResponse(value=value)
        return response

    def CreatePaymentOrder(self, request, context):
        """
        Cria uma ordem de pagamento na carteira especificada.

        - request.wallet (str): O identificador da carteira para a qual a ordem de pagamento será criada.
        - request.value (int): O valor da ordem de pagamento.

        Retorna uma resposta CreatePaymentOrderResponse com o status da criação da ordem de pagamento.
        """
        status = self.m.create_payment_order(request.wallet, request.value)
        response = WalletService_pb2.CreatePaymentOrderResponse(status=status)
        return response

    def Transfer(self, request, context):
        """
        Inicia uma transação de transferência de valores entre carteiras.

        - request.order_id (int): O identificador da ordem de pagamento a ser transferida.
        - request.conference_value (int): O valor a ser transferido.
        - request.wallet (str): O identificador da carteira de origem da transferência.

        Retorna uma resposta TransferResponse com o status da transação.
        """
        status = self.m.start_transaction(request.order_id, request.conference_value, request.wallet)
        response = WalletService_pb2.TransferResponse(status=status)
        return response

    def EndExecution(self, request, context):
        """
        Finaliza a execução do servidor de carteira, liberando recursos e sinalizando a parada.

        Retorna uma resposta EndExecutionResponse contendo o número de ordens pendentes.
        """
        orders_count = len(self.m.orders)
        del self.m
        self._stop_event.set()
        return WalletService_pb2.EndExecutionResponse(pending_orders_count=orders_count)
