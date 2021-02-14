import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

#comparing chosen coin with tether
SOCKET = "wss://stream.binance.com:9443/ws/adausdt@kline_1m"
#RSI candle period
RSI_PERIOD = 14
#Overbought indicator
RSI_OVERBOUGHT = 70
#Oversold indicator
RSI_OVERSOLD = 30
#Trade symbol
TRADE_SYMBOL = 'ADAUSD'
#Amount to buy 
TRADE_QUANTITY = 0.05
#Closes will be collected in a list
closes = []
#Don't own currency
in_position = False
#Client data
client = Client(config.API_KEY, config.API_SECRET)
#Make an order
def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        #Sending order to binance
        print("sending order....")
        #order data
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        #print order made
        print(order)
    #Failed payment
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

#Connection opened   
def on_open(ws):
    print('opened connection')
#Connection closed   
def on_close(ws):
    print('closed connection')
    
#Message recieved
def on_message(ws, message):
    global closes, in_position
    
    print('received message')
    json_message = json.loads(message)
    #Print in readable format
    pprint.pprint(json_message)

    candle = json_message['k']
    #Candle closed
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        #Print out candle closing data
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)
        #if number of closes is greater than the RSI period
        if len(closes) > RSI_PERIOD:
            #Get array of 14 closes
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("RSI'S calculted so far: ")
            print(rsi)
            #Get the previous RSI DATA
            last_rsi = rsi[-1]
            print("The current RSI: {}".format(last_rsi))
            #if the previous RSI is greater than the overbought limit
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("{TRADE_SYMBOL} is OVERBOUGHT, SELLING!!!!!!!")
                    # TRIGGER SELL ORDER
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    #IF SUCCESFULL
                    if order_succeeded:
                        in_position = False
                else:
                    print("NO {TRADE_SYMBOL} owned. DOING NOTHING!!!! ")
             #if the previous RSI is LESS than the oversold limit
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("{TRADE_SYMBOL} is oversold,  but you already own any of this curreny. DOING NOTHING!!!!!.")
                else:
                    print("{TRADE_SYMBOL} is OVERSOLD, BUYING {TRADE_SYMBOL} !!!!!!!!!")
                    # buy logic
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if buy successful
                    if order_succeeded:
                        in_position = True

#Web socket
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
#KEEP RUNNING
ws.run_forever()