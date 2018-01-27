import argparse
import datetime, time
import threading
import urllib.request
import urllib.parse
import bs4 as bs
import csv
import os
from queue import Queue


def main():

    print_lock = threading.Lock()

    url = 'https://coinmarketcap.com/currencies/'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

    defaults = {'start_date': '20090101', 'end_date': '{0:%Y%m%d}'.format(datetime.datetime.now())}
    currencies = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--currency', type=str, help='enter the currency name')
    parser.add_argument('--currencies', type=str, help='enter the currencies names separated by \',\'')
    parser.add_argument('--start_date', type=str, default=defaults['start_date'], help='enter the start date (YYYYMMDD)')
    parser.add_argument('--end_date', type=str, default=defaults['end_date'], help='enter the end date (YYYYMMDD)')
    args = parser.parse_args()

    params = {'start': args.start_date, 'end': args.end_date}
    params_enc = urllib.parse.urlencode(params)
    params_enc = params_enc.encode('utf-8')

    if args.currency:
        currencies.append(args.currency)
    elif args.currencies:
        currencies = [item for item in args.currencies.split(',')]
    else:
        return 0


    def export_csv_data(csv_file, csv_columns, data_list):
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(csv_columns)
                for data in data_list:
                    writer.writerow(data)
        except:
                print("I/O error({0}): {1}")
        return

    def download_currency_data(currency):

        try:
            data_url = url + currency + '/historical-data/?start={0}&end={1}'.format(args.start_date, args.end_date)
            print('cr:' +data_url)
            #req = urllib.request.Request(data_url, params_enc, headers=headers)
            #sauce = urllib.request.urlopen(req).read()
            sauce = urllib.request.urlopen(data_url)
            soup = bs.BeautifulSoup(sauce, 'lxml')
            tbody = soup.tbody
            currency_history_keys = []
            currency_history = []

            for trow in tbody.find_all('tr'):
                td_list = trow.find_all('td')
                #date = time.strptime(td_list[0].text + ' 00:00', '%b %d, %Y %H:%M%')
                currency_history_keys = ['date', 'open', 'high', 'low', 'close', 'volume', 'market_cap']
                currency_history.append([
                time.mktime(time.strptime(td_list[0].text + ' 00:00', '%b %d, %Y %H:%M')),
                td_list[1].text.replace(',','.'),
                td_list[2].text.replace(',','.'),
                td_list[3].text.replace(',','.'),
                td_list[4].text.replace(',','.'),
                td_list[5].text.replace(',',''),
                td_list[6].text.replace(',','')
                ])

            filename = currency + ' - hist {0:%Y-%m-%d}'.format(datetime.datetime.now()) + '.csv'

            with print_lock:
                '''
                saveFile = open('newFile'+currency+'.txt', 'w')
                saveFile.write(str(currency_history))
                saveFile.close()
                '''
                export_csv_data(filename, currency_history_keys, currency_history)

                print('\'{0} historical data was extracted\''.format(currency))
                #print(currency_history)

        except:
            print('in ex')
            pass

    # The threader thread pulls an worker from the queue and processes it
    def threader():
        while True:
            # gets an worker from the queue
            worker = q.get()
            # Run the example job with the avail worker in queue (thread)
            download_currency_data(worker)
            # completed with the job
            q.task_done()

    # Create the queue and threader
    q = Queue()
    # how many threads are we going to allow for
    for x in range(10):
         t = threading.Thread(target=threader)
         # classifying as a daemon, so they will die when the main dies
         t.daemon = True
         # begins, must come after daemon definition
         t.start()

    # 100 jobs assigned.
    for worker in currencies:
        q.put(worker)

    # wait until the thread terminates.
    q.join()

if __name__ == '__main__':
    main()
