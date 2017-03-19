from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import current_user
from .models import Meal, Ingrediant, Measure, Ammount, User
from .forms import BigForm, SettingForm, LoginForm, SignupForm
from sqlalchemy.sql.expression import func
from .. import login_manager, bcrypt
from flask_login import current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required
from .. import db

main = Blueprint("main", __name__)


@main.route('/')
def about():
    return render_template('about.html')


@main.route('/test')
def test():
    return redirect(url_for('main.calendar', days='2', meal='1', breakfast='001002'))


@main.route('/settings/', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():

        days = int(form.days.data)

        bin_meal_num = 0
        if form.breakfast.data:
            bin_meal_num += 1
        if form.lunch.data:
            bin_meal_num += 2
        if form.dinner.data:
            bin_meal_num += 4

        breakfast = ''
        lunch = ''
        dinner = ''

        if form.breakfast.data:
            meal = Meal.query.filter(Meal.breakfast.is_(True)).order_by(func.rand()).limit(days).all()
            for m in meal:
                breakfast += (str(m.id).zfill(3))
        if form.lunch.data:
            meal = Meal.query.filter(Meal.lunch.is_(True)).order_by(func.rand()).limit(days).all()
            for m in meal:
                lunch += (str(m.id).zfill(3))
        if form.dinner.data:
            meal = Meal.query.filter(Meal.dinner.is_(True)).order_by(func.rand()).limit(days).all()
            for m in meal:
                dinner += (str(m.id).zfill(3))
        return redirect(url_for('main.calendar',
                                days=days,
                                meal=bin_meal_num,
                                breakfast=breakfast,
                                lunch=lunch,
                                dinner=dinner))

    return render_template('settings.html', form=form, current_user=current_user)


@main.route('/calendar/')
def calendar():
    if request.args.get('days'):
        days = int(request.args.get('days'))
        meal_arg = int(request.args.get('meal'))

        dictionary = {'breakfast': request.args.get('breakfast'),
                      'lunch': request.args.get('lunch'),
                      'dinner': request.args.get('dinner')}

        meal_list = {'breakfast': [],
                     'lunch': [],
                     'dinner': []}

        meal_key = {'breakfast': 0x1,
                    'lunch': 0x2,
                    'dinner': 0x4}

        y = [k for k, v in meal_key.items() if meal_arg & v == v]
        for m in y:
            if m in dictionary:
                g = dictionary.get(m)
                meal_list[m] = break_list(str(g), days)

        ingrediants = []

        #query the database
        breakfast_meals = Meal.query.filter(Meal.id.in_(meal_list['breakfast'])).all()
        lunch_meals = Meal.query.filter(Meal.id.in_(meal_list['lunch'])).all()
        dinner_meals = Meal.query.filter(Meal.id.in_(meal_list['dinner'])).all()

        breakfast_dic = {'name': "Breakfast", 'data': breakfast_meals}
        lunch_dic = {'name': "Lunch", 'data': lunch_meals}
        dinner_dic = {'name': "Dinner", 'data': dinner_meals}

        meals = [breakfast_dic, lunch_dic, dinner_dic]

        # get the ingredients into the ingredients list
        for meal_list in meals:
            if meal_list['data']:
                for each in meal_list['data']:
                    ingrediant = db.engine.execute(
                        "SELECT ingrediant.name, ammount.ammount, measure.unit "
                        "FROM ammount "
                        "INNER JOIN ingrediant "
                        "ON ammount.ing_id=ingrediant.id "
                        "INNER JOIN measure "
                        "ON ammount.measure_id=measure.id "
                        "WHERE ammount.meal_id=" + str(each.id) + ";")
                    for ing in ingrediant:
                        i = {'name': ing.name, 'ammount': ing.ammount, 'unit': ing.unit}
                        ingrediants.append(i)

        ingrediants.sort(key=lambda x: (x['name'], x['unit']))
        for _ in range(days):
            for i in range((len(ingrediants))):
                try:
                    if ingrediants[i]['name'] == ingrediants[i + 1]['name'] and \
                                    ingrediants[i]['unit'] == ingrediants[i + 1]['unit']:
                        number = int(ingrediants[i]['ammount']) + int(ingrediants[i + 1]['ammount'])
                        ingrediants[i]['ammount'] = number
                        ingrediants.pop(i+1)
                except IndexError:
                    pass
        percent = (100/days)

        return render_template('calendar.html',
                               meals=meals,
                               ingrediants=ingrediants,
                               current_user=current_user,
                               percent=percent,
                               days=days)
    else:
        days = 7
        meal_arg = 4

        dinner = ""

        meal = Meal.query.filter(Meal.dinner.is_(True)).order_by(func.rand()).limit(days).all()
        for m in meal:
            dinner += (str(m.id).zfill(3))

        return redirect(url_for('main.calendar',
                                days=days,
                                meal=meal_arg,
                                dinner=dinner))


@main.route('/meal/')
def meal():
    num = request.args.get('meal')
    meal = Meal.query.get(num)
    ingrediants = []
    # ingrediant = Ammount.query.join(Ingrediant, Ammount.ing_id == Ingrediant.id )
    # .join(Measure, Ammount.measure_id == Measure.id).filter(Ammount.meal_id == meal.id )
    ingrediant = db.engine.execute("SELECT ingrediant.name, ammount.ammount, measure.unit "
                                   "FROM ammount "
                                   "INNER JOIN ingrediant "
                                   "ON ammount.ing_id=ingrediant.id "
                                   "INNER JOIN measure "
                                   "ON ammount.measure_id=measure.id "
                                   "WHERE ammount.meal_id=" + str(meal.id) + ";")
    for ing in ingrediant:
        ingrediants.append(ing)
    ingrediants.sort(key=lambda x: x.name)
    return render_template('meal.html',
                           meal=meal,
                           ingrediants=ingrediants,
                           current_user=current_user)


@main.route('/insert/', methods=["GET", "POST"])
@login_required
def insert():
    form = BigForm()
    if form.validate_on_submit():
        print "validation succeessful"
        meal = Meal()
        meal.name = form.name.data
        meal.instructions = form.instructions.data
        meal.breakfast = form.breakfast.data
        meal.lunch = form.lunch.data
        meal.dinner = form.dinner.data
        db.session.add(meal)
        db.session.commit()
        for i in range(11):
            if form.ingrediants[i].data:
                try:
                    ing = Ingrediant()
                    dbing = Ingrediant.query.filter(Ingrediant.name.like(form.ingrediants[i].data)).first()
                    if dbing:
                        ing = dbing
                    else:
                        ing.name = form.ingrediants[i].data
                        db.session.add(ing)
                        db.session.commit()

                    meas = Measure.query.filter(Measure.unit.like(form.measurements[i].data)).first()

                    amnt = Ammount()
                    amnt.meal_id = meal.id
                    amnt.ammount = form.ammounts[i].data
                    amnt.measure_id = meas.id
                    amnt.ing_id = ing.id
                    db.session.add(amnt)
                    db.session.commit()
                except IndexError:
                    pass
            else:
                break
        return redirect(url_for('main.about'))

    return render_template('insert.html',
                           form=form,
                           current_user=current_user)


@main.route('/profile/')
def profile():
    return render_template("profile.html",
                           current_user=current_user)


@login_required
@main.route('/measure/')
def measure():
    if current_user.admin:
        example_list = ['Gallon', 'Litre', 'Pint', 'Cup', 'Fluid ounce',
                        'Pound', 'ounce', 'Table spoon', 'Tea spoon',
                        'Inch', 'Centimeter', 'Milliliter', 'Piece', 'Dozen']
        for i in example_list:
            meas = Measure()
            meas.unit = i
            db.session.add(meas)
            db.session.commit()
        return redirect(url_for('main.about'))
    return redirect(url_for('main.about'))

############################################
# Login Manager
############################################


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@main.route('/register', methods=["get", "POST"])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user.password = pw_hash
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form, current_user=current_user)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for('main.about'))
    return render_template("login.html", form=form, current_user=current_user)


@main.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.about'))


def break_list(string, days):
    """ breaks a string into a listt with groups of 3 chars"""
    temp_list = []
    for i in range(days):
        part = string[(i*3):((i*3)+3)]
        temp_list.append(part)
    return temp_list
