from operator import add
from re import U
from turtle import color, width
from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, Response
from pythonFiles.Forms import AddProd
from pythonFiles.User import User
from pythonFiles.Feedbackform import CreateFeedbackForm
import shelve
from pythonFiles import add_prod, add_user, id_generator
from pythonFiles.account_forms import CreateUserForm, UpdateUserForm, Login, ForgotPassword, PaymentDetails, \
    DeliveryDetails, ResetPassword, CustomerDeleteAccount, OTP, FResetPassword, Promocode
from random import *
from flask_mail import Mail, Message
from staff_accounts import staff_account
import datetime
from pythonFiles.transaction import transaction
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64
import plotly
import plotly.express as px


from pythonFiles.trans_form import PromoTrans


app = Flask(__name__)
app.secret_key = 'notsecret'
app.config["MAIL_SERVER"] ='smtp.gmail.com'
app.config["MAIL_PORT"] =465
app.config["MAIL_USERNAME"] ='hoopllab@gmail.com'
app.config['MAIL_PASSWORD'] ='pgiyaijuhqafkxhy' # Hoopllabpassw0rd Same for mail.com
app.config['MAIL_USE_TLS'] =False
app.config['MAIL_USE_SSL'] =True
mail=Mail(app)

# Used to store whether they logged in. If not logged in, the user field will be empty
user = []


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = session['user_id']


@app.route('/')
def home():
    # Create the staff account, only for testing.
    staff_account()
    if not user:
        session.clear()
        session['acc_type'] = "Guest"
    return render_template('home.html')


# Andrew
@app.route('/login', methods=['GET', 'POST'])  # follow the title here not the html title
def login():
    # start of shermaine's login counter dIE :)
    db = shelve.open('storage.db', 'c')

    login_counter = {}

    try:
        login_counter = db['login_counter']
    except:
        db['login_counter'] = login_counter
    # end of shermaine's login counter db dIE :)
    
    log_in = Login(request.form)
    if request.method == 'POST' and log_in.validate():
        session.clear() # Remove the user ID if there is 1 already in the session
        user.clear()
        db = shelve.open('storage.db', 'c')
        for j in db:
            if j == 'Customer' or j == 'Staff':
                for i in db[j]: # The i is the user's id.
                    if log_in.email.data == db[j][i].get_email() and log_in.password.data == db[j][i].get_password():
                        user.append('True')
                        session['user_id'] = i
                        session['acc_type'] = j
                        session['first_name'] = db[j][i].get_first_name()
                        session['last_name'] = db[j][i].get_last_name()
                        session['email'] = db[j][i].get_email()
                        session['password'] = db[j][i].get_password()
                        session['user_loggedin'] = f'{db[j][i].get_first_name()}'
                        if j == "Customer":
                            # counter for customer login report @andrew pls dont touch :) 
                            tdy_date = datetime.datetime.now().strftime("%d/%m/%Y")
                            #tdy_date = "09/08/2022"
                            try:
                                tdy_counter = len(login_counter[tdy_date])
                            except:
                                tdy_counter = 0
                            
                            if tdy_counter > 0:
                                login_counter[tdy_date].append(tdy_counter)
                            else: 
                                login_counter[tdy_date] = [tdy_counter]

                            db['login_counter'] = login_counter
                            db.close()
                            # end of counter for customer login report :)
                            return redirect(url_for('account_details'))
                        else:
                            return redirect(url_for('staff_report'))
                        # return render_template('./account/account_overview_base.html')
        flash("Email or password wrong. Please try again.")
    print(login_counter)
    key_list = list(login_counter.keys())
    print(key_list)
    return render_template('login.html', form=log_in)


