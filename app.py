import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)


# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_prcp = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).all()

    session.close()

    date_tobs = list(np.ravel(results))

    return jsonify(date_tobs)


@app.route("/api/v1.0/<startdate>")
def start_input(startdate):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all()
    
    session.close()

    date_stat = list(np.ravel(results))

    return jsonify(date_stat)

@app.route("/api/v1.0/<startdate><enddate>")
def start_end_input(startdate, enddate):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= startdate, Measurement.date <= enddate).all()
    
    session.close()

    dates_stat = list(np.ravel(results))

    return jsonify(dates_stat)

if __name__ == '__main__':
    app.run(debug=True)
