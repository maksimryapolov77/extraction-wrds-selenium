import csv
import re

output_rest_name = 'output_restatement.csv'
output_sec2_name = 'output_sec2.csv'
output_aaers_name = 'output_aaers.csv'
output_file_list = [
    output_rest_name,
    output_sec2_name,
    output_aaers_name,
]


def generate_text():
    for out_file_idx, out_file in enumerate(output_file_list):
        txt = open(out_file.replace('output_', '8_'), mode='w+', newline='')
        txt_writer = csv.writer(txt,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        with open(out_file) as f:
            reader = csv.reader(f, delimiter=',')
            for idx, row in enumerate(reader):
                cusip = row[3]
                if idx != 0:
                    if len(cusip) == 8:
                        txt_writer.writerow([idx, cusip])


if __name__ == "__main__":
    generate_text()
