from wtforms import Form, StringField, PasswordField, validators, EmailField, DateField, IntegerField


class PromoTrans(Form):
    pay_promo_code = StringField("Promo Code", [validators.Length(min=1, max=150), validators.DataRequired()])


