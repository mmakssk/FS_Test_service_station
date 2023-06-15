from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Database connect
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:6455@localhost:5432/fstest"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Database Model
class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password, last_name, first_name):
        self.email = email
        self.password = password
        self.last_name = last_name
        self.first_name = first_name

    def __repr__(self):
        return f""


class OrderModel(db.Model):
    __tablename__ = 'order_card'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    car_number = db.Column(db.String(8), nullable=False)
    car_brand = db.Column(db.String(150), nullable=False)
    year_issue = db.Column(db.Integer, nullable=False)
    car_mileage = db.Column(db.Integer, nullable=False)
    breakdowns = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(100, 2), nullable=False)
    mechanic_first_name = db.Column(db.String(50), nullable=False)
    mechanic_last_name = db.Column(db.String(50), nullable=False)
    status_pending = db.Column(db.Boolean)
    status_progress = db.Column(db.Boolean)
    status_completed = db.Column(db.Boolean)

    def __init__(self, email, car_number, car_brand, year_issue,  car_mileage, breakdowns, price, mechanic_first_name, mechanic_last_name, status_pending, status_progress, status_completed):
        self.email = email
        self.car_number = car_number
        self.car_brand = car_brand
        self.year_issue = year_issue
        self.car_mileage = car_mileage
        self.breakdowns = breakdowns
        self.price = price
        self.mechanic_first_name = mechanic_first_name
        self.mechanic_last_name = mechanic_last_name
        self.status_pending = status_pending
        self.status_progress = status_progress
        self.status_completed = status_completed

    def __repr__(self):
        return f""

class SaveUserModel(db.Model):
    __tablename__ = "save_email"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f""


db.create_all()


# site route
# main page
@app.route('/')
def index():
    try:
        save_e = SaveUserModel.query.first()
        db.session.delete(save_e)
        db.session.commit()
    except:
        pass
    card = OrderModel.query.filter_by(status_completed=True).all()
    return render_template('index.html', card=card)


# page for registration
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    message = ""
    if request.method == "POST":
        # getting data from form
        email = request.form['email']
        password = request.form['password']
        l_name = request.form['last_name']
        f_name = request.form['first_name']

        test = True
        test_dog = False
        test_dot = False

        # password validity test
        if len(password) != 8:
            test = False

        new_user = UsersModel(email=email, password=password, last_name=l_name, first_name=f_name)

        try:
            if test:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/sign_in')
            else:
                # email repeat test
                user = UsersModel.query.filter_by(email=email).first()
                if user:
                    message = "Данный email уже зарегистрирован"
                else:
                    message = "Неверно введенные данные (пароль должен быть 8 символов)"

        except:
            user = UsersModel.query.filter_by(email=email).first()
            if user:
                message = "Данный email уже зарегистрирован"
            else:
                message = "Неверно введенные данные"

    return render_template('sign_up.html', message=message)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    try:
        save_e = SaveUserModel.query.first()
        db.session.delete(save_e)
        db.session.commit()
    except:
        pass
    message = ""
    if request.method == "POST":
        save_email = request.form['email']
        password = request.form['password']
        # user presence test
        user = UsersModel.query.filter_by(email=save_email, password=password).first()

        if user:
            save_e = SaveUserModel(email = user.email)
            db.session.add(save_e)
            db.session.commit()
            return redirect('/login_user')
        else:
            message = "Неверно введенный email или пароль"

    return render_template('sign_in.html', message=message)


@app.route('/create_order', methods=['POST', 'GET'])
def create_order():
    message = " "

    if request.method == "POST":
        # getting data from form
        car_number = request.form['car_number']
        car_brand = request.form['car_brand']
        year = request.form['year']
        car_mileage = request.form['car_mileage']
        breakdowns = request.form['breakdowns']
        price = request.form['price']
        m_last_name = request.form['m_last_name']
        m_first_name = request.form['m_first_name']
        status = request.form['status']

        test = True
        # information correctness test
        if len(car_number) != 8:
            test = False
        elif int(year) < 1900:
            test = False
        elif int(car_mileage) < 0:
            test = False
        elif float(price) < 0.01:
            test = False

        try:
            if test:
                save_email = SaveUserModel.query.first()
                if status == "pending":
                    new_order = OrderModel(email=save_email.email, car_number=car_number, car_brand=car_brand, year_issue=year,
                                           car_mileage=car_mileage, breakdowns=breakdowns, price=price,
                                           mechanic_first_name=m_first_name, mechanic_last_name=m_last_name,
                                           status_pending=True, status_progress=False, status_completed=False)
                    db.session.add(new_order)
                    db.session.commit()
                    return redirect('/my_order')
                elif status == "progress":
                    new_order = OrderModel(email=save_email.email, car_number=car_number, car_brand=car_brand, year_issue=year,
                                           car_mileage=car_mileage, breakdowns=breakdowns, price=price,
                                           mechanic_first_name=m_first_name, mechanic_last_name=m_last_name,
                                           status_pending=False, status_progress=True, status_completed=False)
                    db.session.add(new_order)
                    db.session.commit()
                    return redirect('/my_order')
                elif status == "completed":
                    new_order = OrderModel(email=save_email.email, car_number=car_number, car_brand=car_brand, year_issue=year,
                                           car_mileage=car_mileage, breakdowns=breakdowns, price=price,
                                           mechanic_first_name=m_first_name, mechanic_last_name=m_last_name,
                                           status_pending=False, status_progress=False, status_completed=True)
                    db.session.add(new_order)
                    db.session.commit()
                    return redirect('/my_order')
            else:
                message = "Неверно введенныйе данные"
        except:
            message = "Неверно введенныйе данные"

    return render_template('create_order.html', message=message)


