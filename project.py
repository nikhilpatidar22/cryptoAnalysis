import requests
import pandas as pd
import time

def cryptoData():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    api_key = '6fcd2f87-fc50-4759-806c-cce1c071c258'

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    params = {
        'start': '1',
        'limit': '50',
    }
    response = requests.get(url, headers=headers, params=params)


    if response.status_code == 200:
        data = response.json()
        dataframe=pd.DataFrame(data['data'])
        
    else:
        print(f'Error: {response.status_code} - {response.text}')
    df= pd.json_normalize(dataframe['quote'].apply(lambda x: x['USD']))
    
    df.head()
    df2=pd.concat([dataframe,df],axis=1)
    
    df3=df2[['name', 'symbol', 'price', 'volume_24h', 'market_cap', 'percent_change_24h']]
    
    outputFilename = "cryptoDataOutput.xlsx"
    df3.to_excel(outputFilename, index=False)

    top5Crypto = df3.nlargest(5, 'market_cap')
    print("Top 5 Cryptocurrencies by Market Cap:")
    print(top5Crypto[['name', 'symbol','market_cap']])


    averagePrice = df3['price'].mean()
    print(f"Average Price of the Top 50 Cryptocurrencies: ${averagePrice}")


    highestChange = df3['percent_change_24h'].max()
    lowestChange = df3['percent_change_24h'].min()

    highestChangeCrypto = df3[df3['percent_change_24h'] == highestChange]
    lowestChangeCrypto = df3[df3['percent_change_24h'] == lowestChange]

    print("\nHighest 24-Hour Percentage Price Change:")
    print(highestChangeCrypto[['name', 'symbol','percent_change_24h']])

    print("\nLowest 24-Hour Percentage Price Change:")
    print(lowestChangeCrypto[['name', 'symbol','percent_change_24h']])

def every5Minutes():
    while True:
        cryptoData()
        
        time.sleep(300) 

every5Minutes()
