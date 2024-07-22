import csv
from time import strftime

# collects data given fileName, 
def doDataCollect(fileName: str, list: dict):
    # header for timestamps
    header = ['SOC', 'SPEED', 'NETAMPS', 'MPPT0AMP', 'MPPT1AMP', 'TIMESTAMP']

    with open('data(.csv', newline='') as csvfile:

        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row[)