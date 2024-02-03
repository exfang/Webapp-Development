#from website.pythonFiles.Forms import AddProd
class Add_Prod:
    def __init__(self, id, name, price, category, stock, size, colors, description, image):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__category = category
        self.__stock = stock
        self.__size = size
        self.__colors = colors
        self.__description = description
        self.__image = image
        self.prodid = 0
    
    def create_id(self):
        self.prodid += 1
        return self.prodid
    
    def check_num(self):
        uids = self.read()
        if uids:
            uid = uids[-1]
            self.counter = int(uid) + 1
        else:
            pass
    
    
        
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_price(self):
        return self.__price
    def get_category(self):
        return self.__category
    def get_stock(self):
        return self.__stock
    def get_size(self):
        return self.__size
    def get_colors(self):
        return self.__colors
    def get_description(self):
        return self.__description
    def get_image(self):
        return self.__image
    
    def set_name(self, name):
        self.__name = name
    def set_price(self, price):
        self.__price = price
    def set_category(self, category):
        self.__category = category
    def set_stock(self, stock):
        self.__stock = stock
    def set_size(self, size):
        self.__size = size
    def set_colors(self, colors):
        self.__colors = colors
    def set_description(self, description):
        self.__description = description
    def set_image(self, image):
        self.__image = image
