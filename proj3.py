from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/kevin/Documents/proj3/resources/project3.sqlite'
db = SQLAlchemy(app)

class HouseData(db.Model):
    Id = db.Column("Id", db.Integer, primary_key=True)
    State = db.Column("State", db.String)
    Median_Home_Price = db.Column("Median Home Price", db.Integer)
    Median_Home_Size = db.Column("Median Home Size (in square feet)", db.Integer)
    Median_Household_Income = db.Column("Median Household Income", db.Integer)

    def to_dict(self):
        return {
            'Id': self.Id,
            'State': self.State,
            'Median Home Price': self.Median_Home_Price,
            'Median Home Size': self.Median_Home_Size,
            'Median Household Income': self.Median_Household_Income
        }


class CitiesData(db.Model):
    STATE = db.Column(db.String, primary_key=True)
    one_earner = db.Column(db.Float, name=" 1 EARNER")
    two_people = db.Column(db.Float, name=" 2 PEOPLE")
    three_people = db.Column(db.Float, name=" 3 PEOPLE")
    four_people = db.Column(db.Float, name=" 4 PEOPLE *")

    def to_dict(self):
        return {
            'STATE': self.STATE,
            '1 EARNER': self.one_earner,
            '2 PEOPLE': self.two_people,
            '3 PEOPLE': self.three_people,
            '4 PEOPLE': self.four_people
        }

@app.route('/')
def home():
    # You could query your database to get the list of states for both house and income data.
    # For simplicity, I'm using hardcoded lists here:
    house_states = db.session.query(HouseData.State).distinct().all()
    income_states = db.session.query(CitiesData.STATE).distinct().all()

    html = """
    <h1>Project 3</h1>
    <h2>House Data</h2>
    {% for state in house_states %}
        <a href='/house_data/{{ state[0] }}'>{{ state[0] }}</a><br>
    {% endfor %}
    <h2>Income Data</h2>
    {% for state in income_states %}
        <a href='/income/{{ state[0] }}'>{{ state[0] }}</a><br>
    {% endfor %}
    """

    return render_template_string(html, house_states=house_states, income_states=income_states)

@app.route('/house_data/<state>', methods=['GET'])
def get_house_data(state):
    house = HouseData.query.filter(func.lower(HouseData.State) == state.lower()).first() 
    if not house:
        return jsonify({'error': 'State not found'}), 404

    return jsonify(house.to_dict())

@app.route('/income/<state>', methods=['GET'])
def get_income_by_state(state):
    income = CitiesData.query.filter(func.lower(CitiesData.STATE) == state.lower()).first() 
    if not income:
        return jsonify({'error': 'State not found'}), 404
    return jsonify(income.to_dict())

if __name__ == '__main__':
    app.run(debug=True)