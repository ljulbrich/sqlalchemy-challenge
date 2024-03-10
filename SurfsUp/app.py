# Import the dependencies.
from flask import Flask, jsonify, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from pathlib import Path
import numpy as np
import regex as re

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine_path = Path('../Resources/hawaii.sqlite')
engine = create_engine(f'sqlite:///{engine_path}')

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create a session
session = Session(engine)
conn = engine.connect()
session.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/api/v1.0/precipitation")
def precipitation():
    start_date = "2016-08-23"
    end_date = "2017-08-23"
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(start_date, end_date)).all()
    session.close()
    measurement_list = [{'date':date, 'precipitation':prcp} for date, prcp in results]
    return jsonify(measurement_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    station_list = [{'station':station, 'name':name, 'latitude':latitude, 'longitude':longitude, 'elevation':elevation}
                     for station, name, latitude, longitude, elevation in results]
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()
    session.close()
    tobs_list = [{'date':date, 'tobs':tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start_date>')
def temp_from_date(start_date):
    start_match = re.match(r"\d{4}\W\d{2}\W\d{2}", start_date)
    session = Session(engine)
    dates = session.query(Measurement.date).all()
    # I have to format the dates from the SQLlite database to check them against the input date
    # This seems to be faster than the regex
    blacklist = ['(', "'", ',', ')']
    date_list = []
    for date in dates:
        new_string = ''
        for char in date:
            if char in blacklist:
                new_string += ''
            else:
                new_string += char
        date_list.append(new_string)
    end_date = '2017-08-23'
    error_msg_1 = 'Invalid date input.\nPlease use YYYY-MM-DD format.'
    error_msg_2 = 'Invalid date input.\nPlease input dates between 2010-01-01 and 2017-08-23'
    if  start_match:
        if start_date in date_list:
            result = session.query(Measurement.tobs).filter(Measurement.date.between(start_date, end_date)).all()
            session.close()
            tmin = np.min(result)
            tmax = np.max(result)
            tavg = np.average(result)
            start_date_list = {'TMIN':tmin, 'TAVG':tavg, 'TMAX':tmax}
            return jsonify(start_date_list)
        else:
            return error_msg_2
    else:
        return error_msg_1


@app.route('/api/v1.0/<start_date>/<end_date>')
def temp_from_to_date(start_date, end_date):
    start_match = re.match(r"\d{4}\W\d{2}\W\d{2}", start_date)
    end_match = re.match(r"\d{4}\W\d{2}\W\d{2}", end_date)
    session = Session(engine)
    dates = session.query(Measurement.date).all()
    blacklist = ['(', "'", ',', ')']
    date_list = []
    for date in dates:
        new_string = ''
        for char in date:
            if char in blacklist:
                new_string += ''
            else:
                new_string += char
        date_list.append(new_string)
    error_msg_1 = 'Invalid date input.\nPlease use YYYY-MM-DD format.'
    error_msg_2 = 'Invalid date input.\nPlease input dates between 2010-01-01 and 2017-08-23'
    if start_match:
        if  end_match:
            if start_date in date_list:
                if end_date in date_list:
                    result = session.query(Measurement.tobs).filter(Measurement.date.between(start_date, end_date)).all()
                    session.close()
                    tmin = np.min(result)
                    tmax = np.max(result)
                    tavg = np.average(result)
                    date_list = {'TMIN':tmin, 'TAVG':tavg, 'TMAX':tmax}
                    return jsonify(date_list)
                else:
                    return error_msg_2
            else:
                return error_msg_2
        else:
            return error_msg_1
    else:
        return error_msg_1


if __name__ == '__main__':
    app.run(debug=True)