# Andrew
@app.route('/account_detail', methods=['GET', 'POST'])
def account_details():
    account_detail = UpdateUserForm(request.form)
    if request.method == 'POST' and account_detail.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        if session['acc_type'] == "Customer":
            users_dict = db['Customer']
        elif session['acc_type'] == "Staff":
            users_dict = db['Staff']

        users = users_dict.get(session['user_id'])

        users.set_first_name(account_detail.first_name.data)
        users.set_last_name(account_detail.last_name.data)
        users.set_email(account_detail.email.data)
        if users.get_first_name() != session['first_name'] or users.get_last_name() != session['last_name'] \
                or users.get_email() != session['email']:
            session['first_name'] = users.get_first_name()
            session['last_name'] = users.get_last_name()
            session['email'] = users.get_email()
            session['user_updated'] = users.get_first_name() + ' ' + users.get_last_name()
            db[session['acc_type']] = users_dict
            db.close()
        return redirect(url_for('account_details'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        if session['acc_type'] == "Guest":
            return redirect(url_for('home'))
        else:
            if session['acc_type'] == "Customer":
                users_dict = db['Customer']
            elif session['acc_type'] == "Staff":
                users_dict = db['Staff']

            users = users_dict.get(session['user_id'])
            account_detail.first_name.data = users.get_first_name()
            account_detail.last_name.data = users.get_last_name()
            account_detail.email.data = users.get_email()

        return render_template('./account/account_detail.html', form=account_detail)


# Andrew
# Reset password within their account details
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_password_form = ResetPassword(request.form)
    if request.method == 'POST' and reset_password_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        if session['acc_type'] == "Customer":
            users_dict = db['Customer']
        elif session['acc_type'] == "Staff":
            users_dict = db['Staff']

        users = users_dict.get(session['user_id'])

        old_password = users.get_password()
        if reset_password_form.old_password.data != old_password:
            flash("Please enter your previous password.", "oldpassworderror")
        elif reset_password_form.new_password.data != reset_password_form.confirm_password.data:
            flash("Confirm password not the same as new password.", "confirmpassworderror")
            print("Wrong confirm")
        else:
            session['user_updated'] = users.get_first_name() + ' ' + users.get_last_name()+"'s password "
            users.set_password(reset_password_form.new_password.data)
            users_dict[session['user_id']] = users
            if session['acc_type'] == "Customer":
                db['Customer'] = users_dict
            else:
                db['Staff'] = users_dict
            db.close()

            return redirect(url_for('account_details'))

    return render_template('./account/reset_password.html', form=reset_password_form)


# Andrew
@app.route('/customer_delete_account', methods=['POST', 'GET'])
def delete_account():
    customer_delete_form = CustomerDeleteAccount(request.form)
    if request.method == 'POST' and customer_delete_form.validate():
        db = shelve.open('storage.db', 'w')
        if session['acc_type'] == "Customer":
            users_dict = db['Customer']
        else:
            users_dict = db['Staff']
        password = users_dict[session['user_id']].get_password()
        if customer_delete_form.confirm_password.data == customer_delete_form.password.data:
            if password == customer_delete_form.password.data:
                recipient_email = users_dict[session["user_id"]].get_email()
                otp = randint(100000, 999999)
                session['otp'] = otp
                msg = Message(subject="Hoop Llab Account Deletion Authentication OTP", sender="hoopllab@gmail.com",
                              recipients=[recipient_email])
                msg.body = "Dear Customer, please use the code:"+str(otp)+" for your email authentication. Thank you."
                session['reset'] = f'Code sent to {recipient_email}. Please enter the code for authentication.'
                mail.send(msg)
                return redirect(url_for('authentication_account'))

    return render_template('./account/delete_account.html', form=customer_delete_form)


# Andrew
@app.route('/authentication',  methods=['GET', 'POST'])
def authentication_account():
    otp_form = OTP(request.form)
    if request.method == 'POST' and otp_form.validate():
        if otp_form.otp.data == session['otp']:
            session.pop('otp')
            db = shelve.open('storage.db', 'w')
            if session['acc_type'] == "Customer":
                users_dict = db['Customer']
            else:
                users_dict = db['Staff']

            users_dict.pop(session['user_id'])
            if session['acc_type'] == "Customer":
                db['Customer'] = users_dict
            else:
                db['Staff'] = users_dict
            payments_dict = db['Payments']
            delivery_dict = db['Delivery']
            if session['acc_type'] == "Customer":
                for j in db:
                    if j == "Payments" or j == "Delivery":
                        for i in db[j]:
                            if db[j][i].get_user_id() == session['user_id']:
                                if j == "Payments":
                                    payments_dict.pop(i)
                                else:
                                    delivery_dict.pop(i)
                db['Payments'] = payments_dict
                db['Delivery'] = delivery_dict

            if session['acc_type'] == "Customer":
                db['Customer'] = users_dict
            else:
                db['Staff'] = users_dict
            db.close()
            return redirect(url_for('logout'))
        else:
            flash("Wrong OTP entered. Please enter again.")
    return render_template('./account/accounts_otp.html', form=otp_form)


# Andrew
@app.route('/deleteAccounts')
def retrieve_users():
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        users_dict = db['Customer']
    except:
        print("None")
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('./account/staff_delete_account.html', count=len(users_list), users_list=users_list)


@app.route('/CustomerDeleteDelivery/<int:id>', methods=['POST'])
def CustomerDeleteDelivery(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    delivery_dict = db['Delivery']
    # Their user id is the same as their id in the dictionary, therefore can just pop directly.
    ids = []
    for i in delivery_dict:
        ids.append(i)

    if id in ids:
        delivery_dict.pop(id)
        db['Delivery'] = delivery_dict
        session['user_updated'] = "Delivery Details Deleted"
        db.close()
    else:
        session['user_updated'] = "Nothing deleted"

    return redirect(url_for('delivery_details'))


@app.route('/CustomerDeletePayment/<int:id>', methods=['POST'])
def CustomerDeletePayment(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    payment_dict = db['Payments']
    # Their user id is the same as their id in the dictionary, therefore can just pop directly.
    ids = []
    for i in payment_dict:
        ids.append(i)

    if id in ids:
        payment_dict.pop(id)
        db['Payments'] = payment_dict
        session['user_updated'] = "Payment Details Deleted"
        db.close()
    else:
        session['user_updated'] = "Nothing deleted"

    return redirect(url_for('payment_details'))


@app.route('/StaffDeleteUser/<int:id>', methods=['POST'])
def StaffDeleteAccounts(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Customer']
    payments_dict = db['Payments']
    delivery_dict = db['Delivery']

    # Their user id is the same as their id in the dictionary, therefore can just pop directly.
    users_dict.pop(id)

    # Since payments and delivery is not necessary, it is not in order customer registration.
    # Therefore, need to get the user_ids in the dictionaries to delete their details.
    for j in db:
        if j == "Payments" or j == "Delivery":
            for i in db[j]:
                if db[j][i].get_user_id() == id:
                    if j == "Payments":
                        payments_dict.pop(i)
                    elif j == "Delivery":
                        delivery_dict.pop(i)

    db['Customer'] = users_dict
    db['Payments'] = payments_dict
    db['Delivery'] = delivery_dict
    db.close()

    return redirect(url_for('retrieve_users'))


# Andrew
@app.route('/payment_detail', methods=['GET', 'POST'])
def payment_details():
    payment_detail_form = PaymentDetails(request.form)
    if request.method == 'POST' and payment_detail_form.validate():
        payment_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            payment_dict = db['Payments']
        except:
            print("First entry")
            # Check if the expiry is empty
        if payment_detail_form.expiry.data < datetime.date.today():
            flash(f"Changes not updated. Please enter an expiry date that is after {datetime.date.today()}.")
            return redirect(url_for('payment_details'))
        else:
            counter = 0
            for i in payment_dict:
                if session['user_id'] == i:
                    counter += 1
                    if payment_dict[i].get_name_on_card() != payment_detail_form.name_on_card.data or payment_dict[
                        i].get_card_number() != payment_detail_form.card_number.data or payment_dict[
                        i].get_cvv() != payment_detail_form.cvv.data or payment_dict[
                        i].get_expiry() != payment_detail_form.expiry.data:
                        session['user_updated'] = "Payment Details updated."

            if counter == 0:
                session['user_updated'] = "Payment Details updated."

            payment = add_user.Payment(session['user_id'], payment_detail_form.name_on_card.data,
                                       payment_detail_form.card_number.data, payment_detail_form.cvv.data,
                                       payment_detail_form.expiry.data)

            payment_dict[session['user_id']] = payment
            db['Payments'] = payment_dict
            db.close()
        return redirect(url_for('payment_details'))
    else:
        db = shelve.open('storage.db', 'r')
        if session['acc_type'] == "Guest":
            return redirect(url_for('home'))
        else:
            if session['acc_type'] == "Customer" or session['acc_type'] == "Staff":
                try:
                    payment_dict = db['Payments']
                    payment = payment_dict.get(session['user_id'])
                    payment_detail_form.name_on_card.data = payment.get_name_on_card()
                    payment_detail_form.card_number.data = payment.get_card_number()
                    payment_detail_form.cvv.data = payment.get_cvv()
                    payment_detail_form.expiry.data = payment.get_expiry()
                except:
                    print("Payments empty")

        return render_template('./account/payment_details.html', form=payment_detail_form)


# Andrew
@app.route('/delivery_detail', methods=['GET', 'POST'])
def delivery_details():
    delivery_detail_form = DeliveryDetails(request.form)
    if request.method == 'POST' and delivery_detail_form.validate():
        delivery_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            delivery_dict = db['Delivery']
        except:
            print("First entry")
            # Check if the expiry is empty

        counter = 0
        for i in delivery_dict:
            if session['user_id'] == i:
                counter += 1
                if delivery_dict[i].get_recipient_name() != delivery_detail_form.recipient_name.data or delivery_dict[
                    i].get_address() != delivery_detail_form.address.data or delivery_dict[
                    i].get_unit_number() != delivery_detail_form.unit_number.data or delivery_dict[
                    i].get_postal_code() != delivery_detail_form.postal_code.data or delivery_dict[
                    i].get_phone_number() != delivery_detail_form.phone_number.data:
                    session['user_updated'] = "Delivery Details updated."

        if counter == 0:
            session['user_updated'] = "Delivery Details updated."

        delivery = add_user.Delivery(session['user_id'], delivery_detail_form.recipient_name.data,
                                     delivery_detail_form.address.data, delivery_detail_form.unit_number.data,
                                     delivery_detail_form.postal_code.data, delivery_detail_form.phone_number.data)

        delivery_dict[session['user_id']] = delivery
        db['Delivery'] = delivery_dict
        db.close()
        return redirect(url_for('delivery_details'))
    else:
        db = shelve.open('storage.db', 'r')
        if session['acc_type'] == "Guest":
            return redirect(url_for('home'))
        else:
            if session['acc_type'] == "Customer" or session['acc_type'] == "Staff":
                try:
                    delivery_dict = db['Delivery']
                    delivery_person = delivery_dict.get(session['user_id'])
                    delivery_detail_form.recipient_name.data = delivery_person.get_recipient_name()
                    delivery_detail_form.address.data = delivery_person.get_address()
                    delivery_detail_form.unit_number.data = delivery_person.get_unit_number()
                    delivery_detail_form.postal_code.data = delivery_person.get_postal_code()
                    delivery_detail_form.phone_number.data = delivery_person.get_phone_number()
                except:
                    print("Delivery empty")

        return render_template('./account/delivery_details.html', form=delivery_detail_form)


# Andrew
@app.route('/logout')
def logout():
    session.clear()
    session['acc_type'] = "Guest"
    return redirect(url_for('home'))


# Andrew
@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        if create_user_form.confirm_password.data == create_user_form.password.data:
            customer_dict = {}
            db = shelve.open('storage.db', 'c')
            try:
                customer_dict = db['Customer']
            except:
                print("Error in retrieving Users from storage.db.")
            for i in customer_dict:
                if create_user_form.email.data == customer_dict[i].get_email():
                    flash('Email address exists. Please ', 'emailexists')
                    return redirect(url_for('sign_up'))

            customer = add_user.Customer(create_user_form.first_name.data, create_user_form.last_name.data,
                                         create_user_form.email.data, create_user_form.password.data)
            customer_id = customer.get_user_id()
            # Checking if ID exists. If exists, increment it until the ID is a new and unique value.
            while True:
                for i in customer_dict:
                    if customer_id == customer_dict[i].get_user_id():
                        customer_id += 1
                break
            customer.set_user_id(customer_id)
            customer_dict[customer_id] = customer
            db['Customer'] = customer_dict
            db.close()
            session['reset'] = 'Account created successfully! Please login to test your credentials.'
            return redirect(url_for('login'))

        else:
            flash('Password not the same. Please try again.', 'confirmpassword')
    return render_template('signup.html', form=create_user_form)


# Andrew
@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    forgot_password_form = ForgotPassword(request.form)
    if request.method == 'POST' and forgot_password_form.validate():
        db = shelve.open('storage.db', 'r')
        for j in db:
            if j == 'Customer' or j == 'Staff':
                for i in db[j]: # The i is the user's id.
                    if forgot_password_form.email.data == db[j][i].get_email():
                        session['forgot_email'] = forgot_password_form.email.data
                        session['forgot_password_allowed'] = True
                        otp = randint(100000, 999999)
                        session['otp'] = otp
                        msg = Message(subject="Hoop Llab Forgot Password OTP", sender="hoopllab@gmail.com", recipients=[db[j][i].get_email()])
                        msg.body = "Dear Customer, please use the code:"+str(otp)+" for your email authentication. Thank you."
                        session['reset'] = f'Code sent to {forgot_password_form.email.data}. Please enter the code for authentication.'
                        mail.send(msg)
                        return redirect(url_for('otp_code'))
        else:
            flash('Email does not exist. Note: Capitals are important')
    return render_template('./account/forgotpassword.html', form=forgot_password_form)


# Andrew
@app.route('/otp-code', methods=['GET', 'POST'])
def otp_code():
    otp_form = OTP(request.form)
    if request.method == 'POST' and otp_form.validate():
        if otp_form.otp.data == session['otp']:
            session.pop('otp')
            session['reset'] = 'Authentication Successful!'
            return redirect(url_for('reset_forgot_password'))
        else:
            flash("Wrong OTP entered. Please enter again.")
    return render_template('./account/reset_otp.html', form=otp_form)


# Andrew
@app.route('/reset-forgot-password', methods=['GET', 'POST'])
def reset_forgot_password():
    reset_password_form = FResetPassword(request.form)
    if request.method == 'POST' and reset_password_form.validate():
        db = shelve.open('storage.db', 'w')

        for j in db:
            if j == "Customer" or j == "Staff":
                for i in db[j]:
                    if db[j][i].get_email() == session['forgot_email']:
                        user_dict = db[j]
                        user_id = i

                        if reset_password_form.new_password.data != reset_password_form.confirm_password.data:
                            flash("Please enter the same password as your new password.", "confirmpassworderror")
                        else:
                            user_dict[user_id].set_password(reset_password_form.new_password.data)
                            if j == "Customer":
                                db['Customer'] = user_dict
                            else:
                                db['Staff'] = user_dict

                            session.pop('forgot_email')
                            db.close()
                            session['reset'] = 'Password changed successfully! Please login.'
                            session.pop('forgot_password_allowed')
                            return redirect(url_for('login'))

    return render_template('./account/fr_password.html', form=reset_password_form)


# Andrew
@app.route("/add_promocode", methods=['GET', 'POST'])
def promo_code():
    promo_code_form = Promocode(request.form)
    if request.method == 'POST' and promo_code_form.validate():
        db = shelve.open('storage.db', 'w')
        promotion_codes = {}
        try:
            promotion_codes = db['Promotion_Codes']
        except:
            print("New entry")

        promotion = add_user.Promotion(promo_code_form.promo_code.data, promo_code_form.discount.data)
        promotion_id = promotion.get_promo_id()
        # Checking if ID exists. If exists, increment it until the ID is a new and unique value.
        while True:
            for i in promotion_codes:
                if promotion_id == promotion_codes[i].get_promo_id():
                    promotion_id += 1
            break

        promotion.set_promo_id(promotion_id)
        promotion_codes[promotion_id] = promotion
        db['Promotion_Codes'] = promotion_codes
        session['promotion_added'] = f"Promotion Code {promotion.get_promo_name()} has been added"
        db.close()
        return redirect(url_for('promo_code'))

    return render_template("./account/promo_code.html", form = promo_code_form)


@app.route("/staff-home")
def staff_home():
    if session['acc_type'] == "Staff":
        return render_template("staff_base.html")
    else:
        return redirect(url_for('login'))


@app.route("/guest-home")
def guest_home():
    if session['acc_type'] == "Customer":
        return render_template("guest_base.html")
    else:
        return redirect(url_for('login'))

#start of product pages

#start of product pages - shermaine
@app.route('/Add-Product', methods=['GET', 'POST'])
def add_products():
    if session['acc_type'] == "Staff":
        add_prodform = AddProd(request.form)
        if request.method == 'POST' and add_prodform.validate():
            prod_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                prod_dict = db['Products']
            except:
                print("Error in retrieving Products from storage.db.")

            # Check if product ID exists & get lastest id
            prod_id = id_generator.Generator() # Generate a new ID - old version pls dont copy this, use the one i created in dummy database if u need  :) 
            id = prod_id.checkID()
            print(id)
            

            product = add_prod.Add_Prod(id, add_prodform.name.data, add_prodform.price.data, add_prodform.category.data, add_prodform.stock.data, add_prodform.size.data, add_prodform.colors.data, add_prodform.description.data, add_prodform.image.data)
            prod_dict[product.get_id()] = product
            db['Products'] = prod_dict
            print("Product ID=", product.get_id(), " with the details", product.get_image())
            db.close()

            return redirect(url_for('update'))
    else:
        return redirect(url_for('home'))
    return render_template('./products/addprod.html', form=add_prodform)


@app.route ('/EditProduct', methods=['GET', 'POST'])
def update():
    if session['acc_type'] == "Staff":
        prod_dict = {}
        db = shelve.open('storage.db', 'r')
        prod_dict = db['Products']
        db.close()

        #storing all the products in a list, to be displayed in table
        products_list = []
        for key in prod_dict:
            product = prod_dict.get(key)
            products_list.append(product)
    else:
        return redirect(url_for('home'))
    return render_template('./products/rmvupdate_prod.html', count=len(products_list), products_list= products_list)

@app.route ('/UpdateProduct/<int:id>/', methods=['GET', 'POST']) #<int:id> is the id of the product to be updated
def update_prod(id):
    if session['acc_type'] == "Staff":
        update_prod_form = AddProd(request.form)
        if request.method == 'POST' and update_prod_form.validate():
            prod_dict = {}
            db = shelve.open('storage.db', 'w')
            prod_dict = db['Products']
            product = prod_dict.get(id)
            product.set_name(update_prod_form.name.data)
            product.set_price(update_prod_form.price.data)
            product.set_category(update_prod_form.category.data)
            product.set_stock(update_prod_form.stock.data)
            product.set_size(update_prod_form.size.data)
            product.set_colors(update_prod_form.colors.data)
            product.set_description(update_prod_form.description.data)
            product.set_image(update_prod_form.image.data)

            db['Products'] = prod_dict
            db.close()
            return redirect(url_for('update'))
        else:
            prod_dict = {}
            db = shelve.open('storage.db', 'r')
            prod_dict = db['Products']
            db.close()

            product = prod_dict.get(id)
            update_prod_form.name.data = product.get_name()
            update_prod_form.price.data = product.get_price()
            update_prod_form.category.data = product.get_category()
            update_prod_form.stock.data = product.get_stock()
            update_prod_form.size.data = product.get_size()
            update_prod_form.colors.data = product.get_colors()
            update_prod_form.description.data = product.get_description()
            update_prod_form.image.data = product.get_image()

            return render_template('./products/updateprod.html', form = update_prod_form, user = "Staff")
    else:
        return redirect(url_for('home'))

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    prod_dict = {}
    db = shelve.open('storage.db', 'w')
    prod_dict = db['Products']
    prod_dict.pop(id)
    db['Products'] = prod_dict
    db.close()
    return redirect(url_for('update'))

@app.route('/View-CustomProducts') #view all custom products, if else statement in html 
def view_custom_products():
    if session['acc_type'] == "Customer" or session['acc_type'] == "Guest":
        prod_dict = {}
        db = shelve.open('storage.db', 'r')
        prod_dict = db['Products']
        db.close()

        products_list = []
        img_list = []
        for key in prod_dict:
            product = prod_dict.get(key)
            products_list.append(product)
        img = product.get_image()
        return render_template("./products/custom.html", products_list = products_list, img=img)
    else:
        return redirect(url_for('home'))

@app.route('/View-RegularProducts') #view all regular products, if else statement in html
def view_regular_products():
    if session['acc_type'] == "Customer" or session['acc_type'] == "Guest":
        prod_dict = {}
        db = shelve.open('storage.db', 'r')
        prod_dict = db['Products']
        db.close()

        products_list = []
        img_list = []
        for key in prod_dict:
            product = prod_dict.get(key)
            products_list.append(product)
            img = product.get_image()
            img_list.append(img)
        print("image = ", img)
        return render_template("./products/regular.html", products_list = products_list, img=img_list)
    else:
        return redirect(url_for('home'))

@app.route('/View-KidsProducts') #view all kids products, if else statement in html
def view_kids_products():
    if session['acc_type'] == "Customer" or session['acc_type'] == "Guest":
        prod_dict = {}
        db = shelve.open('storage.db', 'r')
        prod_dict = db['Products']
        db.close()

        products_list = []
        img_list = []
        for key in prod_dict:
            product = prod_dict.get(key)
            products_list.append(product)
            img = product.get_image()
            img_list.append(img)
        return render_template("./products/kids.html", products_list = products_list, img=img_list)
    else:
        return redirect(url_for('home'))


@app.route('/Product-Details/<int:prodID>') #view product details, based on id clicked on, store img in file format !!!
def product_details(prodID:int):
    if session['acc_type'] == "Customer" or session['acc_type'] == "Guest":
        db = shelve.open('storage.db', 'r')
        prod_dict = db['Products']
        db.close()
        print(prodID)
        colorslist = []
        product = prod_dict.get(prodID)
        colors = product.get_colors()
        print(product.get_colors())
        splitcolors = colors.split(',')
        for x in splitcolors:
            colorslist.append(x)

        products_list = []
        img_list = []
        for key in prod_dict:
            product_slide = prod_dict.get(key)
            products_list.append(product_slide)
            img = product_slide.get_image()
            img_list.append(img)

        return render_template("./products/product_details.html", product = product, colorslist = colorslist, products_list = products_list, img=img_list)
    else:
        return redirect(url_for('home'))
#end of products pages

# Fixed 5-8
@app.route('/addcart/<int:prodID>', methods=["POST"])
def get_id(prodID:int):
    prod_dict = {}
    db = shelve.open('storage.db', 'r')
    prod_dict = db['Products']
    db.close()

    cart_list = []
    product = prod_dict.get(prodID)
    cart_list.append(product)

    cart_dict = {}
    db = shelve.open('storage.db', 'w')
    try:
        cart_dict = db['carts']
    except:
        print("Error in retrieving Products from storage.db.")

    countofcart_dict = []
    for j in cart_dict:
        countofcart_dict.append(j)

    cart_dict[(len(countofcart_dict))] = product
    db['carts'] = cart_dict

    return redirect(url_for('product_details', prodID=prodID))


# Akira
@app.route('/cartlist', methods=["GET"])
def add_to_cart():
    cart_dict = {}
    db = shelve.open('storage.db', 'r')
    cart_dict = db['carts']
    db.close()
    if session['acc_type'] == "Customer":
        if cart_dict:
            cart_list = []
            # Iterate through the art_dict, i is the item_cart_id
            for i in cart_dict:
                # iterate through the cart_dict, append the product details
                item = cart_dict.get(i)
                cart_list.append(item)

            totalamt_list = []
            for item in cart_list:
                cost = item.get_price()
                totalamt_list.append(cost)
        else:
            cart_list = []
            totalamt_list = []
    else:
        return redirect(url_for('home'))

    return render_template("./transactions/cart.html", cart_list=cart_list, count=len(cart_list),
                           total=sum(totalamt_list))


# Akira
@app.route('/cart_payment', methods=['GET', 'POST'])
def cart_payment_details():
    delivery_detail_form = DeliveryDetails(request.form)
    if session['acc_type'] == "Customer":
        if request.method == 'POST' and delivery_detail_form.validate():
            delivery_dict = {}
            db = shelve.open('storage.db', 'w')
            try:
                delivery_dict = db['Delivery']
            except:
                print("First entry")
                # Check if the expiry is empty

            counter = 0
            for i in delivery_dict:
                if session['user_id'] == i:
                    counter += 1
                    if delivery_dict[i].get_recipient_name() != delivery_detail_form.recipient_name.data or delivery_dict[
                        i].get_address() != delivery_detail_form.address.data or delivery_dict[
                        i].get_unit_number() != delivery_detail_form.unit_number.data or delivery_dict[
                        i].get_postal_code() != delivery_detail_form.postal_code.data or delivery_dict[
                        i].get_phone_number() != delivery_detail_form.phone_number.data:
                        session['user_updated'] = "Delivery Details updated."

            if counter == 0:
                session['user_updated'] = "Delivery Details updated."

            delivery = add_user.Delivery(session['user_id'], delivery_detail_form.recipient_name.data,
                                         delivery_detail_form.address.data, delivery_detail_form.unit_number.data,
                                         delivery_detail_form.postal_code.data, delivery_detail_form.phone_number.data)

            delivery_dict[session['user_id']] = delivery
            db['Delivery'] = delivery_dict
            db.close()
            return redirect(url_for('credit_details'))
        else:
            db = shelve.open('storage.db', 'r')
            if session['acc_type'] == "Guest":
                return redirect(url_for('home'))
            else:
                if session['acc_type'] == "Customer" or session['acc_type'] == "Staff":
                    try:
                        delivery_dict = db['Delivery']
                        delivery_person = delivery_dict.get(session['user_id'])
                        delivery_detail_form.recipient_name.data = delivery_person.get_recipient_name()
                        delivery_detail_form.address.data = delivery_person.get_address()
                        delivery_detail_form.unit_number.data = delivery_person.get_unit_number()
                        delivery_detail_form.postal_code.data = delivery_person.get_postal_code()
                        delivery_detail_form.phone_number.data = delivery_person.get_phone_number()
                    except:
                        print("Delivery empty")
    else:
        return redirect(url_for('home'))

    return render_template('./transactions/payment_detail..html', form=delivery_detail_form)


@app.route('/credit_details', methods=['GET', 'POST'])
def credit_details():
    payment_detail_form = PaymentDetails(request.form)
    if session['acc_type'] == "Customer":
        if request.method == 'POST' and payment_detail_form.validate():
            payment_dict = {}
            db = shelve.open('storage.db', 'w')
            try:
                payment_dict = db['Payments']
            except:
                print("First entry")

            counter = 0
            for i in payment_dict:
                if session['user_id'] == i:
                    counter += 1
                    if payment_dict[i].get_name_on_card() != payment_detail_form.name_on_card.data or payment_dict[
                        i].get_card_number() != payment_detail_form.card_number.data or payment_dict[
                        i].get_cvv() != payment_detail_form.cvv.data or payment_dict[
                        i].get_expiry() != payment_detail_form.expiry.data:
                        session['user_updated'] = "Payment Details updated."

            if counter == 0:
                session['user_updated'] = "Payment Details updated."

            payment = add_user.Payment(session['user_id'], payment_detail_form.name_on_card.data,
                                        payment_detail_form.card_number.data, payment_detail_form.cvv.data,
                                        payment_detail_form.expiry.data)

            payment_dict[session['user_id']] = payment
            db['Payments'] = payment_dict
            db.close()

            return redirect(url_for('payment'))
        else:
            db = shelve.open('storage.db', 'r')
            if session['acc_type'] == "Guest":
                return redirect(url_for('home'))
            else:
                if session['acc_type'] == "Customer" or session['acc_type'] == "Staff":
                    try:
                        payment_dict = db['Payments']
                        payment = payment_dict.get(session['user_id'])
                        payment_detail_form.name_on_card.data = payment.get_name_on_card()
                        payment_detail_form.card_number.data = payment.get_card_number()
                        payment_detail_form.cvv.data = payment.get_cvv()
                        payment_detail_form.expiry.data = payment.get_expiry()
                    except:
                        print("Payments empty")
    else:
        return redirect(url_for('home'))
    return render_template('./transactions/creditcard_detail.html', form=payment_detail_form)


# Akira
@app.route('/payment', methods = ['GET','POST'])
def payment():
    promo_veri_form = PromoTrans(request.form)
    if session['acc_type'] == "Customer":
        if request.method == 'POST' and promo_veri_form.validate():
            promo_dict = {}
            db = shelve.open('storage.db', 'r')

            try:
                promo_dict = db['Promotion_Codes']
            except:
                print("Error in retrieving Promo from storage.db")
            db.close()
            code_entered = promo_veri_form.pay_promo_code.data
            print(code_entered)
            promo_id = []
            for i in promo_dict:
                id = promo_dict[i].get_promo_id()
                promo_id.append(id)

            for id in promo_id:
                if promo_dict[id].get_promo_name() == code_entered:

                    print("promo code valid")
                    cart_dict = {}
                    db = shelve.open('storage.db', 'r')
                    cart_dict = db['carts']
                    db.close()

                    cart_list = []
                    for i in cart_dict:
                        item = cart_dict.get(i)
                        cart_list.append(item)

                    totalamt_list = []
                    for item in cart_list:
                        cost = item.get_price()
                        totalamt_list.append(cost)
                    discount = promo_dict[id].get_discount_amt()
                    shipping = 10
                    tax = 10
                    totaltotal = (sum(totalamt_list) + shipping + tax) * (1-discount)

                    return render_template("./transactions/payment.html", cart_list=cart_list,total = sum(totalamt_list), totaltotal=totaltotal, shipping=shipping, tax=tax, form = promo_veri_form)
                else:
                    print("promo invalid")
                    cart_dict = {}
                    db = shelve.open('storage.db', 'r')
                    cart_dict = db['carts']
                    db.close()

                    cart_list = []
                    for i in cart_dict:
                        item = cart_dict.get(i)
                        cart_list.append(item)

                    totalamt_list = []
                    for item in cart_list:
                        cost = item.get_price()
                        totalamt_list.append(cost)
                    discount = promo_dict[id].get_discount_amt()
                    shipping = 10
                    tax = 10
                    totaltotal = (sum(totalamt_list) + shipping + tax) * (1-discount)

                    shipping = 10
                    tax = 10
                    totaltotal = sum(totalamt_list) + shipping + tax

                    return render_template("./transactions/payment.html", cart_list=cart_list,total = sum(totalamt_list), totaltotal=totaltotal, shipping=shipping, tax=tax, form = promo_veri_form)


        else:
            print("promo invalid")
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['carts']
            db.close()

            cart_list = []
            for i in cart_dict:
                item = cart_dict.get(i)
                cart_list.append(item)

            totalamt_list = []
            for item in cart_list:
                cost = item.get_price()
                totalamt_list.append(cost)

            shipping = 10
            tax = 10
            totaltotal = sum(totalamt_list) + shipping + tax

            return render_template("./transactions/payment.html", cart_list=cart_list,total = sum(totalamt_list), totaltotal=totaltotal, shipping=shipping, tax=tax, form = promo_veri_form)

    else:
        return redirect(url_for('home'))


# Akira
@app.route('/delete_item/<int:itemid>', methods=['POST'])
def delete_item(itemid:int):
    cart_dict = {}
    db = shelve.open('storage.db', 'w')
    cart_dict = db['carts']

    for i in cart_dict:
        if cart_dict[i].get_id() == itemid:
            delete = i
        else:
            break

    cart_dict.pop(delete)
    db['carts'] = cart_dict

    db.close()

    return redirect(url_for('add_to_cart'))


# Akira
@app.route('/add_trans/<int:total>', methods=["POST"])
def add_trans(total):
    if session['acc_type'] == "Customer":
        cart_dict = {}
        db = shelve.open('storage.db', 'r')
        cart_dict = db['carts']
        db.close()

        cart_item_names = []
        for i in cart_dict:
            item_id = cart_dict[i].get_name()
            cart_item_names.append(item_id)

        x = datetime.datetime.now()
        trans_date = (x.strftime("%x"))

        trans_dict = {}
        cart_dict = {}
        db = shelve.open('storage.db','c')
        try:
            cart_dict = db['carts']
            trans_dict = db['Transaction']
        except:
            print("Error in retrieving Products from storage.db.")
        id = len(trans_dict)
        print(id)
        print(trans_dict)
        trans = transaction(id, cart_item_names, total, trans_date, session['user_id'])
        trans_dict[trans.get_trans_id()] = trans
        db['Transaction'] = trans_dict

        cart_dict.clear()
        db['carts'] = cart_dict

        db.close()

        return render_template('./transactions/confirmation.html', date_today = trans_date)
    else:
        return redirect(url_for('home'))


#start of report pages - shermaine
@app.route('/cust_report')
def cust_report(): 
    if session['acc_type'] == "Customer":
        prod_dict = {}
        trans_dict = {} # create database 
        db = shelve.open('storage.db', writeback=True)
        try:
            prod_dict = db['Products'] #get product details 
        
        # dummy database 
            trans_dict = db['Transaction']
        except:
                print("Error in retrieving Products from storage.db.")
        print(dict(trans_dict))
        id = len(trans_dict) # generate id 
        print(id)
        
        # dumb & dumber :) ☠️
        # STORE BY PROD NAME - TO MATCH AKIRA'S DB 
        #trans = transaction(id, [1, 2], 123, '03/08/2022', 1 ) #write dummy data into file - dont use
        #trans = transaction(id, [1, 2], 10, '04/08/2022', 2 ) - dont use!!
        #trans = transaction(id, ['Test23', 'Dassdj1'], 10, '06-08-2022', 2 )
        #trans = transaction(id, ['test23','xgchvjk'], 10, '06-08-2022', 1 )
        #trans = transaction(id, ['test23'], 10, '06/06/2022', 1 )
        #trans = transaction(id, ['test23'], 100, '12/05/2022', 3 )
        #trans = transaction(id, ['Dassdj1'], 20, '07-08-2022', 1 )
        #trans_dict[trans.get_trans_id()] = trans
        #print("transaction written", trans)
        db['Transaction'] = trans_dict # storing details 
        # print(trans_dict)
        # print(len(trans_dict))
        db.close()
        
        user_trans = []
        for transactions in trans_dict:
            user_tran = trans_dict[transactions].get_user_id()
            user_trans.append(user_tran)
            
        if session['user_id'] not in user_trans:
            print("no data")
            return render_template('./reports/no_trans.html')
        
        else:
            prods_bought = []
            Rcat = []
            Ccat = []
            Kcat = []
            total = []   # get total sales & total trans by user id 
            prod_bought = []
            dates = []
            for transactions in trans_dict:
                #print(transactions)
                if trans_dict[transactions].get_user_id() == session['user_id']:
                    total.append(trans_dict[transactions].get_amount_spent())
                    dates.append(trans_dict[transactions].get_trans_date())
                    prod_bought = trans_dict[transactions].get_items_bought()
                    for x in prod_bought:
                        prods_bought.append(x)
                
            df_date = pd.DataFrame({'dates': dates, 'amount': total})
            df_date[["day", "month", "year"]] = df_date["dates"].str.split("/", expand = True)
            month_spend = df_date.groupby(["month"], as_index=False)["amount"].sum()
            date_list = month_spend['month'].tolist()
            amount_list = month_spend['amount'].tolist()
            plt.plot(date_list, amount_list, color = 'black')
            plt.xlabel('Month')
            plt.ylabel('Amount Spent')
            ax = plt.gca()
            ax.set(facecolor = "#ffc397") #change background color
            #remove borders
            ax.spines['top'].set_visible(False) 
            ax.spines['right'].set_visible(False)
            fig = ax.get_figure() #get figure
            #change face's background color
            fig.patch.set_facecolor('#ffc397')
            img = BytesIO() #create buffer to store image
            plt.savefig(img, format='png', bbox_inches='tight') #save image and ensure NO CUTOFF
            plt.close() #close/ end figure
            img.seek(0) #reset buffer to start
            plot_month_spend = base64.b64encode(img.getvalue()).decode('utf8')
            # print(date_list)
            # print(amount_list)
            # print(month_spend)
            # print(df_date)
            
            print(prods_bought)
            print(dates) 
            prod_cat = []
            for name in prods_bought:
                for key in prod_dict:
                    prod = prod_dict[key]
                    if prod.get_name() == name:
                        prod_cat.append(prod.get_category())
                    else:
                        pass
            print(prod_cat)
            for i in prod_cat:
                if i == 'R':
                    Rcat.append(i)
                elif i == 'C':
                    Ccat.append(i)
                elif i == 'K':
                    Kcat.append(i)
            # print(Rcat)
            # print(Ccat)
            # print(Kcat)
            if len(Ccat) > len(Rcat) and len(Ccat) > len(Kcat): # get most popular category
                topcat = "Customised"
            elif len(Rcat) > len(Ccat) and len(Rcat) > len(Kcat): 
                topcat = "Regular"
            else:
                topcat = "Kids"
                        
            return render_template('./reports/cust-dash.html', total_spent = sum(total), total_trans = len(total), topcat = topcat, plot_month_spend = plot_month_spend)    
    else:
        return redirect(url_for('home'))

@app.route('/cust_trans')
def cust_trans():
    if session['acc_type'] == "Customer":
        trans_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            trans_dict = db['Transaction']
        except: 
            print("no data")
        db.close()
        
        user_trans = []
        for transactions in trans_dict:
            user_tran = trans_dict[transactions].get_user_id()
            user_trans.append(user_tran)
            
        if session['user_id'] not in user_trans:

            print("no data")
            return render_template('./reports/no_trans.html')
        
        else:
        
            transaction_list = [] #loop to get ALL transactions by logged in user id 
            for transactions in trans_dict:
                if trans_dict[transactions].get_user_id() == session['user_id']:
                    trans = trans_dict.get(transactions)
                    transaction_list.append(trans)
            return render_template('./reports/cust-trans.html', transaction_list = transaction_list)   

        # user_trans = []
        # for transactions in trans_dict:
        # #     user_tran = trans_dict[transactions].get_user_id()
        # #     user_trans.append(user_tran)
            
        # # if session['user_id'] not in user_trans:

        # #     print("no data")
        # #     return render_template('./reports/no_trans.html')
        
        # # else:
        #     transaction_list = [] #loop to get ALL transactions by logged in user id 
        #     # for transactions in trans_dict:
        #     if trans_dict[transactions].get_user_id() == session['user_id']:
        #         trans = trans_dict.get(transactions)
        #         transaction_list.append(trans)
        #         return render_template('./reports/cust-trans.html', transaction_list = transaction_list)
                    
        # #         else:
        # #             print("no data")
        # #             return render_template('./reports/no_trans.html')
    else:
        return redirect(url_for('home'))
            
   

@app.route('/staff_report')
def staff_report():
    if session['acc_type'] == "Staff":
        cust_dict = {}
        trans_dict = {}
        login_counter = {}
        db = shelve.open('storage.db', 'w')#read both customer & transaction files 
    
        cust_dict = db['Customer']
        print(cust_dict)
        trans_dict = db['Transaction']
        login_counter = db['login_counter']

        cust_list = []  # get total sign ups
        for customers in cust_dict:
            cust_list.append(customers)

        total = []  # get total transactions & sales
        for transactions in trans_dict:
            total.append(trans_dict[transactions].get_amount_spent())
        
        trans_list = [] #get all transactions to be displayed in table 
        cust = []
        trans_name = {}
        for key in trans_dict:
            user_id = trans_dict[key].get_user_id()
            if user_id in cust_dict:
                print(user_id)
                print(cust_dict)
                #print(cust_dict[user_id].get_first_name())
                name = cust_dict[user_id].get_first_name()
                cust.append(name)
                print("Customer name=", name, " trans id =", trans_dict[key].get_trans_id())
                transactions = trans_dict.get(key)
                trans_list.append(transactions)
                trans_name[user_id] = name
        print(trans_name)
        
        

        dates = []
        log_count = []
        for key in sorted(login_counter.keys()):
            dates.append(key)
            log_count.append(len(login_counter[key]))
        plt.plot(dates, log_count)
        plt.xlabel('Date')
        plt.ylabel('Login Count')
        ax = plt.gca()
        ax.set(facecolor = "#ffc397") #change background color
        #remove borders
        ax.spines['top'].set_visible(False) 
        ax.spines['right'].set_visible(False)
        fig = ax.get_figure() #get figure
        #change face's background color
        fig.patch.set_facecolor('#ffc397')
        img = BytesIO() #create buffer to store image
        plt.savefig(img, format='png', bbox_inches='tight') #save image and ensure NO CUTOFF
        plt.close() #close/ end figure
        img.seek(0) #reset buffer to start
        plot_daily_traffic = base64.b64encode(img.getvalue()).decode('utf8')
        
        target = 1000
        target = sum(total) / target * 100
        sales_to_target = round(target, 2)
        #import plotly.graph_objects as go
        # if sum(total) >= 1000:
        #     fig = go.Figure(go.Indicator(
        #         mode = "gauge+number",
        #         value = sum(total),
        #         domain = {'x': [0, 1], 'y': [0, 1]}, 
        #         gauge = {'axis': {'range': [None, 1000]}, 'bgcolor': 'green'}  
        #         ))
        #     fig.update_layout(paper_bgcolor = "#ffc397")
        #     fig.show()
        # else: 
        #     fig = go.Figure(go.Indicator(
        #         mode = "gauge+number",
        #         value = sum(total),
        #         domain = {'x': [0, 1], 'y': [0, 1]}, 
        #         gauge = {'axis': {'range': [None, 1000]}, 'bgcolor': 'red'}  
        #         ))
        #     fig.update_layout(paper_bgcolor = "#ffc397")
        #     fig.show()
        # print(dates)
        # print(log_count)
        # df = pd.DataFrame({'date' : login_counter.keys() , 'date_value' : len(login_counter.values()) })
        # print(df)


        #fig.show()
        return render_template('./reports/stf-main.html', signup = len(cust_list), sales = sum(total), trans = len(total), trans_list = trans_list, plot_daily_traffic = plot_daily_traffic, log_count = log_count, sales_to_target = sales_to_target, name = cust, cust_list = cust_list, cust_dict = cust_dict, trans_name = trans_name)

            
    #         # cust_list = []
    #         # total = []
    #         # trans_list = []
    #         # log_count = []
    #         # plot_daily_traffic = 0
    #         # sales_to_target = 0
    #         # name = None
    #         import ctypes
    #         ctypes.windll.user32.MessageBoxW(0, "Start attracting users :)", "No Transactions!", 48)
    #         return render_template('./reports/stf-main.html')
    # else:
    #     return redirect(url_for('home'))
        

@app.route('/prod_report')
def prod_report():
    if session['acc_type'] == "Staff":
        prod_dict = {}
        trans_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            prod_dict = db['Products']
            trans_dict = db['Transaction']
        except:
            print("no details")    
        products_list = [] #get all products to be displayed in table
        for key in prod_dict:
            product = prod_dict.get(key)
            products_list.append(product)
        
        #storing all products bought into list
        prod_bought = []
        for transaction in trans_dict:
            items = trans_dict[transaction].get_items_bought()
            for x in items:
                prod_bought.append(x)
        prod_count = Counter(prod_bought) #count number of occurence of each item & store 
        #print(prod_count) - test/ debug code
        top_prod = []
        top_prod_count = []
        for top in sorted(prod_count, key=prod_count.get, reverse=True): #get key of each item with count & sort by count
            #print(top, prod_count[top]) - test/ debug code
            #prod_count[top] = number of occurrence, test/ debug code
            top_prod.append(top) #append top items to list in order of top sales
            top_prod_count.append(prod_count[top]) #append count of top items to list in order of top sales
        # print("top product", top_prod)
        # print("product count", top_prod_count)
        
        
        prod_ids = []
        for name in prod_bought:
            #print("name =", name)
            for key in prod_dict:
                prod = prod_dict[key]
                #print("dict_name = ", prod.get_name())  
                if prod.get_name() == name:
                    #print(prod.get_id())
                    prod_ids.append(prod.get_id())
                else:
                    pass
        prod_cat = []
        bar_clr = [] #test color change
        #renaming categories, so it prints out full category name instead of just the first letter
        for category in prod_ids:
            for key in prod_dict:
                prod = prod_dict[key]
                if prod.get_id() == category:
                    cat = prod.get_category()
                    if cat == "C":
                        catt = "Customised"
                        color = "orange"
                        bar_clr.append(color)
                        prod_cat.append(catt)
                    elif cat == "R":
                        catt = "Regular"
                        color = "blue"
                        bar_clr.append(color)
                        prod_cat.append(catt)
                    elif cat == "K":
                        catt = "Kids"
                        color = "pink"
                        bar_clr.append(color)
                        prod_cat.append(catt)
                    break
                else:
                    pass
            
        #plotting the graph    
        matplotlib.use('Agg')
        print(top_prod)
        colors = bar_clr #test color change :(
        df = pd.DataFrame({'Product': top_prod, 'Count':top_prod_count})
        ax = df.plot.bar(x='Product', y='Count') #change bar color
        ax.set(facecolor = "#ffc397") #change background color
        fig = ax.get_figure() #get figure
        #remove borders
        ax.spines['top'].set_visible(False) 
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        #change face's background color
        fig.patch.set_facecolor('#ffc397')
        img = BytesIO() #create buffer to store image
        plt.savefig(img, format='png', bbox_inches='tight') #save image and ensure NO CUTOFF
        plt.close() #close/ end figure
        img.seek(0) #reset buffer to start
        plot_url = base64.b64encode(img.getvalue()).decode('utf8') #encode image to base64 so that it can be retrieved in html :)))
        
        top_prod_cat = []
        top_prodcat_count = []
        prod_cat_count = Counter(prod_cat) #count number of occurence of each category & store
        for top_cat in sorted(prod_cat_count, key=prod_cat_count.get, reverse=True):
            top_prod_cat.append(top_cat) #append top items to list in order of top sales
            top_prodcat_count.append(prod_cat_count[top_cat])
        print("categories = ", top_prod_cat)
        print("count = ", top_prodcat_count)
        
        df_cat = pd.DataFrame({'Category': top_prod_cat, 'Count':top_prodcat_count})
        ax = df_cat.plot.barh(x='Category', y='Count', color = '#7dbcf0' ) #change bar color
        ax.set(facecolor = "#ffc397") #change background color
        fig = ax.get_figure() #get figure
        #remove borders
        ax.spines['top'].set_visible(False) 
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.invert_yaxis()
        #change face's background color
        fig.patch.set_facecolor('#ffc397')
        img = BytesIO() #create buffer to store image
        plt.savefig(img, format='png', bbox_inches='tight') #save image and ensure NO CUTOFF
        plt.close() #close/ end figure
        img.seek(0) #reset buffer to start
        plotcat_url = base64.b64encode(img.getvalue()).decode('utf8')
        
        # print(top_prod)
        # df = pd.DataFrame({'Category': top_prod_cat, 'Count':top_prodcat_count})
        # ax = df.plot.bar(x='Category', y='Count') #change bar color
        # ax.set(facecolor = "#ffc397") #change background color
        # fig = ax.get_figure() #get figure
        # #remove borders
        # ax.spines['top'].set_visible(False) 
        # ax.spines['right'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # #change face's background color
        # fig.patch.set_facecolor('#ffc397')
        # img = BytesIO() #create buffer to store image
        # plt.savefig(img, format='png', bbox_inches='tight') #save image and ensure NO CUTOFF
        # plt.close() #close/ end figure
        # img.seek(0) #reset buffer to start
        # plotcat_url = base64.b64encode(img.getvalue()).decode('utf8') #encode image to base64 so that it can be retrieved in html :)))
            
        # df_cat = pd.DataFrame({'Product': top_prod, 'Count':top_prod_count})
        # ax = df_cat.plot.barh(x='Product', y='Count', color = '#7dbcf0' ) #change bar color
        # ax.set(facecolor = "#ffc397") #change background color
        # fig = ax.get_figure() #get figure
        # #remove borders
        # ax.spines['top'].set_visible(False) 
        # ax.spines['right'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # ax.invert_yaxis()
        # #change face's background color
        # fig.patch.set_facecolor('#ffc397')
        # img = BytesIO() #create buffer to store image
        # plt.savefig(img, format='png', bbox_inches='tight') #save image and ensure NO CUTOFF
        # plt.close() #close/ end figure
        # img.seek(0) #reset buffer to start
        # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        
        #dIE    
        # for transaction in trans_dict:
        # #     dates = trans_dict[transaction].get_trans_date()
        # #     trans_date.append(date = [str(dates).split("-")])
        #     # trans_date = str(trans_dict[transaction].get_trans_date()).split("-") for transaction in trans_dict)
        #     # month = [date[1] for date in trans_date]    
            
        # df = pd.DataFrame({'month':month, 'category':cat})
        # print(cat)
        # print(df)  
        # print(month)
        # print(trans_date)
    
        # df_date = pd.DataFrame({'dates': trans_date})
        # df_date[["day", "month", "year"]] = df_date["dates"].str.split("-", expand = True)
        # print(df_date)
            
        return render_template('./reports/prod-report.html', products_list = products_list, plot_url=plot_url, plotcat_url=plotcat_url)
    else:
        return redirect(url_for('home'))

@app.route('/to_csv')
def csv():
    trans_dict = {}
    db = shelve.open('storage.db', 'w')
    trans_dict = db['Transaction']
    db.close()
    prod_bought = []
    for transaction in trans_dict:
        items = trans_dict[transaction].get_items_bought()
        for x in items:
            prod_bought.append(x)
    prod_count = Counter(prod_bought) #count number of occurence of each item & store 
    #print(prod_count) - test/ debug code
    top_prod = []
    top_prod_count = []
    for top in sorted(prod_count, key=prod_count.get, reverse=True): #get key of each item with count & sort by count
        #print(top, prod_count[top]) - test/ debug code
        #prod_count[top] = number of occurrence, test/ debug code
        top_prod.append(top) #append top items to list in order of top sales
        top_prod_count.append(prod_count[top]) #append count of top items to list in order of top sales
    df_csv = pd.DataFrame({'Product': top_prod, 'Count':top_prod_count})
    print(df_csv)
    df_csv.to_csv('output.csv',index=False)
    with open("output.csv") as fp:
        csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=product_sales.csv"})

@app.route('/delete_prod/<int:id>', methods=['POST'])
def delete_prod(id):
    prod_dict = {}
    db = shelve.open('storage.db', 'w')
    prod_dict = db['Products']
    prod_dict.pop(id)
    db['Products'] = prod_dict
    db.close()
    return redirect(url_for('prod_report'))

# end of report pages

# Skye's part
@app.route('/feedback')
def feedback():
    return render_template("./customer_support/feedback.html")


# @app.route('/contactus', methods=["GET","POST"])
# def get_contact():
#     form = ContactForm()
#     # here, if the request type is a POST we get the data on contat
#     #forms and save them else we return the contact forms html page
#     if request.method == 'POST':
#         name =  request.form["name"]
#         email = request.form["email"]
#         subject = request.form["subject"]
#         message = request.form["message"]
#         res = pd.DataFrame({'name':name, 'email':email, 'subject':subject ,'message':message}, index=[0])
#         res.to_csv('./contactusMessage.csv')
#         print("The data are saved !")
#     else:
#         return render_template('contact.html', form=form)

@app.route('/customersupportmain')
def customersupportmain():
    return render_template("./customer_support/customersupportmain.html")


@app.route('/Accountbasicsmain')
def Accountbasicsmain():
    return render_template("./customer_support/Accountbasicsmain.html")

@app.route('/forgot_acc')
def forgot_acc():
    return render_template("./customer_support/forgot_acc.html")

@app.route('/forgot_acc2')
def forgot_acc2():
    return render_template("./customer_support/forgot_acc2.html")

@app.route('/forgot_acc3')
def forgot_acc3():
    return render_template("./customer_support/forgot_acc3.html")

@app.route('/forgot_acc4')
def forgot_acc4():
    return render_template("./customer_support/forgot_acc4.html")

@app.route('/forgot_acc5')
def forgot_acc5():
    return render_template("./customer_support/forgot_acc5.html")

@app.route('/forgot_acc6')
def forgot_acc6():
    return render_template("./customer_support/forgot_acc6.html")

@app.route('/forgot_acc7')
def forgot_acc7():
    return render_template("./customer_support/forgot_acc7.html")

@app.route('/forgot_acc8')
def forgot_acc8():
    return render_template("./customer_support/forgot_acc8.html")


@app.route('/billingmain')
def billingmain():
    return render_template("./customer_support/billingmain.html")

@app.route('/billing1')
def billing1():
    return render_template("./customer_support/billing1.html")

@app.route('/billing2')
def billing2():
    return render_template("./customer_support/billing2.html")

@app.route('/billing3')
def billing3():
    return render_template("./customer_support/billing3.html")

@app.route('/billing4')
def billing4():
    return render_template("./customer_support/billing4.html")

@app.route('/billing5')
def billing5():
    return render_template("./customer_support/billing5.html")

@app.route('/billing6')
def billing6():
    return render_template("./customer_support/billing6.html")

@app.route('/billing7')
def billing7():
    return render_template("./customer_support/billing7.html")

@app.route('/deliverymain')
def deliverymain():
    return render_template("./customer_support/deliverymain.html")

@app.route('/delivery1')
def delivery1():
    return render_template("./customer_support/delivery1.html")

@app.route('/delivery2')
def delivery2():
    return render_template("./customer_support/delivery2.html")

@app.route('/delivery3')
def delivery3():
    return render_template("./customer_support/delivery3.html")

@app.route('/delivery4')
def delivery4():
    return render_template("./customer_support/delivery4.html")

@app.route('/delivery5')
def delivery5():
    return render_template("./customer_support/delivery5.html")

@app.route('/productinfomain')
def productinfomain():
    return render_template("./customer_support/productinfomain.html")

@app.route('/prodin1')
def prodin1():
    return render_template("./customer_support/prodin1.html")

@app.route('/prodin2')
def prodin2():
    return render_template("./customer_support/prodin2.html")

@app.route('/feedbackconfirm')
def feedbackconfirm():
    return render_template("./customer_support/feedbackconfirm.html")

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User(create_user_form.skye_first_name.data, create_user_form.skye_last_name.data, create_user_form.skye_RateProd.data, create_user_form.skye_RatePrice.data, create_user_form.skye_RateDel.data, create_user_form.skye_email.data, create_user_form.skye_remarks.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        print(users_dict)

        db.close()

        return redirect(url_for('feedbackconfirm'))
    return render_template('./customer_support/createUser.html', form=create_user_form)

@app.route('/skye_retrieveUsers', methods = ['GET', 'POST'])
def skye_retrieve_users():
    # users_dict = {}
    # db = shelve.open('storage.db', 'r')
    # users_dict = db['Users']
    # db.close()
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    # users_list = []
    # for key in users_dict:
    #     user = users_dict.get(key)
    #     users_list.append(user)

    return render_template('./customer_support/retrieveUsers.html', count=len(users_list), users_list=users_list)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.skye_first_name.data)
        user.set_last_name(update_user_form.skye_last_name.data)
        user.set_skye_RateProd(update_user_form.skye_RateProd.data)
        user.set_skye_RatePrice(update_user_form.skye_RatePrice.data)
        user.set_skye_RateDel(update_user_form.skye_RateDel.data)
        user.set_remarks(update_user_form.skye_remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('skye_retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.skye_first_name.data = user.get_skye_first_name()
        update_user_form.skye_last_name.data = user.get_skye_last_name()
        update_user_form.skye_RateProd.data = user.get_skye_RateProd()
        update_user_form.skye_RatePrice.data = user.get_skye_RatePrice()
        update_user_form.skye_RatePrice.data = user.get_skye_RatePrice()
        update_user_form.skye_email.data = user.get_skye_email()
        update_user_form.skye_remarks.data = user.get_skye_remarks()

        return render_template('./customer_support/createUser.html', form=update_user_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('skye_retrieve_users'))


if __name__ == '__main__':
    app.run(debug=True)
