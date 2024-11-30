import erdantic as erd
from database import Station, StationMeasurements
from sqlmodel import SQLModel
from sqlalchemy_data_model_visualizer import generate_data_model_diagram

models = [Station, StationMeasurements]
generate_data_model_diagram(models, "diagram")

diagram = erd.create([Station, StationMeasurements])

# draw([Station, StationMeasurements],out="erd.png")