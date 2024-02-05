import time
from selenium import webdriver
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException, TimeoutException

website = 'https://www.sec.gov/edgar/search/?fbclid=IwAR0QhrfhVCRCfU8p1UERnZGgCvY0Mbydh9W0Oo4YTi4mQ3ti0Juhex6V71s#/dateRange=custom&category=custom&startdt=2024-01-15&enddt=2024-01-18&forms=8-K'

driver = webdriver.Chrome()
driver.get(website)

link_visit = []
summary = []
company_name = []
date_filed = []

while True:
    try:
        time.sleep(10)

        # Scraping company_name and date_filed
        companys = driver.find_elements(By.XPATH, '//td[@class="entity-name"]')
        for company in companys:
            company_name.append(company.get_attribute('innerText'))

        dates = driver.find_elements(By.XPATH, '//td[@class="filed"]')
        for date in dates:
            date_filed.append(date.get_attribute('innerText'))

        # Wait until post_links are present in the DOM
        post_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//td[@class="filetype"]/a'))
        )

        for post_link in post_links:
            # Get the href attribute before clicking to handle the pop-up window
            # to_catch = post_link.get_attribute('href')

            # Click on the post link
            post_link.click()

            # Wait for the pop-up to appear
            to_catch = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[3]/a[1]'))
            ).get_attribute('href')

            # Do something with the 'to_catch' attribute (e.g., append it to a list)
            link_visit.append(to_catch)

            # Close the pop-up
            post_close_button = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button')
            post_close_button.click()

        # Find the next page link and click it
        next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/nav/ul/li[12]/a'))
        )
        time.sleep(5)
        next_page.click()

    except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
        # If the next page link is not found or any exception occurs, exit the loop
        break

driver.quit()

def Summary():
    driver = webdriver.Chrome()

    for url in link_visit:
        # Visit the URL
        driver.get(url)

        # Extract summ_elements
        summ_elements = driver.find_elements(By.XPATH, """(//*[self::p or self::span][contains(text(), 'On') and (contains(text(), 'January') or contains(text(), 'February') or contains(text(), 'March') or contains(text(), 'April') or contains(text(), 'May') or contains(text(), 'June') or contains(text(), 'July') or contains(text(), 'August') or contains(text(), 'September') or contains(text(), 'October') or contains(text(), 'November') or contains(text(), 'December'))])""")

        # Process summ_elements
        if len(summ_elements) > 1:
            # Concatenate texts if there are multiple summ_elements
            summary_text = ' '.join(element.text for element in summ_elements)
        elif len(summ_elements) == 1:
            # Get text if there is only one summ_elements
            summary_text = summ_elements[0].text
        else:
            # Handle the case where no summ_elements are found
            summary_text = "No summary found."

        # Extract the text content of the entire HTML
        overall_text = driver.find_element(By.TAG_NAME, 'body').text

        # Append the summary and overall_text to the lists
        summary.append(summary_text)
        overall_text_list.append(overall_text)
        time.sleep(1)

    driver.quit()

# Initialize a list to store overall_text for each URL
overall_text_list = []

# Call the Summary function
Summary()

# Create a DataFrame with the new 'overall_text' column
df = pd.DataFrame({'company_name': company_name,
                   'summary': summary,
                   'date_filed': date_filed,
                   'link_visit': link_visit,
                   'overall_text': overall_text_list})

# # # Save the DataFrame to a CSV file
# # df.to_csv('213balconys12323232ample1_csv.csv', index=False)
#
# # Filter rows where 'overall_text' contains "Item 1.05" (case insensitive)
# filtered_df = df[df['overall_text'].str.contains("Item 1.05", case=False)]
#
# # Create a new DataFrame with selected columns
# result_df = filtered_df[['company_name', 'summary', 'date_filed', 'link_visit']]
#
#
#
#
# # Initialize a new DataFrame to store matching entries
# filtered_df = pd.DataFrame(columns=df.columns)



# Create a DataFrame with the new 'overall_text' column
df = pd.DataFrame({'company_name': company_name,
                   'summary': summary,
                   'date_filed': date_filed,
                   'link_visit': link_visit,
                   'overall_text': overall_text_list})

# Filter rows where 'overall_text' contains "Item 1.05" (case insensitive)
filtered_df = df[df['overall_text'].str.contains("Item 1.05", case=False)]

# Create a new DataFrame with selected columns
result_df = filtered_df[['company_name', 'summary', 'date_filed', 'link_visit']]

# Save the filtered DataFrame to a CSV file
# Remove duplicate rows based on 'company_name' and 'date_filed'
result_df = filtered_df.drop_duplicates(subset=['company_name', 'date_filed'])

# Create a new DataFrame with selected columns
result_df = result_df[['company_name', 'summary', 'date_filed', 'link_visit']]

# Save the filtered and de-duplicated DataFrame to a CSV file
result_df.to_csv('Items.csv', index=False)




