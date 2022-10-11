import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Calculate the date one year from the last date in data set.
year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

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
        f"Precipation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Tobs: /api/v1.0/tobs<br/>"
        f"Tobs for a specified Start Date: /api/v1.0/yyyy-mm-dd<br/>"
        f"Tobs for a specified Start and End Date: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data from the last 12 months"""
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= year_ago).order_by(Measurement.date).all()

    session.close()

    # Create an empty list to hold the dictionaries
    precipitation_data = []

    # Loop through results to append to empty list
    for date, prcp in results:
        prcp_dict = {}

        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp

        precipitation_data.append(prcp_dict)

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station data"""
    # Query all station data
    results = session.query(Station.station, Station.name,
                            Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create an empty list to hold the dictionaries
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}

        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation

        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs from the most active station for the previous year of data"""
    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    most_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(
        Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # Query all tobs from the most active station
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == most_active[0][0]).filter(Measurement.date >= year_ago).all()

    session.close()

    # Create an empty list to hold the dictionaries
    most_active_tobs = []
    for date, tobs in results:
        most_active_dict = {}

        most_active_dict['Date'] = date
        most_active_dict['Tobs'] = tobs

        most_active_tobs.append(most_active_dict)

    return jsonify(most_active_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, and max temperatures for a specified start date"""
    # Query using func operations from SQLAlchemy
    results = session.query(func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Create an empty list to hold the dictionaries
    start_date_summary = []
    for min_tobs, avg_tobs, max_tobs in results:
        start_date_dict = {}

        start_date_dict['Min_Tobs'] = min_tobs
        start_date_dict['Avg_Tobs'] = avg_tobs
        start_date_dict['Max_Tobs'] = max_tobs

        start_date_summary.append(start_date_dict)

    return jsonify(start_date_summary)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, and max temperatures for a specified start and end date"""
    # Query using func operations from SQLAlchemy
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(
        Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Create an empty list to hold the dictionaries
    start_end_summary = []
    for min_tobs, avg_tobs, max_tobs in results:
        start_end_dict = {}

        start_end_dict['Min_Tobs'] = min_tobs
        start_end_dict['Avg_Tobs'] = avg_tobs
        start_end_dict['Max_Tobs'] = max_tobs

        start_end_summary.append(start_end_dict)

    return jsonify(start_end_summary)


if __name__ == "__main__":
    app.run(debug=True)
