import psycopg2
import datetime
import time
import pandas as pd

class SpotApi():
    def __init__(self, host, port, username, password, dbname):
        while True:
            try:
                self.conn = psycopg2.connect("host={} port={} user={} password={} dbname={}".format(host, port, username, password, dbname))
                print("DB connect successful!")
            except psycopg2.OperationalError as e:
                print('pg connection failed retry in 5 seconds:' + str(e))
                time.sleep(5)
                continue
            break
        self.cur = self.conn.cursor()

    def analyze_args(self, args):
        if args.get('start_date', '') and args.get('end_date' ''):
            return ' and time >= \'{}\' and time <= \'{}\' order by time desc'.format(args['start_date'], args['end_date'])
        elif args.get('latest_day', ''):
            latest_day = int(args['latest_day'])
            return ' and time >= \'{}\' order by time desc'.format((datetime.datetime.now() - datetime.timedelta(days=latest_day, hours=8)).isoformat())
        elif args.get('latest_number', ''):
            latest_number = int(args['latest_number'])
            return ' order by time desc limit {} '.format(latest_number)
        else:
            return ' order by time desc limit 500 '

    def query(self, type, exchange_name, pair, **args):
        if type == 'ticker':
            return self.ticker(exchange_name, pair, **args)
        elif type == 'candles':
            return self.candles(exchange_name, pair, **args)
        elif type == 'trade':
            return self.trade(exchange_name, pair, **args)
        elif type == 'depth':
            return self.depth(exchange_name, pair, **args)
        else:
            return 'Please provide correct type: ticker | candles | trade | depth'

    def ticker(self, exchange_name, pair, **args):
        sql_condition = self.analyze_args(args)
        sql = 'select * from SpotTicker where exchange_name = \'{}\' and pair = \'{}\' {}'.format(exchange_name, pair, sql_condition)
        self.cur.execute(sql)
        results = self.cur.fetchall()
        dataframes = pd.DataFrame(results, columns = ['time', 'exchange_id', 'exchange_name', 'pair', 'update_time',
                                                      'last', 'best_ask', 'best_bid', 'high_24h', 'low_24h', 'open_24h', 'base_volume_24h', 'quote_volume_24h'])
        dataframes.set_index('time', inplace=True)
        return dataframes

    def candles(self, exchange_name, pair, **args):
        sql_condition = self.analyze_args(args)
        period_condition = ''
        if args.get('period', ''):
            period_condition = ' and period = {} '.format(args['period'])
        sql = 'select * from SpotCandles where exchange_name = \'{}\' and pair = \'{}\' {} {}'.format(exchange_name, pair, period_condition, sql_condition)
        self.cur.execute(sql)
        results = self.cur.fetchall()
        dataframes = pd.DataFrame(results, columns = ['time', 'exchange_id', 'exchange_name', 'pair', 'update_time',
                                                      'period', 'open', 'high', 'low', 'close', 'volume'])
        dataframes.set_index('time', inplace=True)
        return dataframes

    def trade(self, exchange_name, pair, **args):
        sql_condition = self.analyze_args(args)
        sql = 'select * from SpotTrade where exchange_name = \'{}\' and pair = \'{}\' {}'.format(exchange_name, pair, sql_condition)
        self.cur.execute(sql)
        results = self.cur.fetchall()
        dataframes = pd.DataFrame(results, columns = ['time', 'exchange_id', 'exchange_name', 'pair', 'update_time',
                                                      'trade_id', 'price', 'quantity', 'side'])
        dataframes.set_index('time', inplace=True)
        return dataframes

    def depth(self, exchange_name, pair, **args):
        end_date = datetime.datetime.now().isoformat()
        if args.get('end_date', ''):
            end_date = args['end_date']
        latest_snapshot_sql = 'select time from SpotDepth where exchange_name = \'{}\' and pair = \'{}\' and type = "snapshot" and time <= {} order by time desc limit 1'.format(exchange_name, pair, end_date)
        self.cur.execute(latest_snapshot_sql)
        latest_snapshot = self.cur.fetchall()
        if len(latest_snapshot) == 0:
            return list()
        latest_snapshot_time = latest_snapshot[0][0]
        sql = 'select * from SpotDepth where exchange_name = \'{}\' and pair = \'{}\' and time >= {} and time <= {} order by time desc'.format(exchange_name, pair, latest_snapshot_time, end_date)
        self.cur.execute(sql)
        results = self.cur.fetchall()
        dataframes = pd.DataFrame(results, columns = ['time', 'exchange_id', 'exchange_name', 'pair', 'update_time',
                                                      'snapshot_id', 'type', 'content'])
        dataframes.set_index('time', inplace=True)
        return dataframes

