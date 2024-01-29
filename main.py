import time
import requests
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException


website = 'https://www.sec.gov/edgar/search/?fbclid=IwAR0QhrfhVCRCfU8p1UERnZGgCvY0Mbydh9W0Oo4YTi4mQ3ti0Juhex6V71s#/dateRange=custom&category=custom&startdt=2024-01-26&enddt=2024-01-28&forms=8-K'

driver = webdriver.Chrome()
time.sleep(10)
driver.get(website)

time.sleep(10)

link_visit = []
summary = []
company_name = []
date_filed = []    
while True:
    try:
        time.sleep(10)

        companys = driver.find_elements("xpath", '//td[@class="entity-name"]')
        for company in companys:
            company_name.append(company.get_attribute('innerText'))

        dates = driver.find_elements("xpath", '//td[@class="filed"]')
        for date in dates:
            date_filed.append(date.get_attribute('innerText'))            

        # Wait until post_links are present in the DOM
        post_links = driver.find_elements("xpath", '//td[@class="filetype"]/a')

        # Iterate through each post link
        for post_link in post_links:
            # Click on the post link
            post_link.click()

            # Wait for the pop-up to appear
            to_catch = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(("xpath", '/html/body/div[4]/div/div/div[3]/a[1]'))
            ).get_attribute('href')

            # Do something with the 'to_catch' attribute (e.g., append it to a list)
            link_visit.append(to_catch)


            # Close the pop-up
            post_close_button = driver.find_element("xpath", '/html/body/div[4]/div/div/div[3]/button')
            post_close_button.click()

        # Find the next page link and click it
        next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", '/html/body/div[3]/div[2]/div[2]/nav/ul/li[12]/a'))
        )
        time.sleep(5)
        next_page.click()

    except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
        # If the next page link is not found or any exception occurs, exit the loop
        break

driver.quit()

def Summary():
    driver = webdriver.Chrome()

    for url in link_visit:
        # Visit the URL
        driver.get(url)

        # Extract summ_elements
        summ_elements = driver.find_elements("xpath", """(//*[self::p or self::span][contains(text(), 'On') and (contains(text(), 'January') or contains(text(), 'February') or contains(text(), 'March') or contains(text(), 'April') or contains(text(), 'May') or contains(text(), 'June') or contains(text(), 'July') or contains(text(), 'August') or contains(text(), 'September') or contains(text(), 'October') or contains(text(), 'November') or contains(text(), 'December'))])""")

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

        # Append the summary to the list
        summary.append(summary_text)

    driver.quit()
Summary()

df = pd.DataFrame({'company_name': company_name,
                   'summary': summary,
                   'date_filed': date_filed,
                   'link_visit':link_visit,})

df.to_csv('sample_csv.csv', index=False)