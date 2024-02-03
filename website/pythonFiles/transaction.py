class transaction:
    #trans_id = 0
    def __init__(self, length, items_bought, amount_spent, trans_date, user_id):
        # transaction.trans_id += 1
        self.__trans_id = length + 1
        self.__items_bought = items_bought
        self.__amount_spent = amount_spent
        self.__trans_date = trans_date
        self.__user_id = user_id
        #self.__trans_id = 0
        
    def __repr__(self):
        pass
        return repr(f"trans_id = {self.__trans_id} \n amount = {self.__amount_spent} \n items_bought = {self.__items_bought}")

    def set_items_bought(self,items_bought):
        self.__items_bought = items_bought

    def set_amount_spent(self,amount_spent):
        self.__amount_spent = amount_spent

    def set_trans_date(self,trans_date):
        self.__trans_date = trans_date
        
    def set_user_id(self, user_id):
        self._user_id = str(user_id)

    def get_items_bought(self):
        return self.__items_bought

    def get_amount_spent(self):
        return self.__amount_spent

    def get_trans_date(self):
        return self.__trans_date
    
    def get_trans_id(self):
        return self.__trans_id
    
    def get_user_id(self):
        return self.__user_id


    

