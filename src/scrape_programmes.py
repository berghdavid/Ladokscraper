"""
Web scraper for LTH programme courses

David Bergh
berghdavid@hotmail.com
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils import init_webdriver, wait_find_elements, write_object_into_json_file

def get_programme_info():
    """ Ask the user for what programme at LTH to lookup. """
    return input("What programme are you studying? (A, BME, V, etc.): ")

def verify_site_existance(driver, programme):
    """ Verify that the given programme has an existing course plan. """
    url = 'https://kurser.lth.se/lot/programme?ay=22_23&programme=' + programme
    driver.get(url)
    try:
        nothing_to_show = driver.find_element(By.CLASS_NAME, 'p-3 text-center').text
        if not nothing_to_show or nothing_to_show == 'Inget att visa':
            return False
        return True
    except NoSuchElementException:
        return True

def get_programme_courses(driver, programme):
    """ Retrieve what courses are included in the given programme. """
    url = 'https://kurser.lth.se/lot/programme?ay=22_23&programme=' + programme
    driver.get(url)
    all_courses = []
    all_table_names = wait_find_elements(driver, By.TAG_NAME, "h2")
    all_tables = wait_find_elements(driver, By.TAG_NAME, "tbody")

    for index, table in enumerate(all_tables):
        courses = []
        all_cells = table.find_elements(By.CLASS_NAME, 'app-course-code-col')
        for cell in all_cells:
            course_name = cell.find_element(By.TAG_NAME, 'a').text
            courses.append(course_name)
        all_courses.append({all_table_names[index].text: courses})
    print(all_courses)
    return all_courses

def main():
    """ Main method """
    programme = get_programme_info()
    driver = init_webdriver()
    courses = get_programme_courses(driver, programme)
    if not courses:
        print("Could not find that programme...")
    else:
        write_object_into_json_file(courses, programme + '-programme.json')
    driver.close()
    print("Done")

if __name__ == '__main__':
    main()
