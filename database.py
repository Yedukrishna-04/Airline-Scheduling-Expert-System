from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Flight:
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    capacity: int
    cargo_capacity: float  # in tons

@dataclass
class Cargo:
    cargo_id: str
    weight: float  # in tons
    departure_airport: str
    arrival_airport: str
    priority: int  # 1 (highest) to 5 (lowest)
    deadline: datetime

class DatabaseHandler:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client['airline_scheduling']
        self.flights_collection = self.db['flights']
        self.cargo_collection = self.db['cargo']
        self.fleet_collection = self.db['fleet']
        self.airports_collection = self.db['airports']

    def initialize_database(self):
        """Initialize the database with default fleet and airport data"""
        # Initialize fleet data
        fleet_data = {
            "Boeing 737": 5,
            "Airbus A320": 3,
            "Boeing 777": 2
        }
        self.fleet_collection.delete_many({})
        self.fleet_collection.insert_one({"aircraft": fleet_data})

        # Initialize airport data with Indian cities
        airport_data = {
            "Mumbai": 50,
            "Delhi": 45,
            "Pune": 30,
            "Chennai": 40
        }
        self.airports_collection.delete_many({})
        self.airports_collection.insert_one({"airports": airport_data})

    def get_fleet_data(self) -> Dict[str, int]:
        """Retrieve fleet data from database"""
        fleet_doc = self.fleet_collection.find_one({})
        return fleet_doc["aircraft"] if fleet_doc else {}

    def get_airport_data(self) -> Dict[str, int]:
        """Retrieve airport data from database"""
        airport_doc = self.airports_collection.find_one({})
        return airport_doc["airports"] if airport_doc else {}

    def add_flight(self, flight: Flight) -> bool:
        """Add a flight to the database"""
        flight_data = {
            "flight_number": flight.flight_number,
            "departure_airport": flight.departure_airport,
            "arrival_airport": flight.arrival_airport,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "aircraft_type": flight.aircraft_type,
            "capacity": flight.capacity,
            "cargo_capacity": flight.cargo_capacity
        }
        try:
            self.flights_collection.insert_one(flight_data)
            return True
        except Exception as e:
            print(f"Error adding flight: {e}")
            return False

    def add_cargo(self, cargo: Cargo) -> bool:
        """Add a cargo request to the database"""
        cargo_data = {
            "cargo_id": cargo.cargo_id,
            "weight": cargo.weight,
            "departure_airport": cargo.departure_airport,
            "arrival_airport": cargo.arrival_airport,
            "priority": cargo.priority,
            "deadline": cargo.deadline
        }
        try:
            self.cargo_collection.insert_one(cargo_data)
            return True
        except Exception as e:
            print(f"Error adding cargo: {e}")
            return False

    def get_all_flights(self) -> List[Flight]:
        """Retrieve all flights from the database"""
        flights = []
        for flight_doc in self.flights_collection.find():
            flight = Flight(
                flight_number=flight_doc["flight_number"],
                departure_airport=flight_doc["departure_airport"],
                arrival_airport=flight_doc["arrival_airport"],
                departure_time=flight_doc["departure_time"],
                arrival_time=flight_doc["arrival_time"],
                aircraft_type=flight_doc["aircraft_type"],
                capacity=flight_doc["capacity"],
                cargo_capacity=flight_doc["cargo_capacity"]
            )
            flights.append(flight)
        return flights

    def get_all_cargo(self) -> List[Cargo]:
        """Retrieve all cargo requests from the database"""
        cargo_list = []
        for cargo_doc in self.cargo_collection.find():
            cargo = Cargo(
                cargo_id=cargo_doc["cargo_id"],
                weight=cargo_doc["weight"],
                departure_airport=cargo_doc["departure_airport"],
                arrival_airport=cargo_doc["arrival_airport"],
                priority=cargo_doc["priority"],
                deadline=cargo_doc["deadline"]
            )
            cargo_list.append(cargo)
        return cargo_list

    def update_fleet(self, fleet_data: Dict[str, int]):
        """Update fleet data in the database"""
        self.fleet_collection.delete_many({})
        self.fleet_collection.insert_one({"aircraft": fleet_data})

    def update_airports(self, airport_data: Dict[str, int]):
        """Update airport data in the database"""
        self.airports_collection.delete_many({})
        self.airports_collection.insert_one({"airports": airport_data})

    def delete_flight(self, flight_number: str) -> bool:
        """Delete a flight from the database"""
        try:
            result = self.flights_collection.delete_one({"flight_number": flight_number})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting flight: {e}")
            return False

    def delete_cargo(self, cargo_id: str) -> bool:
        """Delete a cargo request from the database"""
        try:
            result = self.cargo_collection.delete_one({"cargo_id": cargo_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting cargo: {e}")
            return False

    def close(self):
        """Close the database connection"""
        self.client.close() 