"""
Web scraper for Ladok web services

David Bergh
berghdavid@hotmail.com
"""

from getpass import getpass
import json
from alive_progress import alive_bar
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT_MAX = 5
COURSES_URL = "https://www.student.ladok.se/student/app/studentwebb/min-utbildning/alla"

def wait_find_element(driver, identifier, name, timeout = TIMEOUT_MAX):
    """
    Wait for page to load, then retrieve an element defined by its identifier and name.

    Examples
    --------
    >>> wait_get_element(driver, BY.id, username).text
    "ExampleUser"
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((identifier, name))
        )
    except TimeoutException:
        return None

def wait_find_elements(driver, identifier, name, timeout = TIMEOUT_MAX):
    """
    Wait for page to load, then retrieve elements defined by its identifiers and names.

    Examples
    --------
    >>> wait_get_elements(driver, BY.id, usernames)[0].text
    "ExampleUser"
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((identifier, name))
        )
    except TimeoutException:
        return None

def find_course_status(driver):
    """ Find the status of the course. """
    badges = [
        'badge-light',
        'badge-success',
        'badge-primary',
        'badge-danger'
    ]
    for badge in badges:
        try:
            return driver.find_element(By.CLASS_NAME, badge).text
        except NoSuchElementException:
            continue
    return 'credited'

def get_login_info():
    """ Request username and password which is used for login to Ladok. """
    username = input("Username: ")
    password = getpass("Password: ")
    return {
        'username': username,
        'password': password
    }

def init_webdriver():
    """ Initialize a clean new webdriver =) """
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=options)

def login(driver, login_info):
    """ Request username and password, which is then used to login to Ladok web services. """
    driver.get(COURSES_URL)
    wait_find_element(driver, By.CLASS_NAME, "btn-primary").click()
    wait_find_element(driver, By.ID, "searchinput").send_keys("Lund University")
    wait_find_element(driver, By.CLASS_NAME, "identityprovider").click()
    wait_find_element(driver, By.ID, "username").send_keys(login_info['username'])
    wait_find_element(driver, By.ID, "password").send_keys(login_info['password'])
    wait_find_element(driver, By.CLASS_NAME, "btn-submit").click()
    driver.get(COURSES_URL)
    return driver

def get_programme_course_links(driver):
    """
    Retrieve links to all the different courses from the different programmes located at Ladok.
    Assumes that the driver is currently located at the 'courses' webpage.
    """
    all_programmes = {}
    programme_containers = wait_find_elements(driver, By.TAG_NAME, "ladok-paketering")
    for programme in programme_containers:
        programme_name = programme.find_element(By.TAG_NAME, "h2").text
        programme_course_lists = programme.find_elements(By.CLASS_NAME, "ladok-accordian")
        course_links = []
        for course_list in programme_course_lists:
            for course in course_list.find_elements(By.CLASS_NAME, "ladok-list-kort"):
                course_link = course.find_element(By.CLASS_NAME, "card-link").get_attribute("href")
                course_links.append(course_link)
        all_programmes[programme_name] = course_links
    return all_programmes

def retrieve_grades(driver, all_programmes):
    """ Retrieve grades from all the given course links. """
    all_results = {}
    header_class = "ladok-list-kort-header-rubrik"
    size = len(all_programmes)
    print(f"Collecting grades from {size} programmes...")
    for programme_name, course_links in all_programmes.items():
        programme_results = []
        with alive_bar(len(course_links), title=programme_name) as loading_bar:
            for link in course_links:
                driver.get(link)
                course_name_element = wait_find_element(driver, By.TAG_NAME, "h1")
                status = find_course_status(driver)
                grade_element = wait_find_element(driver, By.CLASS_NAME, header_class, 0)

                if course_name_element and status:
                    course_name = course_name_element.text
                    if status == 'Completed' and grade_element:
                        if not grade:
                            print("Missing grade for: " + str(course_name) +
                                ", please edit to the correct grade inside 'grade.txt'")
                            continue
                        # Example: 'Final grade: Pass with credit (4)'
                        grade = grade_element.text[-2]
                    elif status == 'credited':
                        grade = 'credited'
                    else:
                        grade = 'U'

                    programme_results.append({
                        'name': course_name,
                        'status': status,
                        'grade': grade
                    })
                    # pylint: disable=not-callable
                    loading_bar()
        all_results[programme_name] = programme_results
    return all_results

def write_result_to_file(grades):
    """ Write grades to file in json format. """
    file_name = "grades.json"
    print(f"Writing grades to {file_name}...")
    with open(file_name, "w", encoding='UTF-8') as file:
        file.write(json.dumps(grades, indent=4))
        file.close()

def main():
    """ Main method """
    login_info = get_login_info()
    driver = init_webdriver()
    login(driver, login_info)
    all_programmes = get_programme_course_links(driver)
    grades = retrieve_grades(driver, all_programmes)
    write_result_to_file(grades)
    driver.close()
    print("Done")

if __name__ == '__main__':
    main()
