import logging
import os
from pathlib import Path
from time import sleep

from scrapy.utils.log import configure_logging
from selenium import webdriver
import csv
import xlrd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='logging.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

download_path = 'C:\\Users\\Administrator\\Downloads\\'
root_path = os.path.dirname(os.path.realpath(__file__)) + '\\'

cik_rest_name = 'cik_picked_restatement.csv'
cik_sec2_name = 'cik_picked_sec2.csv'
cik_aaers_name = 'cik_picked_aaers.csv'
cik_rest_file = root_path + cik_rest_name
cik_sec2_file = root_path + cik_sec2_name
cik_aaers_file = root_path + cik_aaers_name
cik_format_fields = [
    'COMPANY NAME',
    'CIK',
    'TICKER',
    ]
cik_file_list = [
    cik_rest_name,
    cik_sec2_name,
    cik_aaers_name,
    ]

input_rest_name = 'restatement-data-1565169381.csv'
input_sec2_name = 'SEc2_cleaned.xlsx'
input_aaers_name = 'AAERS_cleaned.xlsx'
input_file_list = [
    input_rest_name,
    input_sec2_name,
    input_aaers_name,
    ]

output_rest_name = 'output_restatement.csv'
output_sec2_name = 'output_sec2.csv'
output_aaers_name = 'output_aaers.csv'
output_file_list = [
    output_rest_name,
    output_sec2_name,
    output_aaers_name,
    ]
output_format_fields = [
    'COMPANY NAME',
    'CIK',
    'CUSIP',
    'CUSIP_8D',
    'CUSIP_9D',
    'TICKER',
    ]

query_url = 'https://wrds-web.wharton.upenn.edu/wrds/ds/compd/funda/index.cfm?navId=83'     # query form url
delay = 20      # max waiting time
m_delay = 7     # middle waiting time

user_name_str = ''       # user's name
password_str = ''       # user's password
start_date = '2000-01'      # start date for submit query
end_date = '2019-01'        # end date for submit query

picked_list = []
log_file = 'log.txt'


