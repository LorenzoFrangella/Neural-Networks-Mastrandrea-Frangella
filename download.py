import csv
with open('balanced_train_segments.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
        print(lines[1])
        break
