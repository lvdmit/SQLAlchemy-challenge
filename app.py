import numpy as np
import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

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
        "Available Routes: <br/>"
        "/api/v1.0/precipitation<br/>"
        #"<a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a><br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all passenger names"""
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-10-01').\
        group_by(Measurement.date).all()

    
    all_precipitation = []
    
    for result in results:
        precipitation_dict = {}
        precipitation_dict["date"] = result[0]
        precipitation_dict["prcp"] = result[1]
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the stations"""
   
    results = session.query(Measurement.station).group_by(Measurement.station).all()

   
    all_sessions = list(np.ravel(results))

    return jsonify(all_sessions)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all the temperature observations"""
   
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-10-01').all()

    

    all_tobs = []
    
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result[0]
        tobs_dict["tobs"] = result[1]
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    """the minimum temperature, the average temperature, and the max temperature for a given start date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    start_data = list(np.ravel(results))

    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    """the minimum temperature, the average temperature, and the max temperature for a given start-end range"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
   
    start_end_data = list(np.ravel(results))

    return jsonify(start_end_data)


if __name__ == '__main__':
    app.run(debug=True)
