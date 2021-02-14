import websocket, json, pprint
#Socket and address
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

closes = []

#Open socet connection
def on_open(ws):
    print('opened connection')
    
#Close socket connection
def on_close(ws):
    print('closed connection')
    
#Print message recieved in json format
def on_message(ws, message):
    global closes
    print(message)
    #convert json string to python data format
    json_message = json.loads(message)
    pprint.pprint(json_message)
   
    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    #Print candle closing price
    if is_candle_closed:
        print("candle closed at {}".format(close))
        #Appending closing prices
        closes.append(float(close))
        print("closes")
        print(closes)
        
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()