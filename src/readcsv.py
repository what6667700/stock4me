import csv

with open('000616.csv', 'r') as csv_file:  # Opens the file in read mode
    csv_reader = csv.reader(csv_file)  # Making use of reader method for reading the file

    for line in csv_reader:  # Iterate through the loop to read line by line
        print(line)