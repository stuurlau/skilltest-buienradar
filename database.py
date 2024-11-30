from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from dateutil import parser

import urllib.request, json 


class StationMeasurements(SQLModel, table=True):

    __tablename__ = "_station measurements_"

    ## Apparently not all stations have the same measurements (some only do wind measurements)

    measurementid : int | None = Field(default=None, primary_key=True)
    timestamp : datetime = Field(default=None, nullable=False)
    temperature : float = Field(nullable=True)
    groundtemperature : float = Field(nullable=True)
    feeltemperature : float = Field(nullable=True)
    windgusts : float = Field(nullable=True)
    windspeedBft : int = Field(nullable=True)
    humidity : int = Field(nullable=True)
    precipitation : float = Field(nullable=True)
    sunpower : int = Field(nullable=True)
    stationid : int = Field(nullable=False , foreign_key="_weather stations_.stationid")


class Station(SQLModel, table=True):

    __tablename__ = "_weather stations_"

    stationid : int | None = Field(default=None, primary_key=True)
    stationname : str = Field(nullable=False)
    lat : float = Field(nullable=False)
    lon : float = Field(nullable=False)
    regio : str = Field(nullable=False)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def fetch_measurement_data():

    with urllib.request.urlopen("https://json.buienradar.nl") as url:
        data = json.load(url)
        measurement_data = data["actual"]["stationmeasurements"]
        with Session(engine) as session:
            for raw_measurement in measurement_data:
                print(raw_measurement)

                measurement = StationMeasurements(
                    # should look 
                    timestamp= parser.parse(raw_measurement.get("timestamp")),
                    temperature= raw_measurement.get("temperature"),
                    groundtemperature= raw_measurement.get("groundtemperature"),
                    feeltemperature= raw_measurement.get("feeltemperature"),
                    windgusts= raw_measurement.get("windgusts"),
                    windspeedBft= raw_measurement.get("windspeedBft"),
                    humidity= raw_measurement.get("humidity"),
                    precipitation= raw_measurement.get("precipitation"),
                    sunpower= raw_measurement.get("sunpower"),
                    stationid= raw_measurement.get("stationid"),
                )
                session.add(measurement)

            session.commit()


def fetch_stations():

    #check if table pupulated
    current_data = read_table(Station)

    if len(current_data) > 0:
        return

    with urllib.request.urlopen("https://json.buienradar.nl") as url:
        data = json.load(url)
        station_data = data["actual"]["stationmeasurements"]
        with Session(engine) as session:
            for raw_station in station_data:
                station = Station(
                    stationid= int(raw_station["stationid"]),
                    stationname= raw_station["stationname"],
                    lat= float(raw_station["lat"]),
                    lon= float(raw_station["lon"]),
                    regio= raw_station["regio"],
                )
                session.add(station)

            session.commit()


def read_table(table: Annotated[SQLModel, Query(description="The table to read")]):
    with Session(engine) as session:
        statement = select(table)
        rows = session.exec(statement)
        return rows.all()
        
def main():
    create_db_and_tables()
    fetch_stations()
    fetch_measurement_data()
    print(read_table(Station))



if __name__ == "__main__":
    main()