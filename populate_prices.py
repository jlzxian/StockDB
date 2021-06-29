import config
import datetime, time
import aiohttp, asyncpg, asyncio
from io import StringIO
import numpy as np
from decimal import Decimal

async def write_to_db(connection, params):
    # Batch load into posgres
    await connection.copy_records_to_table('stock_price', records=params)


async def get_price(pool, stock_id, url):
    try:
        async with pool.acquire() as connection:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    resp = await response.read()
                    resp = str(resp, 'utf-8') # Converting bytes into string
                    data = StringIO(resp)
                    data = np.genfromtxt(data, dtype=None, delimiter=',', skip_header=1)
                    params = [(stock_id, datetime.datetime.strptime(str(bar[0], 'utf-8'), "%Y-%m-%d %H:%M:%S"), round(Decimal(bar[1]), 2), round(Decimal(bar[2]), 2), round(Decimal(bar[3]), 2), round(Decimal(bar[4]), 2), bar[5].astype(int)) for bar in data]
                    await write_to_db(connection, params)

    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def get_prices(pool, symbol_urls):
    try:
        # schedule aiohttp requests to run concurrently for all symbols
        ret = await asyncio.gather(*[get_price(pool, symbol[0], symbol[1]) for symbol in symbol_urls])
        print("Finalized all. Returned  list of {} outputs.".format(len(ret)))
    except Exception as e:
        print(e)


async def get_stocks():
    # create database connection pool
    pool = await asyncpg.create_pool(user=config.DB_USER, password=config.DB_PASS, database=config.DB_NAME, host=config.DB_HOST, command_timeout=60) # Creates a database connection pool, shared database connection, where many inserts can happen

    # get a connection
    async with pool.acquire() as connection:
        stocks = await connection.fetch("SELECT * FROM stock_dict")

        symbol_urls = []
        for stock in stocks:
            for i in range(1, 3):
                for j in range(1, 13):
                    #symbol_urls[stock['id']] = f"https://api.polygon.io/v2/aggs/ticker/{stock['symbol']}/range/5/minute/2020-10-01/2021-02-05?apiKey={config.API_KEY}&limit=50000"
                    symbol_urls.append((stock['id'], f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={stock['symbol']}&interval=1min&slice=year{i}month{j}&apikey={config.ALPHA_API_KEY}"))

    await get_prices(pool, symbol_urls)


start = time.time()

asyncio.run(get_stocks())

end = time.time()

print("Took {} seconds.".format(end - start))