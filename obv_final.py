import requests
from bs4 import BeautifulSoup
import pandas as pd

car_data = []

def process_year_data(make, model, year, trim):
    # Write your logic to process year data here
    print(f"Processing data for {make} {model} {year} {trim}")

    # Initial URL
    url = "https://orangebookvalue.com/"

    # Headers for HTTP requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    # Send the initial request and get the page content
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the form with id 'newForm'
    form = soup.find('form', id='vehicleForm')
    if not form:
        print("The form with id 'newForm' was not found.")
        return

    # Extract the form action URL and method
    action_url = form.get('action')
    method = form.get('method', 'post').lower()  # Default to POST if method is not specified

    # Ensure the action URL is complete (handle relative URLs)
    if not action_url.startswith('http'):
        action_url = url.rstrip('/') + '/' + action_url.lstrip('/')

    # Prepare the form data for submission
    form_data = {
        'feature': 'used',
        'category': 'Car',  # Car
        'make': make,
        'model': model,
        'year': year,
        'trim': trim, 
        'kms_driven': '10',  # Example value
        'city': 'Delhi',  # Example value; ensure this is filled with a valid value
        'phone': '1111111111',
        'userType': 'Individual',
        'transaction_type': 's',
        'is_taxi': '0'
    }

    # Submit the form using the appropriate method
    if method == 'post':
        response = requests.post(action_url, data=form_data, headers=headers)
    elif method == 'get':
        response = requests.get(action_url, params=form_data, headers=headers)
    else:
        print(f"Unsupported form method: {method}")
        return

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to submit the form. Status code: {response.status_code}")
        print(response.text)
    else:
        # Parse the response content
        data = {'Category': 'Car', 'Make': make, 'Model': model, 'Year': year, 'Trim': trim }
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())
        # Find the div with the class 'price price-scroll mainPrice'
        price_div = soup.find('div', class_='price price-scroll mainPrice')
        
        if price_div:
            # Print the content of the div
            price_span = price_div.find('span')
            if price_span:
                price_range = price_span.get_text(strip=True).replace(' - ', '-').replace('₹', 'Rs.')
                price_range = price_range.replace('\n', '')
                print(price_range)
                if '-' in price_range:
                    min_price, max_price = price_range.split('-')
                    min_price = min_price.replace('Rs.', '').strip()
                    max_price = max_price.replace('Rs.', '').strip()
                    data['Min Price'] = 'Rs. ' + min_price
                    data['Max Price'] = 'Rs. ' + max_price
                else:
                    single_price = price_range.replace('Rs.', '').strip()
                    data['Min Price'] = 'Rs. ' + single_price
                    data['Max Price'] = None  # or handle appropriately if only one price is provided
                car_data.append(data)
            else:
                print("Price not found.")
        else:
            print("The div with class 'price price-scroll mainPrice' was not found.")


# Initial API URL
api_url = "https://orangebookvalue.com/mmt_new?&category_id=1&api_version=3"

# Send the initial API request and get the response
response = requests.get(api_url)

# Check if the initial request was successful
if response.status_code != 200:
    print(f"Failed to retrieve the API response. Status code: {response.status_code}")
else:
    # Parse the JSON response content
    response_data = response.json()
    make = "Audi"
    models_url = f"https://orangebookvalue.com/mmt_new?&category_id=1&make={make}&api_version=3"
        
    # Send the request to get models for the specific make
    models_response = requests.get(models_url)
        
    # Check if the request was successful
    if models_response.status_code != 200:
        print(f"Failed to retrieve the API response for {make}. Status code: {models_response.status_code}")
    else:
         # Parse the JSON response content for the specific make
        models_response_data = models_response.json()
            
        # Extract the models from the 'data' array
        models = models_response_data.get('data', [])
            
        # Loop through each model and call the final API
        for model in models:
            # Construct the final API URL for each make and model
            final_url = f"https://orangebookvalue.com/mmt_new?&category_id=1&make={make}&model={model}&api_version=3"
                
            # Send the request to the final API URL
            final_response = requests.get(final_url)
                
             # Check if the request was successful
            if final_response.status_code != 200:
                  print(f"Failed to retrieve the API response for {make} {model}. Status code: {final_response.status_code}")
            else:
                 # Parse the JSON response content for the specific make and model
                final_response_data = final_response.json()
                    
                # Extract and print the array inside the 'data' key
                data_array = final_response_data.get('data', [])
                    
                # For each year in data_array, call the API with the year
                for year in data_array:
                     year_api_url = f"https://orangebookvalue.com/mmt_new?&category_id=1&make={make}&model={model}&year={year}&check_obv=1&api_version=3"
                     year_response = requests.get(year_api_url)
                     if year_response.status_code != 200:
                        print(f"Failed to retrieve the API response for {make} {model} {year}. Status code: {year_response.status_code}")
                     else:
                         year_response_data = year_response.json()
                         year_data_array = year_response_data.get('data', [])

                         if year_data_array:
                            year_data = year_data_array.get('result', [])
                            # print(f"Data for {make} {model} {year}:")
                            
                            for trim in year_data:
                             process_year_data(make, model, year, trim)
            

# Create DataFrame from the list of car data
df = pd.DataFrame(car_data)

# Save DataFrame to a CSV file
df.to_csv(f"{make}newCar.csv", index=False)