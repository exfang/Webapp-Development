from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators,PasswordField, ValidationError
#from wtforms.validators import InputRequired, Email
#from wtforms-html5 import EmailField

class CreateFeedbackForm(Form):
    skye_first_name = StringField(' First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    skye_last_name = StringField(' Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    skye_RateProd = RadioField(' How satisfied are you with our product? ', choices=[('VS', 'Very Satisfied'), ('S', 'Satisfied'), ('N', 'Neutral') ,('US', 'UnSatisfied'),('VUS', 'Very UnSatisfied') ], default='N')
    skye_RatePrice = RadioField(' How would you rate our prices? ', choices=[('VH', 'Very High'), ('H', 'High'), ('N', 'Neutral') ,('L', 'Low'),('VL', 'Very Low') ], default='N')
    skye_RateDel = RadioField(' How satisfied are you with our delivery? ', choices=[('VS', 'Very Satisfied'), ('S', 'Satisfied'), ('N', 'Neutral') ,('US', 'UnSatisfied'),('VUS', 'Very UnSatisfied') ], default='N')
    skye_email = StringField(' Email for contact', [validators.Length(min=9, max=150), validators.DataRequired()])
    skye_remarks = TextAreaField(' Is there anything you would like us to improve on?', [validators.Optional()])
