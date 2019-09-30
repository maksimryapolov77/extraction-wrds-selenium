import csv
import re


output_format_fields = [
    'COMPANY NAME',
    'CIK',
    'CUSIP',
    'CUSIP_8D',
    'CUSIP_9D',
    'TICKER',
    ]


# out_rest_name = 'output_restatement.csv'
out_rest_name = 'output_aaers.csv'
# out_rest_name = 'output_restatement.csv'
# out_sec2_name = 'output_sec2.csv'
# out_aaers_name = 'output_aaers.csv'
# out_file_list = [
#     out_rest_name,
#     out_sec2_name,
#     out_aaers_name,
# ]

# nine_rest_name = '9_restatement.csv'
nine_rest_name = '9_aaers.csv'
# nine_rest_name = '9_restatement.csv'


# nine_sec2_name = '9_sec2.csv'
# nine_aaers_name = '9_aaers.csv'
# nine_file_list = [
#     nine_rest_name,
#     nine_sec2_name,
#     nine_aaers_name,
# ]


def matching():
    adden_nine_cusip = out_rest_name.replace('output_', 'added_nine_')
    with open(adden_nine_cusip, mode='w+', newline='') as cf:
        writer = csv.writer(cf,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        head_writer = csv.DictWriter(cf, fieldnames=output_format_fields)
        head_writer.writeheader()

        with open(out_rest_name) as df:
            df_reader = csv.reader(df, delimiter=',')
            for idx, row in enumerate(df_reader):
                eight_cusip = row[3]
                find_nine_cusip = ''
                with open(nine_rest_name) as nf:
                    n_reader = csv.reader(nf, delimiter=',')
                    for n_idx, n_row in enumerate(n_reader):
                        nine_cusip = n_row[0]
                        if idx != 0 and len(eight_cusip) == 8 and re.match("^[A-Za-z0-9]", eight_cusip):
                            if eight_cusip in nine_cusip:
                                print(f'{nine_cusip}------{eight_cusip}---------{n_idx}------{idx}')
                                find_nine_cusip = nine_cusip
                                break
                    # print(f' ----------{find_nine_cusip}')
                    row[4] = find_nine_cusip
                    writer.writerow(row)


if __name__ == "__main__":
    matching()
