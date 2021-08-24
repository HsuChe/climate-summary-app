import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, query
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
    f"<h2>All Available Routes:</h2><br/>"
    f"<h2>Precipitation: /api/v1.0/precipitation</h2><br/>"
    f"<h2>List of Stations in Dataset: /api/v1.0/stations<br/>"
    f"<h2>Temperature for one year: /api/v1.0/tobs<br/>"
    f"<h2>Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
    f"<h2>Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    all_prcp = session.query(
        Measurement.date,
        Measurement.prcp
    ).all()
    session.close
    result_list = []
    for date, prcp in all_prcp:
        result = {
            'date':date,
            'precipitation':prcp, 
        }
        result_list.append(result)
    return jsonify(result_list)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(
        Station.station,
        Station.name,
        Station.longitude,
        Station.latitude,
        Station.elevation
    ).all()
    session.close
    result_list = []
    for station, name, longitude, latitude, elevation in stations:
        result = {
            'station':station,
            'name':name,
            'longitude':longitude,
            'latitude':latitude,
            'elevation':elevation
        }
        result_list.append(result)
    
    return jsonify(result_list)

@app.route("/api/v1.0/tobs")
def active_temp():
    session = Session(engine)
    active_station = session.query(
        Measurement.station
    ).group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).first()[0]
    station_info = session.query(Measurement.date,Measurement.prcp).filter(
        Measurement.station == active_station).all()
    session.close
    
    result_list = []    
    for date, prcp in station_info:
        result = {
            "date":date,
            "precipitation(in)":prcp
        }
        result_list.append(result)
    
    return jsonify(result_list)

@app.route("/api/v1.0/<start>")
def date(start):
    session = Session(engine)
    query_result = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
        ).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()
    session.close
    result_list = []
    for min, max, avg in query_result:
        result = {
            'min_temp':min,
            'max_temp':max,
            'avg_temp':avg   
        }
        result_list.append(result)
    
    return jsonify(result_list)

@app.route('/api/v1.0/<start>/<end>')
def date_range(start,end):
    
    if dt.datetime.strptime(start,"%Y-%m-%d") < dt.datetime.strptime(end,"%Y-%m-%d"):
        session = Session(engine)
        query_results = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
            ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()    
        session.close()
        result_list = []
        for min, max, avg in query_results:
            result = {
                'min_temp':min,
                'max_temp':max,
                'avg_temp':avg   
            }
            result_list.append(result)
        return jsonify(result_list)
    else:
        return "<h1>Error calculating date range</h1>"

if __name__ == '__main__':
    app.run(debug=True)