from email.mime import image
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, FileField, IntegerField, DecimalField, validators
class AddProd(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = DecimalField('Product Price', [validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()], choices=[('', 'Select'), ('R', 'Regular'), ('K', 'Kids'), ('C', 'Customised')], default='R')
    stock = IntegerField('Stock', [validators.DataRequired()])
    size = SelectField('Size', [validators.DataRequired()], choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='M')
    colors = StringField('Colours', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    image = FileField('Image', [validators.DataRequired()])
