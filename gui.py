import tkinter as tk

class DriverUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Driver UI")
        self.configure(bg='black')  # Use a darker background for a modern look

        # Make the window full screen
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.toggle_fullscreen)

        # Left frame for speed
        self.left_frame = tk.Frame(self, bg='black')
        self.left_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nw")

        self.speed_label = tk.Label(self.left_frame, text="Speed", font=("Helvetica", 60, 'bold'), fg="white", bg="black")
        self.speed_label.pack(anchor='w')

        # Middle frame for the vertical bar
        self.middle_frame = tk.Canvas(self, width=2, bg='white', bd=0, highlightthickness=0)
        self.middle_frame.grid(row=0, column=1, sticky="ns")

        # Right frame for SOC and other details
        self.right_frame = tk.Frame(self, bg='black')
        self.right_frame.grid(row=0, column=2, padx=40, pady=40, sticky="ne")

        self.soc_label = tk.Label(self.right_frame, text="SOC\n00V", font=("Helvetica", 36, 'bold'), fg="white", bg="black")
        self.soc_label.grid(row=0, column=0, padx=20, pady=20)

        self.intake_label = tk.Label(self.right_frame, text="Intake\n00V - 00A", font=("Helvetica", 36, 'bold'), fg="white", bg="black")
        self.intake_label.grid(row=1, column=0, padx=20, pady=20)

        self.outtake_label = tk.Label(self.right_frame, text="Outtake\n00V - 00A", font=("Helvetica", 36, 'bold'), fg="white", bg="black")
        self.outtake_label.grid(row=2, column=0, padx=20, pady=20)

        self.net_label = tk.Label(self.right_frame, text="NET\n00V - 00A", font=("Helvetica", 36, 'bold'), fg="white", bg="black")
        self.net_label.grid(row=3, column=0, padx=20, pady=20)

        # Start updating values
        self.update_values()

    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not is_fullscreen)

    def get_speed(self):
        # Replace with actual logic to get speed
        # Example: return some_sensor.read_speed()
        return "120 km/h"

    def get_soc(self):
        # Replace with actual logic to get SOC (State of Charge)
        # Example: return battery.read_voltage()
        return "72V"

    def get_intake(self):
        # Replace with actual logic to get intake voltage and current
        # Example: return f"{intake_sensor.read_voltage()}V - {intake_sensor.read_current()}A"
        return "48V - 15A"

    def get_outtake(self):
        # Replace with actual logic to get outtake voltage and current
        # Example: return f"{outtake_sensor.read_voltage()}V - {outtake_sensor.read_current()}A"
        return "48V - 10A"

    def get_net(self):
        # Replace with actual logic to get net voltage and current
        # Example: calculate the net current
        return "0V - 5A"

    def update_values(self):
        speed = self.get_speed()
        soc = self.get_soc()
        intake = self.get_intake()
        outtake = self.get_outtake()
        net = self.get_net()

        self.speed_label.config(text=f"Speed\n{speed}")
        self.soc_label.config(text=f"SOC\n{soc}")
        self.intake_label.config(text=f"Intake\n{intake}")
        self.outtake_label.config(text=f"Outtake\n{outtake}")
        self.net_label.config(text=f"NET\n{net}")

        # Update the values every second (1000 ms)
        self.after(1000, self.update_values)

if __name__ == "__main__":
    app = DriverUI()
    app.mainloop()
