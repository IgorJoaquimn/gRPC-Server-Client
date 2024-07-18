from collections import defaultdict
class Manager():
    def __init__(self):
        self.ordem_id   = 0
        self.wallets    = {}
        self.orders     = {}
    
    def get_wallet(self,id):
        if(id in self.wallets):
            return self.wallets[id]
        return -1
    
    def create_payment_order(self,wallet, value):
        #se a carteira não existe, retorna -1; 
        if(wallet not in self.wallets):
            return -1

        #se o valor a ser debitado é maior que o saldo na carteira, retorna -2.
        v = self.wallets[wallet]
        if(v < value):
            return -2

        #em caso de sucesso, retorna o inteiro identificador da ordem
        self.ordem_id+=1
        self.orders[self.ordem_id] = (wallet,value)

        return self.ordem_id

    def start_transaction(self,order,conference,wallet):
        # se a ordem de pagamento não existe, retorna -1; 
        if(order not in self.orders):
            return -1
        # se o valor da ordem difere do valor de conferência, retorna -2; 
        if(self.orders[order][1] != conference):
            return -2
        # se a string não corresponde a uma carteira existente, retorna -3.
        if(wallet not in self.wallets):
            return -3
        # em caso de sucesso, retorna zero depois de remover a ordem de pagamento indicada e fazer a transferência do valor associado para a carteira identificada (string), sendo que, como controle, verifica primeiro se a ordem possui o valor fornecido para conferência;
        if(conference < self.wallets[wallet]):
            self.wallets[wallet] -= conference
            del self.orders[order]
        # em caso de sucesso, retorna zero;
        return 0