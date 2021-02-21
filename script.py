import csv
import paramaters
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import ActionChains

from time import sleep

def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open(paramaters.file_name, 'w'))
writer.writerow(['Name', 'Job Title', 'Company', 'School', 'Location', 'URL'])

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys(paramaters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys(paramaters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@class="sign-in-form__submit-button"]')
sign_in_button.click()
sleep(5)

driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(paramaters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls = []

for i in range(10):
    links = driver.find_elements_by_xpath('//div[@class="yuRUbf"]/a[@href]')
    # links = br.find_elements_by_xpath("//h3[@class='r']/a[@href]")
    for link in links:
        # title = link.text.encode('utf8')
        url = link.get_attribute('href')
        # title_url = (title, url)
        linkedin_urls.append(url)
    # linkedin_url = linkedin.get_attribute('href')
    # linkedin_urls = [url[1:].text for url in linkedin_urls]
    sleep(0.5)

    next_button = driver.find_element_by_link_text("Berikutnya")
    next_button.click()


for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//*[starts-with(@class, "inline")]/text()').get().strip()

    job_title = sel.xpath('//div/h2/text()').get().strip()

    company = sel.xpath('//*[@id="ember66"]/text()').get()
    if company:
        company = company.strip()

    school = sel.xpath('//*[@id="ember69"]/text()').get()
    if school:
        school = school.strip()

    location = sel.xpath('//*[starts-with(@class, "t-16")]/text()').get().strip()

    linkedin_url = driver.current_url

    name = validate_field(name)
    job_title = validate_field(job_title)
    company = validate_field(company)
    school = validate_field(school)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)
    

    print('\n')
    print('Name: ' + name)
    print('Job Title: ' + job_title)
    print('Company: ' + company)
    print('School: ' + school)
    print('Location: ' + location)
    print('URL: ' + linkedin_url)
    print('\n')

    writer.writerow([name,
                     job_title,
                     company,
                     school,
                     location,
                     linkedin_url])

    # try:
    #     driver.find_element_by_xpath('//span[text()="Connect"]').click()
    #     sleep(3)

    #     driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click()
    #     sleep(3)

    # except:
    #     pass

driver.quit()
