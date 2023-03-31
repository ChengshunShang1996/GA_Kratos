import csv  

header = ['name', 'area', 'country_code2', 'country_code3']
data = ['Afghanistan', 652090, 'AF', 'AFG']
my_data = []

with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    my_data.append(data[0])
    my_data.append(data[1])
    my_data.append(data[2])
    # write the data
    writer.writerow(my_data)