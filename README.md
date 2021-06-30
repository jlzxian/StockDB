# StockDB
 Stock Database

Credit: Youtuber Part Time Larry's TimescaleDB series

Prereq:
1. TimescaleDB docker image
2. requirements.txt

Steps:
1. Setup Postgres tables in accordance to 'db/create_table.sql'
2. Download ticker list from NASDAQ and place in 'data' folder
3. Run populate_symbols.py to upload tickers to database
4. Run populate.prices.py to upload price history to database
