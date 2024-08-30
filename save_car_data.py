
PATH = "./car_data.csv"

# Creates and returns a string with our compiled data. Edit how you see fit
def build_data():
    output = ""
    
    # Headers
    output += "Car Speed,"
    output += "Example Variable 0,"
    output += "Example Variable 1"

    output += "\n"

    # Data
    output += str(50) + ","
    output += str(10) + ","
    output += str(5)

    return output


# File exists, overwrite it
saved_data = open(PATH, "w")

saved_data.write(build_data())

saved_data.close()

