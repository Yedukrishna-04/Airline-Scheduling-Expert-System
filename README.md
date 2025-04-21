# Airline Scheduling Expert System

An expert system for airline scheduling that helps manage flights, cargo, and optimize schedules.

## Features

- **Flight Management**: Add, view, and delete flights between airports
- **Cargo Management**: Add, view, and delete cargo requests
- **Schedule Analysis**: Optimize cargo allocation and get improvement suggestions
- **Settings Management**: Configure fleet and airport data

## Technologies Used

- Python
- Tkinter (GUI)
- MongoDB (Database)
- Dataclasses

## Installation

1. Clone the repository:
```
git clone https://github.com/Yedukrishna-04/Airline-Scheduling-Expert-System.git
cd Airline-Scheduling-Expert-System
```

2. Install dependencies:
```
pip install pymongo
```

3. Make sure MongoDB is running on your system

4. Run the application:
```
python gui.py
```

## Project Structure

- `expert_system.py`: Core business logic for the expert system
- `database.py`: Database operations and data models
- `gui.py`: Graphical user interface 