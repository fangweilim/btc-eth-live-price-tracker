import requests
import time

# Constants
REQUEST_INTERVAL = 60  # Minimum interval between requests in seconds
CACHE_DURATION = 120  # Duration to cache responses in seconds

# Cache variables
cache = {}
cache_time = 0

def get_crypto_prices():
    global cache, cache_time
    
    current_time = time.time()
    
    # Check if the cache is still valid
    if current_time - cache_time < CACHE_DURATION:
        return cache.get('bitcoin_price'), cache.get('ethereum_price'), cache.get('bitcoin_change'), cache.get('ethereum_change')
    
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'usd',
        'include_24hr_change': 'true'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        
        data = response.json()
        
        bitcoin_price = data['bitcoin']['usd']
        ethereum_price = data['ethereum']['usd']
        bitcoin_change = data['bitcoin']['usd_24h_change']
        ethereum_change = data['ethereum']['usd_24h_change']
        
        # Cache the data
        cache = {
            'bitcoin_price': bitcoin_price,
            'ethereum_price': ethereum_price,
            'bitcoin_change': bitcoin_change,
            'ethereum_change': ethereum_change
        }
        cache_time = current_time
        
        return bitcoin_price, ethereum_price, bitcoin_change, ethereum_change
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, None, None, None
    except KeyError as e:
        print(f"Data parsing error: {e}")
        return None, None, None, None

def main():
    previous_bitcoin_price = None
    previous_ethereum_price = None

    while True:
        bitcoin_price, ethereum_price, bitcoin_change, ethereum_change = get_crypto_prices()
        
        if bitcoin_price is None or ethereum_price is None:
            print("Failed to fetch data. Retrying in 10 seconds.")
        else:
            if previous_bitcoin_price is None or previous_ethereum_price is None:
                # Initialize previous prices
                previous_bitcoin_price = bitcoin_price
                previous_ethereum_price = ethereum_price
                print(f"Bitcoin price: ${bitcoin_price:.2f} (24h Change: {bitcoin_change:.2f}%)")
                print(f"Ethereum price: ${ethereum_price:.2f} (24h Change: {ethereum_change:.2f}%)")
                print('-' * 30)
            else:
                if bitcoin_price != previous_bitcoin_price or ethereum_price != previous_ethereum_price:
                    print(f"Bitcoin price: ${bitcoin_price:.2f} (24h Change: {bitcoin_change:.2f}%)")
                    print(f"Ethereum price: ${ethereum_price:.2f} (24h Change: {ethereum_change:.2f}%)")
                    print('-' * 30)
                
                # Update previous prices
                previous_bitcoin_price = bitcoin_price
                previous_ethereum_price = ethereum_price
        
        # Sleep for the specified interval
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    main()