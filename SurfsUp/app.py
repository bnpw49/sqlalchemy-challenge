# Dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#Database Setup 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

 

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def Welcome():
    
    return(
       
f"Available Routes: <br/>"
f"/api/v1.0/precipitation <br/>"
f"/api/v1.0/stations <br/>"
f"/api/v1.0/tobs <br/>"
f"/api/v1.0/temp/<start>/<end> <br/>"
)

@app.route('/api/v1.0/precipitation')
def precip():
      #open session
    session = Session(engine)
    
#Get precipitation data for 12 months
    last_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_date).all()
    #transform into dictionary
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    stations_list = list(np.ravel(session.query(Station.station).all()))
    session.close()
    return jsonify(stations_list)

@app.route("/api/v1.0/stations")
def stations():
    stations_list = list(np.ravel(session.query(Station.station).all()))
    session.close()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def monthly_temp():
     station_data = session.query(Measurement.station,Measurement.date, Measurement.prcp, Measurement.tobs)
     station_data_df = pd.DataFrame(station_data, columns=['station','date','prcp','tobs'])
     most_active = list(np.ravel(station_data_df.loc[(station_data_df['station']=='USC00519281')]))
     session.close()
     return jsonify(most_active)
    
@app.route("/api/v1.0/temp/<start>/<end>")
def Temps(start, end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    temp_data = session.query(func.min(Measurement.tobs),\
                              func.max(Measurement.tobs), \
                              func.avg(Measurement.tobs)) \
                        .filter(Measurement.date.between(start_date, end_date)) \
                        .all()
    temp_list = list(np.ravel(temp_data))
    session.close()
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)