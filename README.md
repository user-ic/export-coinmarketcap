## export-coinmarketcap
Exports coinmarketcap historical data

```
optional arguments:
  -h, --help            show this help message and exit
  --currency CURRENCY   enter the currency name
  --currencies CURRENCIES
                        enter the currencies names separated by ','
  --start_date START_DATE
                        enter the start date (YYYYMMDD)
  --end_date END_DATE   enter the end date (YYYYMMDD)
```

## usage example
```
python coinmarketcap.py --currency bitcoin
python coinmarketcap.py --currencies bitcoin,ethereum
python coinmarketcap.py --currencies bitcoin,ethereum --start_date 20180101 --end_date 20180120
```
## notes
the names of the currencies can be obtained at the coinmarketcap website
##### ethereum, bitcoin
```
https://coinmarketcap.com/currencies/ethereum/historical-data/
https://coinmarketcap.com/currencies/bitcoin/historical-data/
```
