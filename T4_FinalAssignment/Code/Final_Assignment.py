import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

tesla = yf.Ticker("TSLA")

tesla_data = tesla.history(period="max")

tesla_data.reset_index(inplace=True)
#print(tesla_data.head())

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html.parser')

# Find all tables on the page
tables = soup.find_all('table')

# Initialize an empty DataFrame with columns "Date" and "Revenue"
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])


# Find all tables in HTML
tables = soup.find_all('table')

# Find relevant table
for table in tables:
    if "Tesla Quarterly Revenue" in table.get_text():
        for row in table.find('tbody').find_all('tr'):
            col = row.find_all('td')
            date = col[0].text
            revenue = col[1].text
            tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)
    else:
        continue
tesla_revenue.head()


# Se eliminan las comas y los simbolos de dolar
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(r',|\$',"", regex=True)

# Se eliminan los valores nulos de la tabla
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Se imprime por pantalla
print(tesla_revenue)


################# Con Pandas
tesla_read_html_pandas = pd.read_html(url)
tesla_revenue = tesla_read_html_pandas[1]
tesla_revenue.columns = ['Date','Revenue (MIllions of US $)']
tesla_revenue.head()

# Question 3

game_stop = yf.Ticker("GME")

gme_data = game_stop.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()
print(gme_data.head())

# Question 4

# Set the url
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

# HTML code
html_data_2 = requests.get(url).text

beautiful_soup = BeautifulSoup(html_data_2, 'html.parser')

# Create an empty DataFrame
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Find all tables in HTML
tables = beautiful_soup.find_all('table')

# Locate the needed table
for table in tables:
    # Check if correct table
    if "Quarterly" in table.get_text():
        for row in table.find('tbody').find_all('tr'):
            col = row.find_all('td')
            date = col[0].text
            revenue = col[1].text

            # Append the data of each row to the table
            gme_revenue = pd.concat([gme_revenue,pd.DataFrame({"Date":[date],"Revenue":[revenue]})], ignore_index=True)
    else:
        # Next table
        continue

gme_revenue.head()
print("\n")
print("\n")
print(f"Los datos de GameStop son: \n \n {gme_revenue}")