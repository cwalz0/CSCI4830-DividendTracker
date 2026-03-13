import yfinance as yf
aapl = yf.Ticker("AAPL")

print(f"{aapl.info.get('shortName',0)}")


def printDoc():
    for word in dir(aapl):
        print(word)


#print(aapl.info)

