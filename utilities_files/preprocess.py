import csv
# Open the CSV file
with open('class_labels_indices.csv', mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    next(csv_reader)
    # Read and print each row of the CSV file
    dict = {}
    for row in csv_reader:
        
        label = row[1]
        display_name = row[2]
        dict[label] = display_name
        

import csv

file_path = 'balanced_train_segments.csv'  # Replace 'your_file.csv' with your file path

with open(file_path, 'r') as file,open("new_balanced.csv", 'w', newline='') as csvfile_out:
    reader = csv.reader(file)
    writer = csv.writer(csvfile_out)
    for row in reader:
        new_column = ""
        for i in range(3,len(row)):
            new_column += row[i]
            if(i != len(row)-1):
                new_column += ","  
        row[3] = new_column.replace('"', '')
        row[3] = row[3].replace(' ', '')
        tokens = row[3].split(",")
        new = []
        for elem in tokens:
            if elem in dict:
                new.append(dict[elem])
        new_row = [row[0],row[1],row[2],row[3],new]
        writer.writerow(new_row)

        


