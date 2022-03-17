import yfinance as yf


class APIStock:
    def __init__(self, stock):
        self.stock = stock
        self.ticker = yf.Ticker(self.stock)

    # Get stock info
    def info(self):      
        return print(self.ticker.info) 

    # Get historical market data
    def history(self):
        return print(self.ticker.history(period="max"))

    # Show actions (dividends, splits)
    def actions(self):
        return print(self.ticker.actions)

    # show dividends
    def dividends(self):
        return print(self.ticker.dividends)

    # show splits
    def splits(self):
        return print(self.ticker.splits)

    # show financials
    def financials(self):
        return print(self.ticker.financials), print(self.ticker.quarterly_financials)

    # show major holders
    def major_holder(self):
        return print(self.ticker.major_holders)

    # show institutional holders
    def institutional_holders(self):
        return print(self.ticker.institutional_holders)

    # show balance sheet
    def balance_sheet(self):
        return print(self.ticker.balance_sheet), print(self.ticker.quarterly_balance_sheet)

    # show cashflow
    def cashflow(self):
        return print(self.ticker.cashflow), print(self.ticker.quarterly_cashflow)

    # show earnings
    def earnings(self):
        return print(self.ticker.earnings), print(self.ticker.quarterly_earnings)

    # show sustainability
    def sustainability(self):
        return print(self.ticker.sustainability)

    # show analysts recommendations
    def analysts_recommendations(self):
        return print(self.ticker.recommendations)

    # show next event (earnings, etc)
    def calendar(self):
        return print(self.ticker.calendar)

    # ISIN = International Securities Identification Number
    def ISIN(self):
        return print(self.ticker.isin)

    # show options expirations
    def options(self):
        return print(self.ticker.options)

    # show news
    def news(self):
        return print(self.ticker.news)


