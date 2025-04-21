import tkinter as tk
from tkinter import ttk, messagebox
from expert_system import AirlineSchedulingExpertSystem, Flight, Cargo
import datetime

class AirlineSchedulingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Scheduling Expert System")
        self.root.geometry("1200x800")
        
        # Initialize the expert system
        self.expert_system = AirlineSchedulingExpertSystem()
        
        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.flights_frame = ttk.Frame(self.notebook)
        self.cargo_frame = ttk.Frame(self.notebook)
        self.schedule_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.flights_frame, text='Flights')
        self.notebook.add(self.cargo_frame, text='Cargo')
        self.notebook.add(self.schedule_frame, text='Schedule Analysis')
        self.notebook.add(self.settings_frame, text='Settings')
        
        # Initialize each tab
        self.setup_flights_tab()
        self.setup_cargo_tab()
        self.setup_schedule_tab()
        self.setup_settings_tab()
        
        # Load initial data
        self.refresh_flight_list()
        self.refresh_cargo_list()

    def setup_flights_tab(self):
        # Flight Entry Form
        entry_frame = ttk.LabelFrame(self.flights_frame, text="Add New Flight", padding=10)
        entry_frame.pack(fill='x', padx=5, pady=5)

        # Flight Number
        ttk.Label(entry_frame, text="Flight Number:").grid(row=0, column=0, padx=5, pady=5)
        self.flight_number = ttk.Entry(entry_frame)
        self.flight_number.grid(row=0, column=1, padx=5, pady=5)

        # Departure Airport
        ttk.Label(entry_frame, text="Departure Airport:").grid(row=1, column=0, padx=5, pady=5)
        self.departure_airport = ttk.Combobox(entry_frame, values=list(self.expert_system.get_airport_data().keys()))
        self.departure_airport.grid(row=1, column=1, padx=5, pady=5)

        # Arrival Airport
        ttk.Label(entry_frame, text="Arrival Airport:").grid(row=2, column=0, padx=5, pady=5)
        self.arrival_airport = ttk.Combobox(entry_frame, values=list(self.expert_system.get_airport_data().keys()))
        self.arrival_airport.grid(row=2, column=1, padx=5, pady=5)

        # Aircraft Type
        ttk.Label(entry_frame, text="Aircraft Type:").grid(row=3, column=0, padx=5, pady=5)
        self.aircraft_type = ttk.Combobox(entry_frame, values=list(self.expert_system.get_fleet_data().keys()))
        self.aircraft_type.grid(row=3, column=1, padx=5, pady=5)

        # Capacity
        ttk.Label(entry_frame, text="Passenger Capacity:").grid(row=4, column=0, padx=5, pady=5)
        self.capacity = ttk.Entry(entry_frame)
        self.capacity.grid(row=4, column=1, padx=5, pady=5)

        # Cargo Capacity
        ttk.Label(entry_frame, text="Cargo Capacity (tons):").grid(row=5, column=0, padx=5, pady=5)
        self.cargo_capacity = ttk.Entry(entry_frame)
        self.cargo_capacity.grid(row=5, column=1, padx=5, pady=5)

        # Add Flight Button
        ttk.Button(entry_frame, text="Add Flight", command=self.add_flight).grid(row=6, column=0, columnspan=2, pady=10)

        # Flight List
        list_frame = ttk.LabelFrame(self.flights_frame, text="Current Flights", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Create Treeview
        columns = ('Flight Number', 'Departure', 'Arrival', 'Aircraft', 'Capacity', 'Cargo Capacity')
        self.flight_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.flight_tree.heading(col, text=col)
            self.flight_tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.flight_tree.yview)
        self.flight_tree.configure(yscrollcommand=scrollbar.set)
        
        self.flight_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add delete button
        ttk.Button(list_frame, text="Delete Selected", command=self.delete_selected_flight).pack(pady=5)

    def setup_cargo_tab(self):
        # Cargo Entry Form
        entry_frame = ttk.LabelFrame(self.cargo_frame, text="Add New Cargo Request", padding=10)
        entry_frame.pack(fill='x', padx=5, pady=5)

        # Cargo ID
        ttk.Label(entry_frame, text="Cargo ID:").grid(row=0, column=0, padx=5, pady=5)
        self.cargo_id = ttk.Entry(entry_frame)
        self.cargo_id.grid(row=0, column=1, padx=5, pady=5)

        # Weight
        ttk.Label(entry_frame, text="Weight (tons):").grid(row=1, column=0, padx=5, pady=5)
        self.weight = ttk.Entry(entry_frame)
        self.weight.grid(row=1, column=1, padx=5, pady=5)

        # Departure Airport
        ttk.Label(entry_frame, text="Departure Airport:").grid(row=2, column=0, padx=5, pady=5)
        self.cargo_departure = ttk.Combobox(entry_frame, values=list(self.expert_system.get_airport_data().keys()))
        self.cargo_departure.grid(row=2, column=1, padx=5, pady=5)

        # Arrival Airport
        ttk.Label(entry_frame, text="Arrival Airport:").grid(row=3, column=0, padx=5, pady=5)
        self.cargo_arrival = ttk.Combobox(entry_frame, values=list(self.expert_system.get_airport_data().keys()))
        self.cargo_arrival.grid(row=3, column=1, padx=5, pady=5)

        # Priority
        ttk.Label(entry_frame, text="Priority (1-5):").grid(row=4, column=0, padx=5, pady=5)
        self.priority = ttk.Spinbox(entry_frame, from_=1, to=5)
        self.priority.grid(row=4, column=1, padx=5, pady=5)

        # Add Cargo Button
        ttk.Button(entry_frame, text="Add Cargo Request", command=self.add_cargo).grid(row=5, column=0, columnspan=2, pady=10)

        # Cargo List
        list_frame = ttk.LabelFrame(self.cargo_frame, text="Current Cargo Requests", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Create Treeview
        columns = ('Cargo ID', 'Weight', 'Departure', 'Arrival', 'Priority', 'Deadline')
        self.cargo_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.cargo_tree.heading(col, text=col)
            self.cargo_tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.cargo_tree.yview)
        self.cargo_tree.configure(yscrollcommand=scrollbar.set)
        
        self.cargo_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add delete button
        ttk.Button(list_frame, text="Delete Selected", command=self.delete_selected_cargo).pack(pady=5)

    def setup_schedule_tab(self):
        # Analysis Frame
        analysis_frame = ttk.LabelFrame(self.schedule_frame, text="Schedule Analysis", padding=10)
        analysis_frame.pack(fill='x', padx=5, pady=5)

        # Analysis Buttons
        ttk.Button(analysis_frame, text="Check Conflicts", command=self.show_conflicts).pack(fill='x', pady=5)
        ttk.Button(analysis_frame, text="Optimize Cargo", command=self.show_cargo_optimization).pack(fill='x', pady=5)
        ttk.Button(analysis_frame, text="Get Suggestions", command=self.show_suggestions).pack(fill='x', pady=5)

        # Results Frame
        results_frame = ttk.LabelFrame(self.schedule_frame, text="Analysis Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Text widget for displaying results
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=20)
        self.results_text.pack(fill='both', expand=True)

    def setup_settings_tab(self):
        # Fleet Settings
        fleet_frame = ttk.LabelFrame(self.settings_frame, text="Fleet Management", padding=10)
        fleet_frame.pack(fill='x', padx=5, pady=5)

        # Create entries for each aircraft type
        self.fleet_entries = {}
        row = 0
        for aircraft, count in self.expert_system.get_fleet_data().items():
            ttk.Label(fleet_frame, text=f"{aircraft}:").grid(row=row, column=0, padx=5, pady=5)
            entry = ttk.Entry(fleet_frame)
            entry.insert(0, str(count))
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.fleet_entries[aircraft] = entry
            row += 1

        # Airport Settings
        airport_frame = ttk.LabelFrame(self.settings_frame, text="Airport Management", padding=10)
        airport_frame.pack(fill='x', padx=5, pady=5)

        # Create entries for each airport
        self.airport_entries = {}
        row = 0
        for airport, capacity in self.expert_system.get_airport_data().items():
            ttk.Label(airport_frame, text=f"{airport} Capacity:").grid(row=row, column=0, padx=5, pady=5)
            entry = ttk.Entry(airport_frame)
            entry.insert(0, str(capacity))
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.airport_entries[airport] = entry
            row += 1

        # Save Settings Button
        ttk.Button(self.settings_frame, text="Save Settings", command=self.save_settings).pack(pady=10)

    def refresh_flight_list(self):
        # Clear existing items
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)
        
        # Add all flights from the expert system
        for flight in self.expert_system.flights:
            self.flight_tree.insert('', 'end', values=(
                flight.flight_number,
                flight.departure_airport,
                flight.arrival_airport,
                flight.aircraft_type,
                flight.capacity,
                flight.cargo_capacity
            ))

    def refresh_cargo_list(self):
        # Clear existing items
        for item in self.cargo_tree.get_children():
            self.cargo_tree.delete(item)
        
        # Add all cargo from the expert system
        for cargo in self.expert_system.cargo_requests:
            self.cargo_tree.insert('', 'end', values=(
                cargo.cargo_id,
                cargo.weight,
                cargo.departure_airport,
                cargo.arrival_airport,
                cargo.priority,
                cargo.deadline
            ))

    def add_flight(self):
        try:
            flight = Flight(
                flight_number=self.flight_number.get(),
                departure_airport=self.departure_airport.get(),
                arrival_airport=self.arrival_airport.get(),
                departure_time=datetime.datetime.now(),
                arrival_time=datetime.datetime.now() + datetime.timedelta(hours=6),
                aircraft_type=self.aircraft_type.get(),
                capacity=int(self.capacity.get()),
                cargo_capacity=float(self.cargo_capacity.get())
            )

            if self.expert_system.add_flight(flight):
                self.refresh_flight_list()
                messagebox.showinfo("Success", "Flight added successfully!")
            else:
                messagebox.showerror("Error", "Flight could not be added. Check for conflicts.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def add_cargo(self):
        try:
            cargo = Cargo(
                cargo_id=self.cargo_id.get(),
                weight=float(self.weight.get()),
                departure_airport=self.cargo_departure.get(),
                arrival_airport=self.cargo_arrival.get(),
                priority=int(self.priority.get()),
                deadline=datetime.datetime.now() + datetime.timedelta(days=1)
            )
            if self.expert_system.add_cargo(cargo):
                messagebox.showinfo("Success", "Cargo request added successfully!")
                self.refresh_cargo_list()
                # Clear the form
                self.cargo_id.delete(0, tk.END)
                self.weight.delete(0, tk.END)
                self.cargo_departure.set('')
                self.cargo_arrival.set('')
                self.priority.set(1)
            else:
                messagebox.showerror("Error", "Failed to add cargo request")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_selected_flight(self):
        selected_item = self.flight_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a flight to delete")
            return
        
        flight_number = self.flight_tree.item(selected_item[0])['values'][0]
        if self.expert_system.delete_flight(flight_number):
            self.refresh_flight_list()
            messagebox.showinfo("Success", "Flight deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete flight")

    def delete_selected_cargo(self):
        selected_item = self.cargo_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a cargo request to delete")
            return
        
        cargo_id = self.cargo_tree.item(selected_item[0])['values'][0]
        if self.expert_system.delete_cargo(cargo_id):
            self.refresh_cargo_list()
            messagebox.showinfo("Success", "Cargo request deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete cargo request")

    def save_settings(self):
        try:
            # Update fleet data
            new_fleet_data = {}
            for aircraft, entry in self.fleet_entries.items():
                new_fleet_data[aircraft] = int(entry.get())
            self.expert_system.db.update_fleet(new_fleet_data)

            # Update airport data
            new_airport_data = {}
            for airport, entry in self.airport_entries.items():
                new_airport_data[airport] = int(entry.get())
            self.expert_system.db.update_airports(new_airport_data)

            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def show_conflicts(self):
        # This method is no longer needed as we check conflicts when adding flights
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Flight conflicts are checked automatically when adding flights.")

    def show_cargo_optimization(self):
        allocations = self.expert_system.optimize_cargo_allocation()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Cargo Allocations:\n\n")
        for flight_number, cargo_list in allocations.items():
            self.results_text.insert(tk.END, f"Flight {flight_number}:\n")
            for cargo in cargo_list:
                self.results_text.insert(tk.END, 
                    f"  - Cargo {cargo.cargo_id}: {cargo.weight} tons\n")

    def show_suggestions(self):
        suggestions = self.expert_system.suggest_improvements()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Schedule Improvement Suggestions:\n\n")
        for suggestion in suggestions:
            self.results_text.insert(tk.END, f"• {suggestion}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineSchedulingGUI(root)
    root.mainloop() 