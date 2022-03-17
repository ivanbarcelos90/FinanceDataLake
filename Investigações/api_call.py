# Call function from API
import api_display_stock as api

# Call API class 
stock = api.APIStock('MSFT') # Microsoft stock

# Call info of a stock
# stock.info()

# Call history of a stock
stock.history()

# # Call actions of a stock
# stock.actions()

# # Call news
# stock.news()


