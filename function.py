# Imports
from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from pathlib import Path
import seaborn as sns
import hvplot.pandas
#%matplotlib inline
# initilize client
client = CoinGeckoAPI()
client.ping()

x = 0


def read_and_clean_1(start,end,coin):
    # Helper Functions
    def unix_time(year, month, day, hour, second):
        date_time = datetime.datetime(year, month, day, hour, second)
        return time.mktime(date_time.timetuple())

    def human_time(unix_time):
        return datetime.datetime.fromtimestamp(unix_time)


   
    # Reading in specified dates from API
    user_coin1 = client.get_coin_market_chart_range_by_id(
    id = coin,
    vs_currency = 'usd',
    from_timestamp=start,
    to_timestamp=end)
    
    # Making dataframes from API
    coin1_df = pd.DataFrame.from_dict(user_coin1)
    
    # Cleaning Coin1Data
    coin1_df['date'] = coin1_df['prices'][0][0]
    coin1_df[['time', 'price']] = coin1_df['prices'].apply(lambda x: pd.Series([x[0], x[1]]))
    coin1_df[['time2', 'market_cap']] = coin1_df['market_caps'].apply(lambda x: pd.Series([x[0], x[1]]))
    coin1_df[['time3', 'total_volume']] = coin1_df['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]]))
    
    coin1_df.drop('prices', axis=1, inplace=True)
    coin1_df.drop('market_caps', axis=1, inplace=True)
    coin1_df.drop('total_volumes', axis=1, inplace=True)
    coin1_df.drop('date', axis=1, inplace=True)
    coin1_df.drop('time2', axis=1, inplace=True)
    coin1_df.drop('time3', axis=1, inplace=True)
    
    coin1_df['time'] = pd.to_datetime(coin1_df['time'], unit='ms')   
    return coin1_df


def monte_carlo(start,end,coin):
    # Call read and clean
    coin1_df = read_and_clean_1(start,end,coin)
    # get a returns column that has the pct change applied to it
    returns = coin1_df["price"].pct_change()
    last_price =coin1_df["price"].iloc[-1]
    # set settings
    number_simulations = 1000
    number_days = 159
    simulation_df = pd.DataFrame()
    # create alogrithm for monte carlo sim
    for x in range(number_simulations):
        count = 0
        daily_volatility = returns.std()
        
        price_series = []
        
        price = last_price * (1 + np.random.normal(0, daily_volatility))
        price_series.append(price)
            
        for y in range(number_days):
            if count == 158:
                break
            price = price_series[count] * (1 + np.random.normal(0, daily_volatility))
            price_series.append(price)
            count +=1
        simulation_df[x] = price_series
    # plot simulation
    fig = plt.figure(figsize=(15,9))
    plt.plot(simulation_df)
    plt.axhline(y = last_price, color = 'r', linestyle = '-')
    plt.title("Monte Carlo Simulation ",  fontsize = 34)
    plt.xlabel('Day')
    plt.ylabel('Price - USD')
    plt.show()
    max_num = simulation_df.max().max()
    min_num = simulation_df.min().min()
    print("In a simulation of 159 days the predicted max is: " + "${:.2f}".format(max_num) + " and the predicted minimum is: " + "${:.2f}".format(min_num))
    

def sharpe_ratio(start,end,coin1,coin2,coin3='bitcoin',coin4='ethereum',coin5='tether'):
    # Getting input for specific coins/ dates
    coin1_df = read_and_clean_1(start,end,coin1)
    coin2_df = read_and_clean_1(start,end,coin2)

    # Check if user input matches default coins
    if coin1 == coin3 or coin2 == coin3:
        coin3 = 'dogecoin'  # Replace with backup coin
    if coin1 == coin4 or coin2 == coin4:
        coin4 = 'cardano'   # Replace with backup coin
    if coin1 == coin5 or coin2 == coin5:
        coin5 = 'monero'   # Replace with backup coin
    
    coin3_df = read_and_clean_1(start,end,coin3)
    coin4_df = read_and_clean_1(start,end,coin4)
    coin5_df = read_and_clean_1(start,end,coin5)
    
    # cleaning continued
    coin1_df = coin1_df.set_index('time')
    coin2_df = coin2_df.set_index('time')
    coin3_df = coin3_df.set_index('time')
    coin4_df = coin4_df.set_index('time')
    coin5_df = coin5_df.set_index('time')
    
    coin1_cleaned = coin1_df.drop(columns=['market_cap', 'total_volume'])
    coin2_cleaned = coin2_df.drop(columns=['market_cap', 'total_volume'])
    coin3_cleaned = coin3_df.drop(columns=['market_cap', 'total_volume'])
    coin4_cleaned = coin4_df.drop(columns=['market_cap', 'total_volume'])
    coin5_cleaned = coin5_df.drop(columns=['market_cap', 'total_volume'])
    
    # combined data 
    combined_data = pd.concat([coin1_cleaned, coin2_cleaned, coin3_cleaned, coin4_cleaned, coin5_cleaned], axis= 1, join="inner")
    
    #clean new data and find pct change
    combined_data = combined_data.pct_change().dropna()
    
    # Sharpe Ratios
    sharpe_ratios = (combined_data.mean()*252) / (combined_data.std() * np.sqrt(252))
    sharpe_plot = sharpe_ratios.plot(kind = "bar")
    
    # Label the plot
    sharpe_plot.set_xlabel('Coins')
    sharpe_plot.set_ylabel('Sharpe Ratio')
    
     # Set xtick labels to be the names of the coins
    sharpe_plot.set_xticklabels([coin1, coin2, coin3, coin4, coin5])
    
    print(sharpe_plot)

def heatmap(start,end,coin1,coin2):
    coin1_df = read_and_clean_1(start,end,coin1)
    coin2_df = read_and_clean_1(start,end,coin2)
    
    combined = pd.merge(coin1_df.rename(columns={'price': coin1 + ' price', 
                                                  'market_cap' : coin1 + ' market caps',
                                                  'total_volume' : coin1 + ' total volumes'
                                                 }),
                        coin2_df.rename(columns={'price': coin2 + ' price', 
                                                  'market_cap' : coin2 +' market caps',
                                                  'total_volume' : coin2 + ' total volumes'
                                                 }),
                        on='time')
#Apply correlation method over df
    corr_df = combined.corr()
#display dataframe
    display(sns.heatmap(corr_df, cmap='coolwarm', annot=True))

def calc_exchange_ratio(start,end,coin1,coin2):
    coin1 = read_and_clean_1(start,end,coin1)
    coin2 = read_and_clean_1(start,end,coin2)
    exchange_df = pd.merge(coin1,coin2, on='time',suffixes=('_1','_2'))                           
    exchange_df['exchange_rate'] = exchange_df['price_1']/exchange_df['price_2']
    #print(exchange_df.head(5)) 
    exchange_df.plot(x='time', y='exchange_rate')
    plt.show()

def graph_trading_volumes(start,end,coin1,coin2):
    coin1 = read_and_clean_1(start,end,coin1)
    coin2 = read_and_clean_1(start,end,coin2)
    merged_df =  pd.merge(coin1,coin2, on='time',suffixes=('_1','_2'))    
    plt.plot(merged_df['time'], merged_df['total_volume_1'])
    plt.plot(merged_df['time'], merged_df['total_volume_2'])
    plt.xlabel('Time')
    plt.ylabel('Total Trade Volume')
    plt.title('Trade Volume Over Time')
    plt.legend()
    plt.show()

def graph_market_cap(start,end,coin1,coin2):
    coin1_df = read_and_clean_1(start,end,coin1)
    coin2_df = read_and_clean_1(start,end,coin2)
    coin1_df = coin1_df.drop(columns=['market_cap', 'total_volume'])
    coin2_df = coin2_df.drop(columns=['market_cap', 'total_volume'])
    merge_df = pd.merge(coin1_df.rename(columns={'price' : coin1 + ' price', 
                                                 }),
                        coin2_df.rename(columns={'price' : coin2 + ' price', 
                                                 }),
                        on='time')
    display(merge_df.hvplot.line(x='time', 
                        title = 'Price over Time',
                       logy=True,
                        height=600,
                        width=1200,
                        use_index=False,
                       ).opts(yformatter='%.0f'))
    
    #merged_df =  pd.merge(coin1,coin2, on='time',suffixes=('_1','_2'))    
    #plt.plot(merged_df['time'], merged_df['market_cap_1'])
    #plt.plot(merged_df['time'], merged_df['market_cap_2'])
    #plt.xlabel('Time')
    #plt.ylabel('Market Cap')
    #plt.title('Market Cap Over Time')
   # plt.yscale('log')  # Set y-axis to log scale
   #plt.legend()
   # plt.show()