from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

# Initialize a Chrome webdriver
driver = webdriver.Chrome()

# Initial URL
url = "https://orangebookvalue.com/"

# Navigate to the URL
driver.get(url)

try:
    # Find the "New" nav item with id 'new-tab' and click it
    new_tab_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "new-tab"))
    )
    new_tab_item.click()
    
    # Wait for the content of the 'New' tab to be visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "new"))
    )
    
    # Get the page source after clicking the "New" tab
    page_source = driver.page_source
    
    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find the content within the "New" tab
    new_tab_content = soup.find('div', id='new')
    if new_tab_content:
        # Find the form within the "New" tab
        form = new_tab_content.find('form', id='newForm')
        if form:
            print("Form found within the 'New' tab:")
            action_url = form.get('action')
            method = form.get('method', 'post').lower()  # Default to POST if method is not specified
        
            form_html = form.prettify()
            
            # Extract form action URL and method
            action_url = form.get('action')
            method = form.get('method', 'post').lower()  # Default to POST if method is not specified

            # Ensure the action URL is complete (handle relative URLs)
            if not action_url.startswith('http'):
                action_url = url.rstrip('/') + '/' + action_url.lstrip('/')

            # Prepare the form data for submission
            form_data = {
                'feature': 'new',
                'newcategory': '1',  # Example: '1' for Car
                'newmake': 'Audi',  # Example: 'Toyota'
                'newmodel': 'Q3',  # Example: 'Corolla'
                'newtrim': 'Technology',  # Example: 'LE'
                'phone': '1111111111',  # From hidden input
                'userType': 'dealer',  # From hidden input
                'newcity': 'Agra'  # Example: 'New York'
            }

            # Submit the form using the appropriate method
            if method == 'post':
                response = requests.post(action_url, data=form_data)
            elif method == 'get':
                response = requests.get(action_url, params=form_data)
            else:
                print(f"Unsupported form method: {method}")
                response = None
                
            # Check if the request was successful
            data = {'Category': 'Car', 'Make': make, 'Model': model, 'Year': year, 'Trim': trim }
            if response and response.status_code == 200:
                # Parse the response text using BeautifulSoup
                response_soup = BeautifulSoup(response.text, 'html.parser')

                # Find the div with class 'vehicle main-result'
                block_div = response_soup.find('div', class_='left_content col-md-6')
                if block_div:
                    print("Div with class 'vehicle main-result' found in the response:")
                    # print(block_div.prettify())

                    # Extract and print the values of interest
                    on_road_price = block_div.find('span', id='on_road_price_id').find('strong').text.strip()
                    ex_showroom_price = block_div.find('span', id='ex_showroom_price_id').find('strong').text.strip()
                    rto = block_div.find('span', id='rto_id').find('strong').text.strip()
                    insurance = block_div.find('span', id='insurance_id').find('strong').text.strip()
                    tcs = block_div.find('span', id='tcs_id').find('strong').text.strip()
                    hypothecation = block_div.find('span', id='hypothecation_id').find('strong').text.strip()
                    hsrp = block_div.find('span', id='hsrp_id').find('strong').text.strip()
                    fastag = block_div.find('span', id='fastag_id').find('strong').text.strip()
                      
                    data['Price'] = on_road_price  
                    data['Ex Price'] = ex_showroom_price  
                    data['Rto'] = rto  
                    data['Insurance'] = insurance  
                    data['TCS'] = tcs  
                    data['hypothention'] = hypothecation  
                    data['hsrp'] = hsrp  
                    data['fastag'] = fastag  
                    car_data.append(data)

                else:
                    print("Div with class 'vehicle main-result' was not found in the response.")
            else:
                print(f"Failed to submit the form. Status code: {response.status_code}")
                if response:
                    print(response.text)
        else:
            print("Form with id 'newForm' was not found within the 'New' tab.")
    else:
        print("Content of the 'New' tab was not found.")
    
finally:
    # Close the webdriver
    driver.quit()
