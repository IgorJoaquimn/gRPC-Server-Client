class Manager():
    def __init__(self) -> None:
        self.ordem_id   = 1
        self.filename   = "db.json"
        self.wallets    = []
        self.orders     = []
    
    def get_wallet(self,id):
        value = 0
        return value
    
    def create_payment_order(self,wallet, value):
        status      = 0
        order_id    = 0
        return status,order_id

    def start_transaction(self,order,conference,wallet):
        status      = 0
        return status