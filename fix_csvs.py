import csv

ekaterina_csv = 'CIK_CUSIP.csv'
cik_picked_ekaterina_csv = 'cik_picked_ekaterina.csv'
fieldnames = ['cik', 'cusip']
out_restatement = 'output_restatement.csv'
out_sec2 = 'output_sec2.csv'
out_aaers = 'output_aaers.csv'

out_file_list = [
    out_restatement,
    out_sec2,
    out_aaers,
    ]


def filter_ekaterina_file():
    """ remove duplicated ciks of cik_cusip.csv
    :return: none
    """
    eka_dic = dict()
    data = csv.reader(open(ekaterina_csv), delimiter=',')
    for idx, line in enumerate(data):
        if not idx == 0:
            cik = line[1]
            cusip = line[3]
            if cik not in eka_dic:
                eka_dic[int(cik)] = cusip

    print(eka_dic)
    for file_idx, output_file in enumerate(out_file_list):
        data = csv.reader(open(output_file), delimiter=',')
        with open(output_file.replace('.csv', 'copy.csv'), mode='w+', newline='') as f:
            writer = csv.writer(f)
            for row_idx, row in enumerate(data):
                if row_idx != 0:
                    cik = int(row[1])
                    if cik in eka_dic:
                        print(f'{cik} : {eka_dic[cik]}')
                        row[3] = eka_dic[cik]
                writer.writerow(row)


if __name__ == "__main__":
    filter_ekaterina_file()
