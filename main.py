import sys
import json
import csv

if not len(sys.argv) < 2:
    file_list = []
    f = open(sys.argv[-1], "r")  # open up the file designated at run time
    data = json.load(f)
    f.close()
    print(data['Statistics'])


    def write_file(data):
        """Takes a json content for statistics and outputs the data relevant to
        a csv file with proper headers"""

        with open('cvs_file.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # create headers
            header = data.keys()
            csv_writer.writerow(header)

            csv_writer.writerow(data.values())

    write_file(data['Statistics'])


else:
    print("hello")