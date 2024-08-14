class Manager:
    def __init__(self):
        """
        Inicializa a classe Manager, responsável por gerenciar as carteiras e as ordens de pagamento.
        
        - ordem_id (int): Identificador único incremental para ordens de pagamento.
        - wallets (dict): Dicionário para armazenar os saldos das carteiras.
        - orders (dict): Dicionário para armazenar as ordens de pagamento.
        """
        self.ordem_id = 0
        self.wallets = {}
        self.orders = {}

    def get_wallet(self, id):
        """
        Retorna o saldo da carteira identificada pelo 'id'.

        - id (str): Identificador da carteira a ser consultada.

        Retorna o saldo da carteira se existir, caso contrário, retorna -1.
        """
        if id in self.wallets:
            return self.wallets[id]
        return -1

    def create_payment_order(self, wallet, value):
        """
        Cria uma nova ordem de pagamento na carteira especificada.

        - wallet (str): Identificador da carteira de onde o valor será debitado.
        - value (int): Valor a ser debitado da carteira.

        Retorna:
        - -1: Se a carteira não existir.
        - -2: Se o saldo da carteira for insuficiente.
        - ordem_id (int): Identificador da nova ordem de pagamento, se bem-sucedido.
        """
        # Se a carteira não existe, retorna -1.
        if wallet not in self.wallets:
            return -1

        # Se o valor a ser debitado é maior que o saldo na carteira, retorna -2.
        if self.wallets[wallet] < value:
            return -2

        # Em caso de sucesso, cria uma nova ordem de pagamento e retorna o identificador da ordem.
        self.ordem_id += 1
        self.wallets[wallet] -= value
        self.orders[self.ordem_id] = (wallet, value)

        return self.ordem_id

    def start_transaction(self, order, conference, wallet):
        """
        Inicia uma transação de transferência de valores entre carteiras.

        - order (int): Identificador da ordem de pagamento a ser transferida.
        - conference (int): Valor a ser transferido, que deve coincidir com o valor da ordem.
        - wallet (str): Identificador da carteira de destino.

        Retorna:
        - -1: Se a ordem de pagamento não existir.
        - -2: Se o valor da ordem for diferente do valor de conferência.
        - -3: Se a carteira de destino não existir.
        - 0: Se a transação for bem-sucedida.
        """
        # Se a ordem de pagamento não existe, retorna -1.
        if order not in self.orders:
            return -1
        # Se o valor da ordem difere do valor de conferência, retorna -2.
        if self.orders[order][1] != conference:
            return -2
        # Se a carteira de destino não existe, retorna -3.
        if wallet not in self.wallets:
            return -3

        # Em caso de sucesso, transfere o valor e remove a ordem de pagamento.
        self.wallets[wallet] += conference
        del self.orders[order]
        
        return 0

    def __del__(self):
        """
        Destrutor da classe Manager, que imprime o saldo de todas as carteiras no momento da destruição.
        """
        for k, v in self.wallets.items():
            print(k, v)
