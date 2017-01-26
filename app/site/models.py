from .. import db


#amount_to_ingredient = db.Table('amount_to_ingredient',
 #                               db.Column('amount_id', db.Integer, db.ForeignKey('ammount.id'), nullable=False),
  #                              db.Column('ingredient_id', db.Integer, db.ForeignKey('ingrediant.id'), nullable=False),
   #                             db.PrimaryKeyConstraint('post_id', 'tags_id') )

class Meal(db.Model):
    __tablename__="meals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    instructions = db.Column(db.Text)

   # amounts = db.relationship(Ammount, backref="meal", lazy="dynamic")

class Ingrediant(db.Model):
    __tablename__="ingrediant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Measure(db.Model):
    __tablename__="measure"
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(120), unique=True)

class Ammount(db.Model):
    __tablename__="ammount"
    id = db.Column(db.Integer, primary_key=True)
    ammount = db.Column(db.Integer)

    measure_id = db.Column(db.Integer, db.ForeignKey('measure.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    ing_id = db.Column(db.Integer, db.ForeignKey('ingrediant.id'))


class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



#meals = Meal.query.get(NUMBER)
#ingrediants = Ammount.query.join(Ingrediant, Ingrediant.id==Ammount.ing_id).join(Measure, measure.id==Ammount.measure_id).filter(Ammount.meal_id==NUMBER)