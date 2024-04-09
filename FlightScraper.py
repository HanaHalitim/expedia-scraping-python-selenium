#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
import re
from datetime import datetime

# Define flight details for departure and return
departure_flight_inputs={'Departure': "FRA", 'Arrival': "CDG", 'Date': "30 April 2024"}
return_flight_inputs={'Departure': "CDG", 'Arrival': "FRA", 'Date': "30 May 2024"}

# Function to find the cheapest flights given flight information
def find_cheapest_flights(flight_info):
    # Initialize Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")

    # Set the path to the Chrome driver
    service = Service('C:\\Users\\latitude\\Desktop\\chromedriver-win32\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Get flight details from the flight_info dictionary
    leaving_from = flight_info['Departure']
    going_to = flight_info['Arrival']
    trip_date = flight_info['Date']
    
    # Open the Expedia website
    driver.get("https://www.expedia.com/")

    # Click on the Flights tab
    flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
    flight_element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, flight_xpath)))
    flight_element.click()
    time.sleep(1)
    
    # Select the One-Way option for the flight
    oneway_xpath = '//a[@aria-controls="FlightSearchForm_ONE_WAY"]' 
    one_way_element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, oneway_xpath)))
    one_way_element.click()
    time.sleep(1)

    # Fill in the departure location
    pop_up_xpath = '//button[@id="onetrust-accept-btn-handler"]'
    pop_up = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, pop_up_xpath)))
    pop_up.clear
    pop_up.click()
    time.sleep(1)
    
    leaving_from_button_xpath = '//button[@aria-label="Leaving from"]'
    leaving_from_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, leaving_from_button_xpath)))
    leaving_from_button.click()

    leaving_from_input_xpath = '//input[@placeholder="Leaving from"]'  
    leaving_from_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, leaving_from_input_xpath)))
    leaving_from_input.clear()
    leaving_from_input.send_keys(leaving_from)
    time.sleep(5)  # Time for the autocomplete options to appear

    leaving_from_input.send_keys(Keys.DOWN, Keys.RETURN)

    # Fill in the arrival location
    going_to_button_xpath = '//button[@aria-label="Going to"]'
    going_to_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, going_to_button_xpath)))
    going_to_button.click()

    going_to_input_xpath = '//input[@placeholder="Going to"]'  
    going_to_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, going_to_input_xpath)))
    going_to_input.clear()
    going_to_input.send_keys(going_to)
    time.sleep(5)  # Time for the autocomplete options to appear

    going_to_input.send_keys(Keys.DOWN, Keys.RETURN)

    # Fill in the departure date
    departing_box_xpath = '//button[contains(@aria-label,"Date")]'
    depart_box_element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, departing_box_xpath)))
    depart_box_element.click() #Click on the departure box
    time.sleep(2)

    trip_date = datetime.strptime(departure_flight_inputs['Date'], "%d %B %Y")
    def navigate_to_month_year(driver, target_date):
        current_month_year_xpath = "//span[@class='uitk-align-center uitk-month-label']"  
        next_button_xpath = "//button[@data-stid='uitk-calendar-navigation-controls-next-button']"
    
        target_month_year = target_date.strftime("%B %Y")
        while True:
            current_month_year = driver.find_element(By.XPATH, current_month_year_xpath).text
            if current_month_year == target_month_year:
                break
            else:
                driver.find_element(By.XPATH, next_button_xpath).click()
    def select_day(driver, target_date):
        day = target_date.day
        day_xpath = f"(//div[@role='button'])[{day}]"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, day_xpath))).click()
    navigate_to_month_year(driver, trip_date)
    select_day(driver, trip_date)

    depart_date_done_xpath = '//*[@id="FlightSearchForm_ONE_WAY"]/div/div[2]/div/section/footer/div/button'
    driver.find_element(By.XPATH, depart_date_done_xpath).click()
    time.sleep(2)

    # Click the search button
    search_button_xpath = '//*[@id="search_button"]'
    driver.find_element(By.XPATH, search_button_xpath).click()
    time.sleep(15) #Need to let the page load properly

    # Check for available flights and sort by lowest price
    available_flights_xpath = "//span[contains(text(),'Select and show fare information ')]"
    available_flights = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, available_flights_xpath)))

    flights = []

    if available_flights:
        print("Available flights found. Processing...")
        
        for item in available_flights[:5]:  # Limit to first 5 flights
            text = item.text
            
            departure_match = re.search(r'departing at (\d{1,2}:\d{2}[ap]m)', text)
            departure_time = departure_match.group(1) if departure_match else 'N/A'
            
            arrival_match = re.search(r'arriving at (\d{1,2}:\d{2}[ap]m)', text)
            arrival_time = arrival_match.group(1) if arrival_match else 'N/A'
            
            price_match = re.search(r'Priced at (\$\d+)', text)
            price = price_match.group(1) if price_match else 'N/A'
            
            flights.append((departure_time, arrival_time, price))
        
        if len(available_flights) > 1:
            try:
                sort_option_xpath = '//option[@value="PRICE_INCREASING"]'  # Update this XPath as needed
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, sort_option_xpath))).click()
                print("Sorted flights by lowest price.")
                time.sleep(5)  # Wait for sort to apply
            except Exception as e:
                print(f"Could not sort flights due to: {e}")
        
        print("Conditions satisfied for: Departure:{}, Arrival:{}, Date:{}".format(leaving_from, going_to, trip_date))
    else:
        print('Not all conditions could be met for: "Departure:{}, Arrival:{}, Date:{}'.format(leaving_from, going_to, trip_date))

    driver.quit()
    return flights

print(find_cheapest_flights(departure_flight_inputs))
