import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.environ.get('SERVER_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


# db model
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


# new cafe form model
class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe Name', validators=[DataRequired()])
    location = StringField('Location')
    w_f = BooleanField('Has Wi-Fi', validators=[DataRequired()])
    coffee_p = StringField('Coffee Price', validators=[DataRequired()], render_kw={"placeholder":
                                                                                   "eg, £2.35 NOTE: alt + 0163 "
                                                                                   "to get '£'"})
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_entry = Cafe(
            name=form.cafe.data,
            location=form.location.data,
            has_wifi=form.w_f.data,
            coffee_price=form.coffee_p.data,
        )

        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.order_by(Cafe.id).all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route('/cafe_submitted')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
