import csv
import tkinter as tk

# Task A: Input Validation
# Finding leap year
def is_leap_year(year):
    """Check if a given year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def validate_date_input():
    while True:
        print("\n ******************************************************************* ", end="\n\n")
        # Get the Day
        while True:
            try:
                Day = int(input("Please enter the day of the survey in the format DD: "))
                if 1 <= Day <= 31:
                    break
                else:
                    print("Out of range - day values must be between 1 and 31.")
            except ValueError:
                print("Invalid input. Please enter an integer for the day.")

        # Get the Month
        while True:
            try:
                Month = int(input("Please enter the month of the survey in the format MM: "))
                if 1 <= Month <= 12:
                    break
                else:
                    print("Out of range - month values must be between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter an integer for the month.")

        # Get the Year
        while True:
            try:
                Year = int(input("Please enter the year of the survey in the format YYYY: "))
                if 2000 <= Year <= 2024:
                    break
                else:
                    print("Out of range - year values must be between 2000 and 2024.")
            except ValueError:
                print("Invalid input. Please enter an integer for the year.")

        # Finding days finishing in months
        if Month in [4, 6, 9, 11] and Day > 30:
            print(f"Invalid date - month {Month} cannot have more than 30 days.")
            continue
        if Month == 2:
            if is_leap_year(Year) and Day > 29:
                print(f"Invalid date - February in a leap year ({Year}) cannot have more than 29 days.")
                continue
            elif not is_leap_year(Year) and Day > 28:
                print(f"Invalid date - February in a non-leap year ({Year}) cannot have more than 28 days.")
                continue
        
        return Day, Month, Year

# Task B: Processed Outcomes
# Declare variables
def process_csv_data(file_path):
    traffic_data = {}
    
    # Open and process CSV data
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row[0] == "JunctionName" or len(row) != 10:
                    continue
                
                JunctionName, Date, timeOfDay, travel_Direction_in, travel_Direction_out, Weather_Conditions, JunctionSpeedLimit, VehicleSpeed, VehicleType, electricHybrid = row
                
                # Extract hour from timeOfDay (assumes time format is HH:MM)
                try:
                    hour = int(timeOfDay.split(":")[0])
                except ValueError:
                    continue
                
                if JunctionName not in traffic_data:
                    traffic_data[JunctionName] = {i: 0 for i in range(24)}  # Initialize hourly counts for each junction
                
                traffic_data[JunctionName][hour] += 1  # Increment count for the hour

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
    return traffic_data

# New function to process the traffic data and generate outcomes
def generate_outcomes(traffic_data):
    outcomes = {
        'total_vehicles': 0,
        'total_trucks': 0,
        'total_evs': 0,
        'total_two_wheelers': 0,
        'total_buses_north': 0,
        'total_no_turns': 0,
        'total_rain_hours': 0,
        'total_over_speed': 0,
        'total_elm_rabbit': 0,
        'total_hanley_westway': 0,
        'percentage_trucks': 0,
        'average_bicycles_per_hour': 0,
        'percentage_scooter': 0,
        'peak_hour_vehicles_hanley': 0,
        'peak_hours': [],
    }

    # Iterate through each junction's data
    for junction, hourly_data in traffic_data.items():
        for hour, count in hourly_data.items():
            outcomes['total_vehicles'] += count
            
            # Example of vehicle type checks, adjust based on your CSV columns
            # You can modify this to classify based on actual VehicleType and other conditions
            if 'truck' in junction.lower():  # Simplified example
                outcomes['total_trucks'] += count
            if 'electric' in junction.lower():
                outcomes['total_evs'] += count
            if 'two-wheeler' in junction.lower():
                outcomes['total_two_wheelers'] += count

    # For simplicity, other categories like buses, over speed vehicles, and more can be handled similarly
    # If specific categories need to be checked, extend this loop with conditions based on your data

    # Additional calculations
    outcomes['percentage_trucks'] = (outcomes['total_trucks'] / outcomes['total_vehicles']) * 100 if outcomes['total_vehicles'] > 0 else 0
    outcomes['average_bicycles_per_hour'] = outcomes['total_vehicles'] // 24

    return outcomes

# printing lines
def display_outcomes(outcomes, file_name):
    output_lines = [
        "\n *******************************************************************\n ",
        f"Data file selected is {file_name}",
        "\n *******************************************************************\n ",
        f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}",
        f"The total number of trucks recorded for this date is {outcomes['total_trucks']}",
        f"The total number of electric vehicles for this date is {outcomes['total_evs']}",
        f"The total number of two-wheeled vehicles for this date is {outcomes['total_two_wheelers']}",
        f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['total_buses_north']}",
        f"The total number of vehicles through both junctions not turning left or right is {outcomes['total_no_turns']}",
        f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['percentage_trucks']}%",
        f"The average number of bikes per hour for this date is {outcomes['average_bicycles_per_hour']}",
        f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['total_over_speed']}",
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['total_elm_rabbit']}",
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['total_hanley_westway']}",
        f"{outcomes['percentage_scooter']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_vehicles_hanley']}",
        f"The most vehicles through Hanley Highway/Westway were recorded " + ', '.join([f"Between {hour:02d}:00 and {hour+1:02d}:00" for hour in outcomes['peak_hours']]),
        f"The number of hours of rain for this date is {outcomes['total_rain_hours']}",
    ]

    for line in output_lines:
        print(line)
        
    return output_lines

# Task C: Save Results to Text File
def save_results_to_file(output_lines):
    with open("results.txt", "a") as file:
        file.write("\n")
        file.write("\n".join(output_lines) + "\n")

# Task D: Histogram Display        
class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None
        self.colors = ['pink', 'lightgreen']  # Light green and light pink

    def setup_window(self):
        """Set up the Tkinter window and canvas."""
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        self.root.geometry("1200x600")
        self.canvas = tk.Canvas(self.root, width=1200, height=600, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        """Draw the histogram based on the traffic data."""
        junctions = list(self.traffic_data.keys())
        hours = range(24)
        bar_width = 20
        spacing = 5
        start_x = 100
        start_y = 500
        
        # Calculate max value for scaling
        max_value = max(
            max(hour_data.values()) for hour_data in self.traffic_data.values()
        )
        scale = 400 / max_value

        # Draw title
        self.canvas.create_text(
            600, 30,
            text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
            font=("Arial", 14, "bold")
        )

        # Draw bars and labels
        for hour in hours:
            x_center = start_x + (bar_width * 2 + spacing) * hour
            
            for i, junction in enumerate(junctions):
                count = self.traffic_data[junction].get(hour, 0)
                bar_height = count * scale
                x = x_center + (bar_width * i)
                
                # Draw bar
                self.canvas.create_rectangle(
                    x, start_y - bar_height,
                    x + bar_width, start_y,
                    fill=self.colors[i],
                    outline=self.colors[i]
                )
                
                # Draw count above bar
                if count > 0:
                    self.canvas.create_text(
                        x + bar_width/2, start_y - bar_height - 5,
                        text=str(count),
                        font=("Arial", 8),
                        anchor="s"
                    )

            # Draw hour label
            self.canvas.create_text(
                x_center + bar_width,
                start_y + 15,
                text=f"{hour:02d}",
                font=("Arial", 8)
            )

        # Draw X-axis
        self.canvas.create_line(50, start_y, 1150, start_y, width=1)
        self.canvas.create_text(
            600, start_y + 35,
            text="Hours 00:00 to 24:00",
            font=("Arial", 10)
        )

        # Draw legend
        legend_y = 60
        for i, junction in enumerate(junctions):
            self.canvas.create_rectangle(
                100 + i * 250, legend_y,
                120 + i * 250, legend_y + 15,
                fill=self.colors[i],
                outline=self.colors[i]
            )
            self.canvas.create_text(
                125 + i * 250, legend_y + 7,
                text=junction,
                anchor="w",
                font=("Arial", 10)
            )

    def run(self):
        """Run the Tkinter application."""
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()
        
# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None

    def load_csv_file(self, file_name):
        self.current_data = process_csv_data(file_name)

    def clear_previous_data(self):
        self.current_data = None

    def validate_continue_input(self):
        while True:
            response = input("\nDo you want to select another data file for a different date? (Y/N): ").strip().upper()
            if response in ("Y", "N"):
                return response
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

    def handle_user_interaction(self):
        while True:
            day, month, year = validate_date_input()
            file_name = f"traffic_data{day:02d}{month:02d}{year:04d}.csv"

            self.load_csv_file(file_name)

            if self.current_data:
                outcomes = generate_outcomes(self.current_data)
                output_lines = display_outcomes(outcomes, file_name)
                save_results_to_file(output_lines)
                HistogramApp(self.current_data, f"{day:02d}/{month:02d}/{year:04d}").run()

            if self.validate_continue_input() == "N":
                print("\nEnd of program. Goodbye!")
                break

            self.clear_previous_data()

# Main Loop
def main():
    processor = MultiCSVProcessor()
    processor.handle_user_interaction()

if __name__ == "__main__":
    main()
    
