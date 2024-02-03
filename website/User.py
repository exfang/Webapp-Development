class User:
    count_id = 0

    def __init__(self, skye_first_name, skye_last_name, skye_RateProd, skye_RatePrice, skye_RateDel, skye_email, skye_remarks):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__skye_first_name = skye_first_name
        self.__skye_last_name = skye_last_name
        self.__skye_RateProd = skye_RateProd
        self.__skye_RatePrice = skye_RatePrice
        self.__skye_RateDel = skye_RateDel
        self.__skye_email = skye_email
        self.__skye_remarks = skye_remarks

    def get_user_id(self):
        return self.__user_id

    def get_skye_first_name(self):
        return self.__skye_first_name

    def get_skye_last_name(self):
        return self.__skye_last_name

    def get_skye_RateProd(self):
        return self.__skye_RateProd

    def get_skye_RatePrice(self):
        return self.__skye_RatePrice

    def get_skye_RateDel(self):
        return self.__skye_RateDel

    def get_skye_email(self):
        return self.__skye_email

    def get_skye_remarks(self):
        return self.__skye_remarks

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_skye_first_name(self, skye_first_name):
        self.__skye_first_name = skye_first_name

    def set_skye_last_name(self, skye_last_name):
        self.__skye_last_name = skye_last_name

    def set_skye_RateProd(self, skye_RateProd):
        self.__skye_RateProd = skye_RateProd

    def set_skye_RatePrice(self, skye_RatePrice):
        self.__skye_RatePrice = skye_RatePrice

    def set_skye_RateDel(self, skye_RateDel):
        self.__skye_RateDel = skye_RateDel

    def set_skye_email(self, skye_email):
        self.__skye_email = skye_email

    def set_skye_remarks(self, skye_remarks):
        self.__skye_remarks = skye_remarks




