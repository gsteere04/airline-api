from fastapi import FastAPI, HTTPException, status
from typing import List, Dict
from models import Flight

app = FastAPI()

airlines_data: Dict[str, List[Flight]] = {
    "Delta": [
        Flight(flight_num="DL1234", capacity=54, estimated_flight_duration=180),
        Flight(flight_num="DL5678", capacity=30, estimated_flight_duration=79)
    ],
    "Southwest": [
        Flight(flight_num="SWA3298", capacity=45, estimated_flight_duration=122),
        Flight(flight_num="SWA8002", capacity=73, estimated_flight_duration=150)
    ],
    "Alaska": [
        Flight(flight_num="AS900", capacity=60, estimated_flight_duration=140),
        Flight(flight_num="AS7230", capacity=68, estimated_flight_duration=135)
    ]
}

@app.get("/", response_model=List[str])
async def list_airlines():
    """Get a list of all airline names"""
    return list(airlines_data.keys())

@app.get("/{airline_name}", response_model=List[str])
async def list_flights(airline_name: str):
    """Get a list of all flight numbers for a specific airline"""
    airline = airlines_data.get(airline_name)
    if not airline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
    return [flight.flight_num for flight in airline]

@app.get("/{airline_name}/{flight_num}", response_model=Flight)
async def get_flight(airline_name: str, flight_num: str):
    """Get details of a specific flight"""
    airline = airlines_data.get(airline_name)
    if not airline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
    for flight in airline:
        if flight.flight_num == flight_num:
            return flight
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")

@app.post("/{airline_name}", response_model=Flight, status_code=status.HTTP_201_CREATED)
async def add_flight(airline_name: str, flight: Flight):
    """Add a new flight to a specified airline"""
    if airline_name not in airlines_data:
        airlines_data[airline_name] = []
    airlines_data[airline_name].append(flight)
    return flight

@app.put("/{airline_name}/{flight_num}", response_model=Flight)
async def update_flight(airline_name: str, flight_num: str, updated_flight: Flight):
    """Update the details of a specific flight"""
    airline = airlines_data.get(airline_name)
    if not airline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
    for i, flight in enumerate(airline):
        if flight.flight_num == flight_num:
            airlines_data[airline_name][i] = updated_flight
            return updated_flight
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")

@app.delete("/{airline_name}/{flight_num}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flight(airline_name: str, flight_num: str):
    """Delete a specific flight from an airline"""
    airline = airlines_data.get(airline_name)
    if not airline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
    for i, flight in enumerate(airline):
        if flight.flight_num == flight_num:
            del airlines_data[airline_name][i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