@app.route('/login_user')
def login_user():
    card = OrderModel.query.filter_by().all()
    return render_template('login_users.html', card=card)


@app.route('/my_order')
def my_order():
    save_email = SaveUserModel.query.first()
    card = OrderModel.query.filter_by(email=save_email.email).all()
    return render_template('my_order.html', card=card)


@app.route('/<int:id>')
def card(id):
    card = OrderModel.query.get(id)
    # status test
    if card.status_pending:
        return render_template('card.html', card=card, status="Pending")
    elif card.status_progress:
        return render_template('card.html', card=card, status="Progress")
    elif card.status_completed:
        return render_template('card.html', card=card, status="Completed")


@app.route('/card_log/<int:id>')
def card_log(id):
    card = OrderModel.query.get(id)
    if card.status_pending:
        return render_template('card_log_user.html', card=card, status="Pending")
    elif card.status_progress:
        return render_template('card_log_user.html', card=card, status="Progress")
    elif card.status_completed:
        return render_template('card_log_user.html', card=card, status="Completed")


@app.route('/my_card/<int:id>')
def my_card(id):
    card = OrderModel.query.get(id)
    if card.status_pending:
        return render_template('my_card.html', card=card, status="Pending")
    elif card.status_progress:
        return render_template('my_card.html', card=card, status="Progress")
    elif card.status_completed:
        return render_template('my_card.html', card=card, status="Completed")


@app.route('/my_card/<int:id>/delete')
def card_delete(id):
    card = OrderModel.query.get(id)
    try:
        db.session.delete(card)
        db.session.commit()
        return redirect('/my_order')
    except:
        return "Error"


@app.route('/my_card/<int:id>/update', methods=['POST', 'GET'])
def card_update(id):
    card = OrderModel.query.get(id)
    status = " "
    message = " "
    # status rest
    if card.status_pending:
        status = "pending"
    elif card.status_progress:
        status = "progress"
    elif card.status_completed:
        status = "completed"

    if request.method == "POST":
        # getting data from form
        card.car_number = request.form['car_number']
        card.car_brand = request.form['car_brand']
        card.year_issue = request.form['year']
        card.car_mileage = request.form['car_mileage']
        card.breakdowns = request.form['breakdowns']
        card.price = request.form['price']
        card.mechanic_last_name = request.form['m_last_name']
        card.mechanic_first_name = request.form['m_first_name']
        statuss = request.form['status']

        test = True

        if len(card.car_number) != 8:
            test = False
        elif int(card.year_issue) < 1900:
            test = False
        elif int(card.car_mileage) < 0:
            test = False
        elif float(card.price) < 0.01:
            test = False

        try:
            if test:
                if statuss == "pending":
                    card.status_pending = True
                    card.status_progress = False
                    card.status_completed = False
                    db.session.commit()
                    return redirect('/my_order')
                elif statuss == "progress":
                    card.status_pending = False
                    card.status_progress = True
                    card.status_completed = False
                    db.session.commit()
                    return redirect('/my_order')
                elif statuss == "completed":
                    card.status_pending = False
                    card.status_progress = False
                    card.status_completed = True
                    db.session.commit()
                    return redirect('/my_order')
                else:
                    db.session.commit()
                    return redirect('/my_order')
            else:
                message = "Неверно введенныйе данные"
        except:
            message = "Неверно введенныйе данные"

    return render_template("update.html", card=card, status=status, message=message)


@app.route('/del_account')
def del_account():
    save_email = SaveUserModel.query.first()
    user = UsersModel.query.filter_by(email=save_email.email).first()
    card = OrderModel.query.filter_by(email=user.email, status_completed=False).all()

    for el in card:
        del_card = OrderModel.query.get(el.id)
        db.session.delete(del_card)
        db.session.commit()

    db.session.delete(user)
    db.session.commit()
    return redirect("/")


@app.route('/my_card/<int:id>/update_error')
def update_error(id):
    card = OrderModel.query.get(id)
    return render_template('update_error.html')


if __name__ == "__main__":
    app.run(debug=True)
