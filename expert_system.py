from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database import Flight, Cargo, DatabaseHandler

class AirlineSchedulingExpertSystem:
    def __init__(self):
        self.db = DatabaseHandler()
        self.db.initialize_database()
        self.flights = []
        self.cargo_requests = []
        self.load_data()

    def load_data(self):
        """Load data from the database"""
        self.flights = self.db.get_all_flights()
        self.cargo_requests = self.db.get_all_cargo()

    def get_airport_data(self) -> Dict[str, int]:
        """Get airport capacity data"""
        return self.db.get_airport_data()

    def get_fleet_data(self) -> Dict[str, int]:
        """Get fleet data"""
        return self.db.get_fleet_data()

    def add_flight(self, flight: Flight) -> bool:
        """Add a new flight to the system"""
        if self.db.add_flight(flight):
            self.flights.append(flight)
            return True
        return False

    def add_cargo(self, cargo: Cargo) -> bool:
        """Add a new cargo request to the system"""
        if self.db.add_cargo(cargo):
            self.cargo_requests.append(cargo)
            return True
        return False

    def check_flight_feasibility(self, flight: Flight) -> bool:
        """Check if a flight is feasible based on various constraints"""
        # Check if departure time is before arrival time
        if flight.departure_time >= flight.arrival_time:
            return False

        # Check if the aircraft type exists in the fleet
        fleet_data = self.db.get_fleet_data()
        if flight.aircraft_type not in fleet_data:
            return False

        # Check if airports exist
        airport_data = self.db.get_airport_data()
        if flight.departure_airport not in airport_data or flight.arrival_airport not in airport_data:
            return False

        # Check for scheduling conflicts
        for existing_flight in self.flights:
            if existing_flight.flight_number == flight.flight_number:
                return False
            if existing_flight.aircraft_type == flight.aircraft_type:
                if (flight.departure_time <= existing_flight.arrival_time and 
                    flight.arrival_time >= existing_flight.departure_time):
                    return False

        return True

    def optimize_cargo_allocation(self) -> Dict[str, List[Cargo]]:
        """Optimize cargo allocation across available flights"""
        allocation = {}
        unallocated_cargo = self.cargo_requests.copy()
        
        # Sort cargo by priority (1 is highest)
        unallocated_cargo.sort(key=lambda x: x.priority)
        
        for flight in self.flights:
            available_capacity = flight.cargo_capacity
            allocation[flight.flight_number] = []
            
            for cargo in unallocated_cargo[:]:
                if (cargo.departure_airport == flight.departure_airport and
                    cargo.arrival_airport == flight.arrival_airport and
                    cargo.weight <= available_capacity and
                    cargo.deadline >= flight.arrival_time):
                    allocation[flight.flight_number].append(cargo)
                    available_capacity -= cargo.weight
                    unallocated_cargo.remove(cargo)
        
        return allocation

    def suggest_improvements(self) -> List[str]:
        """Suggest improvements for the current schedule"""
        suggestions = []
        
        # Check fleet utilization
        fleet_data = self.db.get_fleet_data()
        for aircraft_type, count in fleet_data.items():
            aircraft_flights = [f for f in self.flights if f.aircraft_type == aircraft_type]
            if len(aircraft_flights) < count * 0.7:  # Less than 70% utilization
                suggestions.append(f"Consider increasing flights for {aircraft_type} to improve fleet utilization")
        
        # Check cargo capacity utilization
        for flight in self.flights:
            allocation = self.optimize_cargo_allocation()
            if flight.flight_number in allocation:
                total_cargo = sum(cargo.weight for cargo in allocation[flight.flight_number])
                if total_cargo < flight.cargo_capacity * 0.5:  # Less than 50% cargo capacity used
                    suggestions.append(f"Flight {flight.flight_number} has low cargo capacity utilization")
        
        return suggestions

    def delete_flight(self, flight_number: str) -> bool:
        """Delete a flight from the system"""
        if self.db.delete_flight(flight_number):
            # Reload data from the database
            self.load_data()
            return True
        return False

    def delete_cargo(self, cargo_id: str) -> bool:
        """Delete a cargo request from the system"""
        if self.db.delete_cargo(cargo_id):
            # Reload data from the database
            self.load_data()
            return True
        return False

    def close(self):
        """Close the database connection"""
        self.db.close()

# Example usage
if __name__ == "__main__":
    # Initialize the expert system
    expert_system = AirlineSchedulingExpertSystem()
    
    # Example flight
    flight = Flight(
        flight_number="AA101",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.now(),
        arrival_time=datetime.now() + timedelta(hours=6),
        aircraft_type="Boeing 737",
        capacity=180,
        cargo_capacity=20.0
    )
    
    # Add the flight
    expert_system.add_flight(flight)
    
    # Example cargo request
    cargo = Cargo(
        cargo_id="C001",
        weight=5.0,
        departure_airport="JFK",
        arrival_airport="LAX",
        priority=1,
        deadline=datetime.now() + timedelta(days=1)
    )
    
    # Add the cargo request
    expert_system.add_cargo(cargo)
    
    # Get cargo allocations
    allocations = expert_system.optimize_cargo_allocation()
    
    # Get improvement suggestions
    suggestions = expert_system.suggest_improvements()
    
    print("Cargo Allocations:", allocations)
    print("Improvement Suggestions:", suggestions)
