from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.cardekho.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html')

mainContainer = soup.find_all('div', id='main')

found = False
# Loop through the mainRow to find div with class "listitems gsc-row"
for row in mainContainer:
    listitems_div = row.find('div', class_='desktop')
    if listitems_div:
        # Do something with the listitems_div
        found = True

# If the div was not found, print a message
if not found:
    print("The div with class 'listitems gsc-row' was not found.")

appContent = listitems_div.find('div', class_='app-content')
gscContainerHomepage = listitems_div.find('div', class_='gsc_container homepage')
contentHold = gscContainerHomepage.find('div', class_='contentHold gsc_row')
car_divs = contentHold.find_all('div', class_='gsc_col-xs-12 holder truncate')

# Initialize an empty list to store car data
car_data = []

# Function to extract data for a single car
def extract_car_data(url, title, price_range):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Your code for extracting data from the page goes here
    mainContainer = soup.find_all('main', 'gsc_container')

    if mainContainer:
        container = mainContainer[0] 
        gsc_row = container.find('div', class_='gsc_row')  # Finding the first gsc_row
        if gsc_row:
            qccontent_div = gsc_row.find('div', class_='qccontent')  # Finding the qccontent div within the first gsc_row
            if qccontent_div:
                table = qccontent_div.find('table')

                # Extract table data
                data = {'Car Name': title, 'Price Range': price_range}
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        data[key] = value  # Store data as dictionary

                # Find top features div
                top_features_div = gsc_row.find('div', class_='gsc-ta-content', attrs={'data-track-section': 'Top Features'})
                top_features = []
                if top_features_div:
                  for li in top_features_div.find_all('li'):
                    top_features.append(li.find('span', class_='iconsname').text.strip())
                  top_features_string = ", ".join(top_features)
                  data['Top Features'] = top_features_string
                else:
                 data['Top Features'] = ['No top features found']

                # Find stand out features div
                stand_out_features_div = gsc_row.find('div', class_='gsc-ta-content', attrs={'data-track-section': 'Stand Out Features'})
                stand_out_features = []
                if stand_out_features_div:
                    for li in stand_out_features_div.find_all('li'):
                        image_url = li.find('img')['src'] if li.find('img') else ""
                        text = li.find('p').get_text().strip() if li.find('p') else ""
                        feature = f"Image URL: {image_url}, Text: {text}"
                        stand_out_features.append(feature)
                    stand_out_features_string = "\n".join(stand_out_features)
                    data['Stand Out Features'] = stand_out_features_string
                else:
                    data['Stand Out Features'] = 'No stand out features found'

                # Find variant
                variants_table = gsc_row.find('table', class_='allvariant contentHold', attrs={'data-track-section': 'All Version'})
                if variants_table:
                   variants = variants_table.find_all('tr')[1:]  # Exclude the header row

                   # Extract variant data
                   variants_text = []
                   for variant_row in variants:
                       cells = variant_row.find_all('td')
                       if len(cells) >= 2:
                          variant_name = cells[0].find('a').text.strip()
                          ex_showroom_price = cells[1].text.strip()
                          variant_text = f"{variant_name}: {ex_showroom_price}"
                          variants_text.append(variant_text)

                   # Add variants text to the data dictionary
                   data['Variants'] = "\n".join(variants_text) if variants_text else 'No variants found'
                else:
                  data['Variants'] = 'No variants found'

                # Initialize dictionaries to store exterior and interior data
                exterior_data = {}
                interior_data = {}
                main_section = gsc_row.find('section', class_='modelSpecsMain')
                if main_section:
                   exterior_section = main_section.find('div', {'data-id': 'Exterior'})
                   if exterior_section:
                   # Extract the content from the Exterior section
                       exterior_content = exterior_section.find('div', class_='featuresIocnsSec')
                       if exterior_content:
                          # Extract text content of the paragraphs
                          exterior_data['Exterior'] = [p.text.strip() for p in exterior_content.find_all('p')]
                          # Extract the image URL
                          exterior_image = exterior_content.find('img')
                          if exterior_image:
                              exterior_data['Exterior Image URL'] = exterior_image.get('data-gsll-src')

                          data['Exterior'] = exterior_data

                   interior_section = main_section.find('div', {'data-id': 'Interior'})
                   if interior_section:
                       # Extract the content from the Interior section
                       interior_content = interior_section.find('div', class_='featuresIocnsSec')
                       if interior_content:
                           # Extract text content of the paragraphs
                           interior_data['Interior'] = [p.text.strip() for p in interior_content.find_all('p')]
                           interior_image = interior_content.find('img')
                           if interior_image:
                               interior_data['Interior Image URL'] = interior_image.get('data-gsll-src')
                           data['Interior'] = interior_data   
                else:
                      data['Exterior'] = {'Exterior': ['No data']}
                      data['Interior'] = {'Interior': ['No data']}               

                # Append car data to the list
                car_data.append(data)
            else:
                print("No div with class 'qccontent' found within the first gsc_row.")
        else:
            print("No gsc_row found.")
    else:
        print("Main container not found.")

# Iterate through each car div and extract link and title
for car_div in car_divs:
    # Extract link and title
    anchor_tag = car_div.find('a', class_='title')
    if anchor_tag:
        link = anchor_tag.get('href')
        title = anchor_tag.get('title')
        
        # Print the link for each car
        print("Link:", link)
        
        # Construct the full URL
        full_url = "https://www.cardekho.com" + link
        
        # Run the code to extract data for the current link and append to the list
        
        price_span = car_div.find('div', class_='price')
        if price_span:
                price_range = price_span.text.strip().replace('*', '').strip()

        else:
           print("Price not found")
        extract_car_data(full_url, title, price_range)

# Create DataFrame from the list of car data
df = pd.DataFrame(car_data)

# Save DataFrame to a CSV file
df.to_csv("car_detail.csv", index=False)
