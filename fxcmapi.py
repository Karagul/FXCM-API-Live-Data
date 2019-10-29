import fxcmpy
import time
import datetime as dt

###### USER PARAMETERS ######
token = '*************************'
symbol = 'EUR/CHF'
timeframe = "m1"  # (m1,m5,m15,m30,H1,H2,H3,H4,H6,H8,D1,W1,M1)
#############################

# Global Variables
pricedata = None
numberofcandles = 3
limit = 0.05
stop = 0.01
amount = 1
direction = True

# Connect to FXCM API
con = fxcmpy.fxcmpy(access_token=token, log_level="error")

# This function runs once at the beginning of the strategy to run initial one-time processes/computations
def Prepare():
    global pricedata

    print("Requesting Initial Price Data...")
    pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
    print(pricedata)
    print("Initial Price Data Received...")


# Get latest close bar prices and run Update() function every close of bar/candle
def StrategyHeartBeat():
    while True:
        currenttime = dt.datetime.now()
        if timeframe == "m1" and currenttime.second == 0 and GetLatestPriceData():
            Update()
        elif timeframe == "m5" and currenttime.second == 0 and currenttime.minute % 5 == 0 and GetLatestPriceData():
            Update()
            time.sleep(240)
        elif timeframe == "m15" and currenttime.second == 0 and currenttime.minute % 15 == 0 and GetLatestPriceData():
            Update()
            time.sleep(840)
        elif timeframe == "m30" and currenttime.second == 0 and currenttime.minute % 30 == 0 and GetLatestPriceData():
            Update()
            time.sleep(1740)
        elif currenttime.second == 0 and currenttime.minute == 0 and GetLatestPriceData():
            Update()
            time.sleep(3540)
        time.sleep(1)


# Returns True when pricedata is properly updated
def GetLatestPriceData():
    global pricedata

    # Normal operation will update pricedata on first attempt
    new_pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
    if new_pricedata.index.values[len(new_pricedata.index.values) - 1] != pricedata.index.values[
        len(pricedata.index.values) - 1]:
        pricedata = new_pricedata
        return True

    counter = 0
    # If data is not available on first attempt, try up to 3 times to update pricedata
    while new_pricedata.index.values[len(new_pricedata.index.values) - 1] == pricedata.index.values[
        len(pricedata.index.values) - 1] and counter < 3:
        print("No updated prices found, trying again in 1 seconds...")
        counter += 1
        time.sleep(1)
        new_pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
    if new_pricedata.index.values[len(new_pricedata.index.values) - 1] != pricedata.index.values[
        len(pricedata.index.values) - 1]:
        pricedata = new_pricedata
        return True
    else:
        return False


# This function is run every time a candle closes
def Update():

    print('nothin')

def enter():
    con.create_market_buy_order(symbol, 200)
    print('Entered trade')


Prepare()  # Initialize strategy
enter()
StrategyHeartBeat()  # Run strategy
pos.close()

con.get_open_positions()