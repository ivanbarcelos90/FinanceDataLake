import yfinance as yf


class APIStock:
    def __init__(self, stock):
        self.stock = stock

    # The Ticker Module
    def Ticker(self):
        return yf.Ticker(self.stock)

    # Get stock info
    def info(self):      
        return print(self.Ticker().info) 

    # Get historical market data
    def history(self):
        return print(self.Ticker().history(period="max"))

    # Show actions (dividends, splits)
    def actions(self):
        return print(self.Ticker().actions)

    # show dividends
    def dividends(self):
        return print(self.Ticker().dividends)

    # show splits
    def splits(self):
        return print(self.Ticker().splits)

    # show financials
    def financials(self):
        return print(self.Ticker().financials), print(self.Ticker().quarterly_financials)

    # show major holders
    def major_holder(self):
        return print(self.Ticker().major_holders)

    # show institutional holders
    def institutional_holders(self):
        return print(self.Ticker().institutional_holders)

    # show balance sheet
    def balance_sheet(self):
        return print(self.Ticker().balance_sheet), print(self.Ticker().quarterly_balance_sheet)

    # show cashflow
    def cashflow(self):
        return print(self.Ticker().cashflow), print(self.Ticker().quarterly_cashflow)

    # show earnings
    def earnings(self):
        return print(self.Ticker().earnings), print(self.Ticker().quarterly_earnings)

    # show sustainability
    def sustainability(self):
        return print(self.Ticker().sustainability)

    # show analysts recommendations
    def analysts_recommendations(self):
        return print(self.Ticker().recommendations)

    # show next event (earnings, etc)
    def calendar(self):
        return print(self.Ticker().calendar)

    # ISIN = International Securities Identification Number
    def ISIN(self):
        return print(self.Ticker().isin)

    # show options expirations
    def options(self):
        return print(self.Ticker().options)

    # show news
    def news(self):
        return print(self.Ticker().news)


