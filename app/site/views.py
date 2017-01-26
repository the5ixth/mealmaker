from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import current_user
from .models import Meal, Ingrediant, Measure, Ammount
from .forms import BigForm
import time
import os

from .. import db

main = Blueprint("main", __name__)


@main.route('/')
def about():
    return render_template('about.html')


@main.route('/calendar/')
def calendar():
    meal = Meal.query.get(1)
#    for meal in meals:
#        ingrediant = Ammount.query.join(Ingrediant,
#                                        Ingrediant.id == Ammount.ing_id).join(Measure,
#                                                                              Measure.id == Ammount.Measure_id).filter(Ammount.meal_id == meal.id)
#        ingrediants.append(ingrediant)
    return render_template('calendar.html', meal=meal)

@main.route('/insert/',methods=["GET", "POST"])
def insert():
    form = BigForm()
    if request.method == 'POST':
        meal = Meal()
        meal.name = form.name.data
        meal.instructions = form.instructions.data
        db.session.add(meal)
        db.session.commit()
        for i in range(11):
            if form.ingrediants[i].data:
                amnt = Ammount()
                ing = Ingrediant()
                ing.name = form.ingrediants[i].data
                db.session.add(ing)
                db.session.commit()
                amnt.meal_id = meal.id
                amnt.ammount = form.ammounts[i].data
                amnt.measure_id = form.measure[i].data
                amnt.ing_id = ing.id
                db.session.add(amnt)
                db.session.commit()
        return redirect(url_for('main.about'))



    return render_template('insert.html',form=form)

