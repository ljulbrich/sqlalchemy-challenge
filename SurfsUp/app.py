# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import text


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine('sqlite:///../Resources/hawaii.sqlite')

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
@app.rout('/')
def home():
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start-date>"
        f"/api/v1.0/<start-date>/<end-date>"
    )

@app.rout("/api/v1.0/precipitation")
def precipitation():
    start_date = "2016-08-23"
    end_date = "2017-08-23"
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(start_date, end_date)).all()
    session.close()
    measurement_list = [{'date':date, 'precipitation':prcp} for date, prcp in results]
    return jsonify(measurement_list)

@app.rout("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    station_list = [{'station':station, 'name':name, 'latitude':latitude, 'longitude':longitude, 'elevation':elevation}
                     for station, name, latitude, longitude, elevation in results]
    return jsonify(station_list)

@app.rout('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()
    session.close()
    tobs_list = [{'date':date, 'tobs':tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.rout('/api/v1.0/<start-date>')
def 

if __name__ == '__main__':
    app.run(debug=True)