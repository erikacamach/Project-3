
import pandas as pd
from sqlalchemy import create_engine 
from flask import Flask, render_template

#  Database file path
db_path = "Resources\project3.sqlite"

# Connecting to the SQLite database
engine = create_engine(f"sqlite:///{db_path}")
conn = engine.connect()

# Reading data from the database and loading in DataFrame
query = "select * from house_data"
housedata_df = pd.read_sql(query,conn)
conn.close()


# Sorting  DataFrame in descending order of Median Home Price 
houseprice_sortedD = housedata_df.sort_values("Median Home Price", ascending = False)
houseprice_sortedD = houseprice_sortedD[['State', 'Median Home Price','Median Household Income']]
#print (houseprice_sortedD)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.json.sort_keys = False

# Flask mapping for initial Page
@app.route("/")
def index():
    return render_template("index.html")

# Flask mapping for overview of 2023 house price
@app.route("/api/v1.0/overview")
def overview_data():    
    houseprice_sortedD_json = houseprice_sortedD.to_json()
    return houseprice_sortedD_json
    
# Flask mapping for house price by states
@app.route("/api/v1.0/states_details")
def state_data():    
    housedata_json = housedata_df.to_json()
    return housedata_json    
    

if __name__ == '__main__':
    app.run(debug=True)
