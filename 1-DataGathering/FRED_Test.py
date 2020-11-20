from fredapi import Fred

key_path = "../../FRED.txt"

apiKey = open(key_path, 'r').read()

fred = Fred(api_key=apiKey)
data = fred.get_series('SP500')
print(data)