def login():
    """ crawler login in wrds site.
    input params for form submit
    :return: chrome webdriver
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, delay)
    driver.maximize_window()
    driver.get(query_url)
    username = driver.find_element_by_id('username')
    password = driver.find_element_by_id('password')
    username.clear()
    password.clear()
    username.send_keys(user_name_str)
    password.send_keys(password_str)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-body"]/div/aside/form/div[3]/div/button')))
    driver.find_element_by_xpath('//*[@id="main-body"]/div/aside/form/div[3]/div/button').click()

    """ input start, end date
    handle escape key
    cik combobox click
    select click company name, cik, cusip
    """
    driver.find_element_by_id('select_beg_date').clear()
    driver.find_element_by_id('select_beg_date').send_keys(start_date)
    driver.find_element_by_id('select_end_date').clear()
    driver.find_element_by_id('select_end_date').send_keys(end_date)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    driver.find_element_by_id('format-CIK').click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="select_all_container_div-80DBA1CF"]/label[2]')))
    driver.find_element_by_xpath('//*[@id="select_all_container_div-80DBA1CF"]/label[2]').click()
    driver.find_element_by_xpath('//*[@id="select_all_container_div-80DBA1CF"]/label[3]').click()
    driver.find_element_by_xpath('//*[@id="select_all_container_div-80DBA1CF"]/label[4]').click()
    driver.find_element_by_id('csv').click()
    return driver


def parse_log():
    """ get before stop point from log.txt
    :return: cik_file_name, output_file_name, cik_file_index, cik_row_index
    """
    fh = open(log_file, 'r')
    lines = fh.readlines()
    fh.close()
    line_counts = len(lines)
    # print(f'counts {line_counts}')
    stopped_cik_file = lines[line_counts - 3].strip()
    stopped_cik_file_index = cik_file_list.index(stopped_cik_file)
    stopped_cik_row_index = lines[line_counts - 1].strip()
    return int(stopped_cik_file_index), int(stopped_cik_row_index)


def crawling():
    """ run chrome webdriver.
    iterate query via query_url
    download csv file included cik, cusip, ticker, ... .
    parsing and extract cusip with downloaded csv.
    :return:
    """
    driver = login()
    wait = WebDriverWait(driver, delay)

    stopped_cik_file_index = 0
    stopped_cik_row_index = 0

    if Path(log_file).exists() and os.path.getsize(log_file) > 0:
        stopped_cik_file_index, stopped_cik_row_index = parse_log()

    print(f' file index {stopped_cik_file_index} row index {stopped_cik_row_index}')
    """ handle submit query
    loop cik-picked_file_list
    create three csv file and append extraction data
    """
    log = open(log_file, 'w')

    for cik_idx, cik_file in enumerate(cik_file_list):
        if cik_idx >= stopped_cik_file_index:
            logging.info(f' cik idx: {cik_idx} stopped_cik_file_index:  {stopped_cik_file_index}')
            with open(cik_file) as csv_file:
                csv_data = csv.reader(csv_file, delimiter=',')
                #### row_idx = 0

                """ create output file
                write output file's header
                header: 'COMPANY NAME' 'CIK' 'CUSIP' 'CUSIP_8D' 'CUSIP_9D' 'TICKER'
                """
                with open(output_file_list[cik_idx], mode='a', newline='') as out_file:
                    out_writer = csv.writer(out_file,
                                            delimiter=',',
                                            quotechar='"',
                                            quoting=csv.QUOTE_MINIMAL)
                    if not os.path.getsize(output_file_list[cik_idx]) > 0:
                        head_writer = csv.DictWriter(out_file, fieldnames=output_format_fields)
                        head_writer.writeheader()

                    """ loop submit query with cik iterate
                    download csv file per cik
                    parse csv and export cusip from it
                    """
                    for row_idx, row in enumerate(csv_data):
                        if cik_idx != stopped_cik_file_index:
                            stopped_cik_row_index = 0
                        if row_idx != 0 and row_idx > stopped_cik_row_index:
                            logging.info(f' cik row_idx: {row_idx} stopped_cik_row_index:  {stopped_cik_row_index}')
                            print(f' cik row_idx: {row_idx} stopped_cik_row_index:  {stopped_cik_row_index}')
                            """ log current cik_file_name, output_file_name, row index of cik_file_name
                            """
                            log.write('%s\n' % cik_file)
                            log.write('%s\n' % output_file_list[cik_idx])
                            log.write('%d\n' % row_idx)

                            company_name = row[0]
                            cik = row[1]        # cik code from cik_picked_file
                            ticker = row[2]     # ticker code from cik_picked_file
                            # print(f'Entered {cik}')

                            driver.find_element_by_id('code_lookup_method1').clear()
                            driver.find_element_by_id('code_lookup_method1').send_keys(cik)
                            query_btn = wait.until(
                                EC.element_to_be_clickable((By.ID, 'form_submit')))
                            query_btn.click()
                            driver.switch_to.window(driver.window_handles[1])
                            try:
                                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="subcol"]')))
                                try:
                                    WebDriverWait(driver, m_delay).until(EC.visibility_of_element_located(
                                        (By.XPATH, '//*[@id="main"]/p[4]/b')))
                                    driver.find_element_by_xpath('//*[@id="main"]/p[2]/a').click()      # down click
                                    file_name = driver.find_element_by_xpath(
                                        '//*[@id="main"]/p[2]/a'
                                    ).text      # downloading csv file name
                                    downloaded_file = download_path + file_name     # downloaded csv file's absolute
                                    # path
                                    sleep(2)

                                    # check whether downloading is success
                                    seconds = 0
                                    dl_wait = True
                                    while dl_wait and seconds < delay:
                                        sleep(1)
                                        dl_wait = False
                                        for fname in os.listdir(download_path):
                                            if fname.endswith('.crdownload'):
                                                dl_wait = True
                                        seconds += 1
                                    check_file = Path(downloaded_file)
                                    if check_file.is_file():
                                        print(f'file path : {downloaded_file}')

                                        """ parse downloaded csv file
                                        remove downloaded file after parsing
                                        """
                                        with open(downloaded_file) as df:
                                            df_reader = csv.reader(df, delimiter=',')
                                            interesting_row = [row for idx, row in enumerate(df_reader) if idx == 1]
                                            cusip = interesting_row[0][8]
                                            ticker = interesting_row[0][7]
                                            out_writer.writerow([company_name, cik, cusip, '', '', ticker])
                                            print(f'company: {company_name} cik: {cik} cusip: {cusip} ticker: {ticker}')
                                        df.close()
                                        os.remove(downloaded_file)

                                        driver.close()
                                        driver.switch_to.window(driver.window_handles[0])       # switch in first tab
                                    else:
                                        logging.info(f'{cik}\'s cusip is not parsed.'
                                                     f' It\'s exist. Manual CUSIP must'
                                                     f' input on {output_file_list[cik_idx]}')
                                        out_writer.writerow([company_name, cik, '', '', '', ticker])
                                except TimeoutException:
                                    out_writer.writerow([company_name, cik, '', '', '', ticker])
                                    print(f'Not Founded company: {company_name} cik: {cik} ticker: {ticker}')
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                            except TimeoutException:
                                out_writer.writerow([company_name, cik, '', '', '', ticker])
                                print(f'Not Founded company: {company_name} cik: {cik} ticker: {ticker}')
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])       # switch in first tab
                        ##### row_idx += 1
    # driver.close()


def export_cik_sec2_or_aaers():
    """ make two files(cik_sec2_file, cik_aaers_file) with input_secs_file and input_aaers_file.
    :return:
    """
    for idx, (cik_picked_file, input_file) in \
            enumerate(zip(cik_file_list, input_file_list)):
        if idx != 0:
            with open(cik_picked_file, mode='w+', newline='') as f:
                writer = csv.writer(f,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                header_writer = csv.DictWriter(f,
                                               fieldnames=cik_format_fields)
                header_writer.writeheader()
                workbook = xlrd.open_workbook(input_file, 'rb')
                sh = workbook.sheet_by_name(workbook.sheet_names()[0])
                for row_num in range(sh.nrows):
                    if row_num != 0:
                        row_values = sh.row_values(row_num)
                        company_name = row_values[2]
                        cik = row_values[3]
                        ticker = row_values[5]
                        if cik not in picked_list:
                            picked_list.append(cik)
                            writer.writerow([company_name, int(cik), ticker])
                            # print(f'{company_name} {cik} {ticker}')
                picked_list.clear()


def export_cik_rest():
    """ make cik_rest_file with input_rest_file.
    :return: none
    """
    with open(cik_rest_name, mode='w+', newline='') as cf:
        restatement_writer = csv.writer(cf,
                                        delimiter=',',
                                        quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
        restatement_header_writer = \
            csv.DictWriter(cf, fieldnames=cik_format_fields)
        restatement_header_writer.writeheader()
        with open(input_rest_name) as rf:
            for idx, values in enumerate(rf.readlines()):
                if idx != 0:
                    value_list = values.split(',')
                    cik = value_list[1]
                    if str(cik).isdigit():
                        company_name = value_list[0]
                        ticker = values.split(',')[2]
                    else:
                        company_name = value_list[0] + value_list[1]
                        cik = value_list[2]
                        ticker = value_list[3]
                    if cik not in picked_list:
                        picked_list.append(cik)
                        # print(f'{company_name} {cik} {ticker}')
                        restatement_writer.writerow(
                            [company_name.replace('"', '').replace('.', ''), cik, ticker])
            picked_list.clear()


def create_cik_files():
    """ create cik duplicated removed files with input files.
    :return: none
    """
    for idx, file in enumerate(input_file_list):
        if idx == 0:
            export_cik_rest()
        else:
            export_cik_sec2_or_aaers()


def check_cik_picked_files_exist():
    """ check existing of three cik files.
    :return: boolean
    """
    if Path(cik_rest_file).exists()\
            and Path(cik_sec2_file).exists()\
            and Path(cik_aaers_file).exists():
        return True


if __name__ == "__main__":
    if not check_cik_picked_files_exist():
        create_cik_files()
    crawling()
