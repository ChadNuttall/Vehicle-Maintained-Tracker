import tkinter as tk
from tkinter import messagebox
import pickle

class VehicleMaintenanceTracker:
    def __init__(self, master):
        self.master = master

        # Color Palette
        bg_color = "#606c38"
        button_color = "#dda15e"
        entry_color = "#fefae0"

        self.master.configure(bg=bg_color)

        # Vehicle Image
        vehicle_image = tk.PhotoImage(file="car.png")

        # Create a label to display Vehicle Name
        self.vehicle_name = tk.StringVar()
        self.vehicle_name.set("Licence # CP30")  # Default vehicle name
        self.vehicle_name_label = tk.Label(master, textvariable=self.vehicle_name, bg=bg_color, font=("TkDefaultFont", 10, "underline"))
        self.vehicle_name_label.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=4)

        # Create an entry box for entering the new vehicle name
        self.new_name_entry = tk.Entry(master, bg=entry_color)
        self.new_name_entry.grid(row=1, column=0, padx=10, pady=(5, 10), columnspan=4)

        # Create a button to change the vehicle name
        self.change_name_button = tk.Button(master, text="Change Vehicle Name", command=self.change_vehicle_name, bg=button_color)
        self.change_name_button.grid(row=2, column=1, pady=10, padx=(10, 10), columnspan=2)

        # Create a label to display Vehicle image
        self.vehicle_label = tk.Label(master, image=vehicle_image, bg=bg_color)
        self.vehicle_label.image = vehicle_image
        self.vehicle_label.grid(row=3, column=0, pady=(5, 10), columnspan=4)

        # Create a label to display Current Miles
        self.miles_label = tk.Label(master, text="Current Miles:", bg=bg_color, font=("TkDefaultFont", 12, "underline"))
        self.miles_label.grid(row=4, column=0, padx=10, pady=10, columnspan=4)

        # Create a label to give instructions
        self.miles_instruction_label = tk.Label(master, text="Enter the at what miles maintenance was completed:", bg=bg_color)
        self.miles_instruction_label.grid(row=5, column=0, padx=10, pady=3, columnspan=4)

        # Create an entry box for miles to be entered
        self.miles_entry = tk.Entry(master, bg=entry_color)
        self.miles_entry.grid(row=6, column=0, padx=10, pady=(3, 10), columnspan=4)

        # Create a button to Track Oil Change
        self.track_oil_button = tk.Button(master, text="Track Oil Change", command=self.track_oil_change, bg=button_color)
        self.track_oil_button.grid(row=7, column=1, pady=10, padx=(10, 5))

        # Create a button to Track Vehicle Wash
        self.track_wash_button = tk.Button(master, text="Track Vehicle Wash", command=self.track_wash, bg=button_color)
        self.track_wash_button.grid(row=7, column=2, pady=10, padx=(5, 10))

        # Create a button to Generate a Report for Oil
        self.report_oil_button = tk.Button(master, text="Generate Oil Report", command=self.generate_oil_report, bg=button_color)
        self.report_oil_button.grid(row=9, column=1, pady=10)

        # Create a button to Generate a Report for Wash
        self.report_wash_button = tk.Button(master, text="Generate Wash Report", command=self.generate_wash_report, bg=button_color)
        self.report_wash_button.grid(row=9, column=2, pady=10)

        # Create a label for Vehicle History
        self.report_label = tk.Label(master, text="Vehicle History:", bg=bg_color, font=("TkDefaultFont", 12, "underline"))
        self.report_label.grid(row=10, column=0, pady=(10, 3), columnspan=4)

        # Create a text box to display Vehicle History
        self.history_text = tk.Text(master, height=5, width=70, bg=entry_color)
        self.history_text.grid(row=11, column=0,padx=20, pady=(3, 10), columnspan=4)

        self.oil_changes = self.load_maintenance()
        self.vehicle_wash = self.load_maintenance()

        self.update_history()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def change_vehicle_name(self):
        new_name = self.new_name_entry.get()
        if new_name:
            self.vehicle_name.set(new_name)

    def track_oil_change(self):
        try:
            # Determine when the next oil Change should be done.
            current_miles = float(self.miles_entry.get())
            next_oil_change = current_miles + 5000  # https://www.aaa.com/autorepair/articles/how-often-should-you-change-engine-oil

            self.oil_changes.append((current_miles, next_oil_change))
            self.update_history()

            messagebox.showinfo("Oil Change Tracking", f"Next oil change should be at {next_oil_change} miles.")
        # Error message
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for current miles.")

    def track_wash(self):
        try:
            # Determine when the next vehicle wash should be done.
            current_miles = float(self.miles_entry.get())
            next_wash = current_miles + 600  # https://www.alfaromeousaofgreer.com/research/how-often-should-you-wash-your-car-in-winter.htm#:~:text=While%20your%20vehicle%20might%20feel,car%20in%20tip%2Dtop%20shape.
            # https://www.agilerates.com/advice/auto/average-miles-driven-per-year/

            self.vehicle_wash.append((current_miles, next_wash))
            self.update_history()

            messagebox.showinfo("Vehicle Wash Tracking", f"Next Vehicle wash should be at {next_wash} miles.")
        # Error message
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for current miles.")

    # Generate report (oil Change)
    def generate_oil_report(self):
        if not self.oil_changes:
            messagebox.showinfo("Vehicle Maintenance Report", "No maintenance has been tracked.")
        else:
            report_oil_text = "\n".join([f"Change {i}: {oil_change[0]} miles, Next: {oil_change[1]} miles" for i, oil_change in enumerate(self.oil_changes, start=1)])
            messagebox.showinfo("Maintenance Report", report_oil_text)

    # Generate report (vehicle wash)
    def generate_wash_report(self):
        if not self.vehicle_wash:
            messagebox.showinfo("Vehicle Maintenance Report", "No maintenance has been tracked.")
        else:
            report_wash_text = "\n".join([f"Wash {i}: {next_wash[0]} miles, Next: {next_wash[1]} miles" for i, next_wash in enumerate(self.vehicle_wash, start=1)])
            messagebox.showinfo("Maintenance Report", report_wash_text)

    # Update history with new data
    def update_history(self):
        self.history_text.delete(1.0, tk.END)  # Clear the existing text
        for i, oil_change in enumerate(self.oil_changes, start=1):
            self.history_text.insert(tk.END, f"Change {i}: {oil_change[0]} miles, Next: {oil_change[1]} miles\n")
        for i, next_wash in enumerate(self.vehicle_wash, start=1):
            self.history_text.insert(tk.END, f"Wash {i}: {next_wash[0]} miles, Next: {next_wash[1]} miles\n")

    # Load data from pickle file
    def load_maintenance(self):
        try:
            with open("maintenance.pkl", "rb") as file:
                data = pickle.load(file)
                if "vehicle_name" in data:
                    self.vehicle_name.set(data["vehicle_name"])
                    del data["vehicle_name"]
                return data
        except (FileNotFoundError, EOFError):
            return {}

    # Save History
    def save_oil_changes(self):
        data = {"vehicle_name": self.vehicle_name.get(), "oil_changes": self.oil_changes, "vehicle_wash": self.vehicle_wash}
        with open("maintenance.pkl", "wb") as file:
            pickle.dump(data, file)

    def on_close(self):
        self.save_oil_changes()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleMaintenanceTracker(root)
    root.mainloop()
