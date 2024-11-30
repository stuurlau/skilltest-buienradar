from sqlmodel import Field, Session, SQLModel, create_engine, select
from database import Station, StationMeasurements

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

#Question 5: Which weather station recorded the highest temperature?

with Session(engine) as session:
    sorted_items = session.exec(select(StationMeasurements).order_by(StationMeasurements.temperature)).all()
    highest_temp = sorted_items[-1]
    station = session.exec(select(Station).where(Station.stationid == highest_temp.stationid)).first()
    session.close()

print("Hightest temperature recorded : ",highest_temp.temperature," at Station : " ,station.stationname)

#Question 6: What is the average temperature?

with Session(engine) as session:
    items = session.exec(select(StationMeasurements)).all()
    total_temp = 0
    for item in items:
        if item.temperature is not None:
            total_temp += item.temperature
    avg_temp = total_temp / len(items)
    session.close()

print("Average temperature recorded : ",avg_temp)

#Question 7: What is the station with the biggest difference between feel temperature and the actual temperature?

with Session(engine) as session:
    items = session.exec(select(StationMeasurements)).all()
    max_diff = 0
    station = None
    for item in items:
        if item.feeltemperature is not None and item.temperature is not None:
            diff = abs(item.feeltemperature - item.temperature)
            if diff > max_diff:
                max_diff = diff
                station = session.exec(select(Station).where(Station.stationid == item.stationid)).first()
        session.close()

print("Station with the biggest difference between feel temperature and the actual temperature : ",station.stationname, " with a difference of : ",max_diff)

#Question 8: Which weather station is located in the North Sea?

with Session(engine) as session:
    stations_in_sea = []
    items = session.exec(select(Station)).all()
    for item in items:
        if "zee" in item.regio.lower():
            print(item.stationname)
            stations_in_sea.append(item.stationname)
            break
    session.close()

print("Weather stations located in the North Sea : ")
for station in stations_in_sea:
    print(station)
