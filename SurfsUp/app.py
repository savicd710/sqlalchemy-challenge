import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
abs_path = os.getcwd()
abs_path=abs_path.replace('\\sqlalchemy-challenge', '')
abs_path=abs_path+'\\sqlalchemy-challenge\\SurfsUp\\Resources\\hawaii.sqlite'
print(abs_path)



engine = create_engine(f'sqlite:///{abs_path}', echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )








if __name__ == "__main__":
    app.run(debug=True)
