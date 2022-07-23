"""
Web scraper for Ladok web services

David Bergh
berghdavid@hotmail.com
"""

from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT_MAX = 5
COURSES_URL = "https://www.student.ladok.se/student/app/studentwebb/min-utbildning/avklarade"

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
        print("Error: Could not find " + str(identifier) + ": " + str(name))
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
        print("Error: Could not find " + str(identifier) + ": " + str(name))
        return None

def find_course_status(driver):
    """ Find the status of the course. """
    badges = [
        'badge-light',
        'badge-success',
        'badge-primary'
    ]
    for badge in badges:
        try:
            return driver.find_element(By.CLASS_NAME, badge)
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

def retrieve_course_links(driver):
    """
    Retrieve links to all the different courses from ladok, assuming that the driver is currently
    located at the 'courses' webpage.
    """
    elements = wait_find_elements(driver, By.CLASS_NAME, "ladok-accordian")
    course_links = []
    first_list = elements[0]
    for course in first_list.find_elements(By.CLASS_NAME, "ladok-list-kort"):
        course_link = course.find_element(By.CLASS_NAME, "card-link").get_attribute("href")
        course_links.append(course_link)
    return course_links

def retrieve_grades(driver, course_links):
    """
    Retrieve grades from all the given course links.
    """
    courses = []
    for link in course_links:
        driver.get(link)
        course_name_element = wait_find_element(driver, By.TAG_NAME, "h1")
        status_element = find_course_status(driver)
        grade_element = wait_find_element(
            driver, By.CLASS_NAME, "ladok-list-kort-header-rubrik", 0
        )

        if course_name_element and status_element and grade_element:
            course_name = course_name_element.text
            status = status_element.text
            grade = grade_element.text[-2]
            # --- Example grade ---
            # Final grade: Pass with credit (4)

            print("Adding " + course_name)
            courses.append({
                'name': course_name,
                'status': status,
                'grade': grade
            })
    return courses

def main():
    """ Main method """
    login_info = get_login_info()
    driver = webdriver.Chrome()
    login(driver, login_info)
    course_links = retrieve_course_links(driver)
    grades = retrieve_grades(driver, course_links)
    print(grades)
    driver.close()

if __name__ == '__main__':
    main()
