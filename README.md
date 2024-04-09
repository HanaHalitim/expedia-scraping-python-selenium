# expedia-scraping-python-selenium
This Python script uses Selenium WebDriver to automate the process of finding the cheapest flights on Expedia.

## Requirements
- Python 3
- Selenium WebDriver
- ChromeDriver
 
## Usage
Define your flight details in the `departure_flight_inputs` and `return_flight_inputs` dictionaries at the beginning of the script. 

## Notes
- The script is set to prefer one-way and non-stop flights.
- The script sorts the results by lowest price.
- The script prints the details of the first 5 available flights.
- Make sure to update the path to the ChromeDriver executable in the Service function call.
- It’s crucial to ensure that the version of ChromeDriver you’re using is compatible with your installed version of Google Chrome. To check your Chrome version, click on the three-dot menu in the top-right corner of any Chrome window, then navigate to ‘Help’ and select ‘About Google Chrome’. Once you’ve identified your Chrome version, you can download the corresponding ChromeDriver from chromedriver.chromium.org.
- Please note that due to potential updates and changes to the Expedia website, the functionality of this script may vary over time. Regular maintenance and adjustments to the code may be required to keep it functional.
