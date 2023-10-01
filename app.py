
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify, render_template

db_path = "Resources\project3.sqlite"



engine = create_engine(f"sqlite:///{db_path}")
conn = engine.connect()

query = "select * from house_data"
housedata_df = pd.read_sql(query,conn)
print (housedata_df.head())

conn.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1.0/states_details")
def state_data():

    # print("Inside states API call")
    housedata_json = housedata_df.to_json()
    return housedata_json
    # return jsonify()

if __name__ == '__main__':
    app.run(debug=True)
