from wtforms import Form, StringField, PasswordField, validators, EmailField, DateField, IntegerField, DecimalField


class Login(Form):
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message="Enter valid name")])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class UpdateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message="Enter valid name")])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])


class ForgotPassword(Form):
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])


class PaymentDetails(Form):
    name_on_card = StringField('Name on Card', [validators.Length(min=1, max=150), validators.DataRequired()])
    card_number = IntegerField('Credit Card Number', [validators.NumberRange(min=1000000000000, max=9999999999999999999), validators.DataRequired()])
    cvv = IntegerField('CVV', [validators.NumberRange(min=100, max=9999), validators.DataRequired()])
    expiry = DateField('Expiry Date', [validators.DataRequired()])


class DeliveryDetails(Form):
    recipient_name = StringField('Recipient Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=3, max=150), validators.DataRequired()])
    unit_number = StringField('Unit Number', [validators.Length(min=1, max=7), validators.DataRequired()])
    postal_code = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()])
    phone_number = IntegerField('Phone Number', [validators.NumberRange(min=10000000, max=99999999), validators.DataRequired()])


class ResetPassword(Form):
    old_password = PasswordField('Old Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class CustomerDeleteAccount(Form):
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class OTP(Form):
    otp = IntegerField("OTP", [validators.NumberRange(min=100000, max=999999), validators.DataRequired()])


class FResetPassword(Form):
    new_password = PasswordField('New Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class Promocode(Form):
    promo_code = StringField("Promotion Code", [validators.Length(min=1, max=150), validators.DataRequired()])
    discount = DecimalField("Discount Amount (in Decimal)", [validators.NumberRange(min=0, max=1), validators.DataRequired()])
