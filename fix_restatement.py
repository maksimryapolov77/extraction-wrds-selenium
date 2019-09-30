import csv


def add_missing_ciks():
    """generate cik list of ouput_restatement.csv
    :return:
    """
    cik_picked_restatement_file = 'cik_picked_restatement.csv'
    out_restatement = 'output_restatement.csv'
    cik_list_out_restatement = []

    # file = open(out_restatement, 'r')
    # reader = csv.reader(file)
    # for line in reader:
    #     cik_list_out_restatement.append(line[1])
    # file.close()

    # cik_picked_file = open(cik_picked_restatement_file, 'r')
    # picked_reader = csv.reader(cik_picked_file)
    # file1 = open(out_restatement, 'a', newline='')
    # writer = csv.writer(file1,
    #                     delimiter=',',
    #                     quotechar='"',
    #                     quoting=csv.QUOTE_MINIMAL)
    # for row in picked_reader:
    #     if not row[1] in cik_list_out_restatement:
    #         print(row)
    #         writer.writerow([row[0], row[1], '', '', '', row[2]])

    file3 = open(out_restatement, 'r')
    file_reader = csv.reader(file3)
    i = 0
    for idx, line in enumerate(file_reader):
        cusip = line[2]
        ticker = line[5]
        if cusip != '' and ticker == '':
            i += 1
            print(line)
    file3.close()
    print(i)


if __name__ == "__main__":
    add_missing_ciks()