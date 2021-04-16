#https://pypi.org/project/websocket_client/
import websocket
import numpy as np 
import matplotlib.pyplot as plt 
import json

prices = []


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

def getPriceFromPriceData(priceData) -> str:
    d = json.loads(priceData)
    # Need to see if Python has type safety
    return d['data'][0]['p']
    # print(d['data'][0]['p'])

def getSmallestNumber():
    tmpPriceArr = prices
    tmpPriceArr.sort()
    return tmpPriceArr[0]

def getLargestNumber():
    tmpPriceArr = prices
    tmpPriceArr.sort()
    return tmpPriceArr[len(tmpPriceArr)-1]

def initChart():
    x = 0 
    y = 0
    
    # plotting
    plt.title("DogeCoin Trade Tracker") 
    # plt.xlabel("X axis") 
    plt.ylabel("Price") 
    plt.plot(x, y, color ="red") 
    plt.grid(True)
    plt.show(block=False)

def drawChart(ws, priceData):
    plt.pause(0.05)
    newPrice = getPriceFromPriceData(priceData)
    appendNewPrice = True
    if len(prices) > 0: 
        newPricePos = len(prices) - 1
        appendNewPrice = (newPrice != prices[newPricePos])
    else:
        newPricePos = 0
    if appendNewPrice:
        prices.append(newPrice)
        smallestPrice = getSmallestNumber()
        largestPrice = getLargestNumber()
        plt.ylim((smallestPrice-(smallestPrice*0.01)), (largestPrice+(largestPrice*0.01)))
        plt.plot(newPricePos, prices[newPricePos], color='red', marker='o')
        plt.show(block=False)


if __name__ == "__main__":
    initChart()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c1notfa37fkph7jrm5ng",
                              on_message = drawChart,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()