"""
Web scraper for Ladok web services

David Bergh
berghdavid@hotmail.com
"""

from getpass import getpass
from alive_progress import alive_bar
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from utils import init_webdriver, wait_find_element, wait_find_elements, write_object_into_json_file

def prompt_login_info():
    """ Request username and password which is used for login to Ladok. """
    username = input("Ladok username: ")
    password = getpass("Ladok password: ")
    return {
        'username': username,
        'password': password
    }

def login(driver, login_info):
    """ Request username and password, which is then used to login to Ladok web services. """
    courses_url = "https://www.student.ladok.se/student/app/studentwebb/min-utbildning/alla"
    driver.get(courses_url)
    wait_find_element(driver, By.CLASS_NAME, "btn-primary").click()
    wait_find_element(driver, By.ID, "searchinput").send_keys("Lund University")
    wait_find_element(driver, By.CLASS_NAME, "identityprovider").click()
    wait_find_element(driver, By.ID, "username").send_keys(login_info['username'])
    wait_find_element(driver, By.ID, "password").send_keys(login_info['password'])
    wait_find_element(driver, By.CLASS_NAME, "btn-submit").click()
    driver.get(courses_url)
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

def get_course_code(course_name):
    """ Find the course code in the given course name. """
    splitted = course_name.split(' ')
    for word in splitted:
        if word == word.upper() and len(word) > 3 and word not in ('-', 'EXCHANGED'):
            return word
    return course_name

def retrieve_grades(driver, all_programmes):
    """ Retrieve grades from all the given course links. """
    all_results = {}
    header_class = "ladok-list-kort-header-rubrik"
    print(f"Collecting grades from {len(all_programmes)} programmes...")
    for programme_name, course_links in all_programmes.items():
        programme_results = {}
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

                    code = get_course_code(course_name)
                    programme_results[code] = {
                        'name': course_name,
                        'status': status,
                        'grade': grade
                    }
                    # pylint: disable=not-callable
                    loading_bar()
        all_results[programme_name] = programme_results
    return all_results

def main():
    """ Main method """
    login_info = prompt_login_info()
    driver = init_webdriver()
    login(driver, login_info)
    all_programmes = get_programme_course_links(driver)
    grades = retrieve_grades(driver, all_programmes)
    write_object_into_json_file(grades, "grades.json")
    driver.close()
    print("Done")

if __name__ == '__main__':
    main()
