import csv
from time import strftime

# collects data given fileName, returns a file writer 
def dataOpen():

    # header for columns
    header = ['Speed', 'SOC', 'PackCurrent']

    # write to file, by opening. note, this is equivalent to opening and closing the file,
    # which we may not want to do
    f = open('rose' + strftime("%m_%d_%y_%I%M%p.csv"), 'w') #file name, opening as write
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader() # adds header
    return f

def dataSave(data: dict, file):
    # this is just the data we save from the data packet
    file.write(str(data['Speed']))
    file.write(',')
    file.write(str(data['SOC']))
    file.write(',')
    file.write(str(data['PackCurrent']))
    file.write("," + strftime("%m/%d/%y_%I:%M%p" + "\n")
)

def dataClose(file):
    # closes file so no mrore writing
    file.close()

testDict1 = {'Speed': 543,
             'SOC': 11,
             'PackCurrent': 42,
             }

# example code
# file = dataStart('rose')
# dataSave(data=testDict1, file=file)

# #change dict
# testDict1 = {'Speed': 25,
#              'SOC': 10,
#              'PackCurrent': 0,
#              }

# dataSave(data=testDict1, file=file)
# dataClose(file)

