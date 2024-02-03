class Customer:
    customer_count_id = 0

    def __init__(self, first_name, last_name, email, password):
        Customer.customer_count_id += 1
        self.__user_id = Customer.customer_count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_user_id(self, user_id):
        self.__user_id = user_id


class Staff:
    staff_count_id = 0

    def __init__(self, first_name, last_name, email, password):
        Staff.staff_count_id += 1
        self.__user_id = Staff.staff_count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_user_id(self, user_id):
        self.__user_id = user_id


class Payment:
    def __init__(self, user_id, name_on_card, card_number, cvv, expiry):
        self.__user_id = user_id
        self.__name_on_card = name_on_card
        self.__card_number = card_number
        self.__cvv = cvv
        self.__expiry = expiry

    def get_user_id(self):
        return self.__user_id

    def get_name_on_card(self):
        return self.__name_on_card

    def get_card_number(self):
        return self.__card_number

    def get_cvv(self):
        return self.__cvv

    def get_expiry(self):
        return self.__expiry

    def set_name_on_card(self, name_on_card):
        self.__name_on_card = name_on_card

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_expiry(self, expiry):
        self.__expiry = expiry

    def set_user_id(self, user_id):
        self.__user_id = user_id


class Delivery:
    def __init__(self, user_id, recipient_name, address, unit_number, postal_code, phone_number):
        self.__user_id = user_id
        self.__recipient_name = recipient_name
        self.__address = address
        self.__unit_number = unit_number
        self.__postal_code = postal_code
        self.__phone_number = phone_number

    def get_user_id(self):
        return self.__user_id

    def get_recipient_name(self):
        return self.__recipient_name

    def get_address(self):
        return self.__address

    def get_unit_number(self):
        return self.__unit_number

    def get_postal_code(self):
        return self.__postal_code

    def get_phone_number(self):
        return self.__phone_number

    def set_recipient_name(self, recipient_name):
        self.__recipient_name = recipient_name

    def set_address(self, address):
        self.__address = address

    def set_unit_number(self, unit_number):
        self.__unit_number = unit_number

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number


class Promotion:
    promo_id = 0

    def __init__(self, promo_name, discount_amt):
        Promotion.promo_id += 1
        self.__promo_id = Promotion.promo_id
        self.__promo_name = promo_name
        self.__discount_amt = discount_amt

    def get_promo_id(self):
        return self.__promo_id

    def get_promo_name(self):
        return self.__promo_name

    def get_discount_amt(self):
        return self.__discount_amt

    def set_promo_id(self, promo_id):
        self.__promo_id = promo_id

    def set_promo_name(self, promo_name):
        self.__promo_name = promo_name

    def set_discount_amt(self, discount_amt):
        self.__discount_amt = discount_amt
