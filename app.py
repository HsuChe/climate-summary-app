import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(conn, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
         f"Available Routes:<br/>"
        f"Precipitation Information: /api/v1.0/precipitation<br/>"
        f"List of Stations in the Dataset: /api/v1.0/stations<br/>"
        f"Temperature - Year: /api/v1.0/tobs<br/>"
        f"Temperature stat from Certain Starting Date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from Range of Dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
        )

@app.route("/api/v1.0/<query_date>")
def get_query(query_date):
    session = Session(conn)
    query_result = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= query).all()
    session.close()
    
    for min, avg, max in query_result:
        print(min,avg,max)
    
    return jsonify(query_result)




if __name__ == '__main__':
    app.run(debug=True)