# SQL Alchemy Assignment

### Tropical Vacation

We will be using SQL Alchemy to analyze SQL-lite datebases. Using python, we will be constructing graphs and create custom API to enable users access to the information in the database.  

![tropics.png](Images/maldives-1993704_1920.jpg)

To do the analysis and find the results necessary to make yoru vacation a success, we would need to focus on the average temperature based on the measurement stations around the area.

## Setting up SQL Alchemy

The first thing we are going to do is to set up SQL lite. 

1. We will need to import the dependencies that we need.

```sh
  from sqlalchemy.ext.automap import automap_base
  from sqlalchemy.orm import Session
  from sqlalchem import create_engine, func, inspect
```
* First, create the engine that will link us to the database in SQL lite

```sh
  engine = create_engine("sqlite:///Resources/hawaii.sqlite")
  conn = engine.connect()
```

* The automap_base will allow us to import and map the database from SQL-lite and enable us to read the data based on classes

```sh
  Base.automap_base()
  Base.prepare(conn, reflect = True)
```
* Now we can use various auto_map functions to identify specific classes in the dataset. 

```sh
  Base.classes.key()
```

* Measurement and station will be the two classes that we are working with in the data base. From here we can isolate the data from these classes.

```sh
Measurement = Base.classes.measurement
Station = Base.classes.station
```
* We can spend some time to explore the database and see exactly what kinds of data we are working with. 

```sh
  inspector = inspect(conn)
  inspector.get_table_names()
  column_info = inspector.get_columns('measurement)
```
* column_info will have the column information in the table "measurement.
```sh
  for column in column_info:
    print(
      column['name'],
      column['tupe'],
      column['primary_key']
    )
```
* We can see all the columns which is id, station, date, prcp, and tobs. Id will be our primary key for this table and pcp/tobs are floats that we can calculate. We will do the same with the station table.

```sh
  for columns in inspector.get_columns('station'):
    print(
      columns['name'],
      columns['type'],
      columsn['primary_key']
      )
```
* The "station" table has id, station, name, latitude, logitude, elevation, and the primary key is id. Both the station and measurement tables has "station" column, so we can use that as a mechanism for joining the tables. 

* After knowing everything about the database we are working with, we can now start a connection session and query the data we need for the analysis.

```sh
  session = Session(conn)
```

### Analyzing the Precipitation Data

2. The first analysis we want to do is figure out rain in each location over the last year. 

* To begin, we can parse the date column from Measurement and query all the precipitation information we want a year from the most recent date in the dataset.

```sh
  recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
  recent_parsed = dt.datetime.strptime(recent_date,"%Y-%m-%d")
```

* Now we can parse the starting date, which will be set 1 year before the most recent time or the ending date.

```sh
  target_date = f"{recent_parsed.year - 1}-{recent_parsed.month:02}-{recent_parsed.day:02}"
```
* With the most recent date and the target date, we can construct our query parameters to extract the data that we need.

```sh
  result = session.query(Measurement).filter(func.strftime("%Y-%m-%d" , Measurement.date) > target_date).all()
```
* We now have all the information we need from the dataset. We can begin processing the precipitation data.

```sh
  precipation_list = []
  for row in result:
    precipation_list.append([row.date,row.prcp])
```
* Now we set it into a DataFrame for graphing

```sh
  preci_df = pd.DataFrame(precipation_list, columns  = ['Date','Precipitation'])
  preci_df.set_index('Date')
```
* Now we graph

```sh
  prec_df_sort.plot(figsize = (7,4))
  plt.title('Percipitation Between 2016 and 2017')
  plt.ylabel('Percipitation')
  plt.xticks(rotation = 45)
  plt.savefig("Images/precipitation.png")

  plt.show()
```

  ![precipitation](Images/precipitation.png)


### Station Analysis

3. We will now design queries to calculate specifics temperatures of the stations

* We first calculate the most active stations and that will be based upon the number of time a station produced data off of the Measurement table. We want the min, max, and avg temperature for these stations.

```sh
  station_temp = session.query(
    Measurement.station, 
    func.count(Measurement.id),
    func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)
    ).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
```
* Now we want to graph the most common temperature for the  specific station with the highest activies.

  ```sh
    active_station_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station_temp[0][0]
    ).all()
    station_df = pd.DataFrame(active_station_data, columns = ['Date','tobs'])
    station_sort = station_df.set_index('Date')
    station_sort.plot.hist(figsize = (7,4), bins = 12)
    plt.title(f' Common Temperature for Station {station_temp[0][0]}')
    plt.xlable('Temperature')
    plt.savefig('Images/active_station_info.png')

    plt.show()

  ```
 ![precipitation](Images/active_station_info.png)

  ## Bonus 1
  