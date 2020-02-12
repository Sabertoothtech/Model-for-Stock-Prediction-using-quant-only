def NseTick(Sv):
    import os
    import datetime
    import logging
    import IPython
    import pandas as pd
    import threading
    import datetime
    from IPython.display import clear_output
    from kiteconnect import KiteTicker
    from apscheduler.schedulers.blocking import BlockingScheduler

    sched = BlockingScheduler()
	
    loginfile = open(r"C:\Users\Desktop\Desktop\Schedule_programs\LoginDetail.txt",'r')
    loginlst = eval(loginfile.read())
    access_token = loginlst['access_token']
    logging.basicConfig(level=logging.DEBUG)
    lstfile = open(r"C:\Users\Desktop\Desktop\Schedule_programs\NseList.txt",'r')
    lst = eval(lstfile.read())
    tokens = lst[Sv - 200:Sv]
    print(len(tokens))
    file = open(r'C:\Users\Desktop\Desktop\Schedule_programs\csvoutput1.csv','a')
    # Initialise
    kws = KiteTicker("0ld4qxtvnif715ls", access_token)
    def on_ticks(ws, ticks):
        for i in ticks:
            try:
                df = pd.DataFrame(i['ohlc'], index=[0])
                "st = str(i['instrument_token'])"
                df['Instrument Token'] =i['instrument_token'] #nfo[nfo.instrument_token.str.contains(st)].tradingsymbol.iloc[0]
                df['Last price'] = i['last_price']
                df['Last quantity'] = i['last_quantity']
                df['Average price'] = i['average_price']
                df['Volume'] = i['volume']
                df['Buy quantity'] = i['buy_quantity']
                df['Sell quantity'] = i['sell_quantity']
                df['Change'] = i['change']
                df['Last trade time'] = i['last_trade_time']
                df['OI'] = i['oi']
                df['OI day high'] = i['oi_day_high']
                df['OI day low'] = i['oi_day_low']
                df['Time'] = i['timestamp']
                df.to_csv(file,header = False)
            except:
                pass

    def on_connect(ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe(tokens)
        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL, tokens)
        clear_output()
        
    def on_close(ws, code, reason):
        print('close')
        loginfile = open("LoginDetail.txt",'r')
        loginlst = eval(loginfile.read())
        access_token = loginlst['access_token']
        # Initialise
        global kws
        kws = KiteTicker("0ld4qxtvnif715ls", access_token)
        main_function()

    
    # Assign the callbacks.
    def main_function():
        kws.on_ticks = on_ticks
        kws.on_connect = on_connect
        """app = IPython.Application.instance()
        app.kernel.do_shutdown(True)"""
        "kws.on_close = on_close"
        kws.connect()
    main_function()
