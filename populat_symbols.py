import config
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras
import pandas as pd

# Establishing connection to Postgres DB
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                              password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# #psycopg2.extras.DictCursors enables returned results to be a dictionary instead of a list
# stocks = cursor.execute("SELECT * FROM stock_dict")
# for stock in stocks:
#     print(stock)

###############
# #  Reading in assets from ALPACA
# api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)
# assets = api.list_assets()
#
# for asset in assets:
#     cursor.execute("""
#     INSERT INTO stock_dict (name, symbol, exchange, is_etf)
#     VALUES (%s, %s, %s, %s)""",
#                    (asset.name, asset.symbol, asset.exchange, False))

###############
# Reading in asstes from NASDAQ
df = pd.read_csv("./Data/tickers.txt", sep="|")

for index, stock in df.iterrows():
    cursor.execute("""
    INSERT INTO stock_dict (symbol, name,  exchange, is_etf)
    VALUES (%s, %s, %s, %s)""",
                   (stock['Symbol'], stock['Security Name'], stock['Listing Exchange'], stock['ETF'] == "Y"))

connection.commit()
connection.close()
