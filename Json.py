import json

import os

import csv


def chunks(list_you_want, no_of_items):
    for i in range(0, len(list_you_want), no_of_items):
        yield list_you_want[i:i+no_of_items]


path = 'C:\ProgramData\Malwarebytes\MBAMService\MwacDetections'

directory = os.fsdecode(path)

suffix = ".json"

csv_data = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(suffix):
     #   print(os.path.join(directory, filename))
        read_path = os.path.join(directory, filename)
        with open(read_path, 'r', encoding='utf-8') as json_many_data:
            for json_data in json_many_data:
                data = json_many_data.read()
                json_final_data = json.loads(data)
                detect_date_time = json_final_data['detectionDateTime']

                for threats_data in json_final_data['threats']:
                    for trace_data in threats_data['mainTrace']['websiteData']:
                        csv_data.append(threats_data['mainTrace']['websiteData'][trace_data])
                csv_data.append(detect_date_time)
            csv_data.append(filename)

print(csv_data)
new_csv_data = list(chunks(csv_data,7))
print(new_csv_data)

with open('rakjson.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for ip, isInbound, port, processPath, url, detectdt, filename in new_csv_data:
        writer.writerow([ip, isInbound, port, processPath, url, detectdt, filename])