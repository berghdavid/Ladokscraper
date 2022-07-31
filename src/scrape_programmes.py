"""
Web scraper for LTH programme courses

David Bergh
berghdavid@hotmail.com
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils import init_webdriver, wait_find_elements, write_object_into_json_file

def prompt_programme_info():
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


def is_level(word):
    """ Determine whether the element containes a valid course level or not. """
    return word in ('A', 'G1', 'G2')

def get_course_codes(table):
    """ Retrieve all the course codes from a given table of courses. """
    course_code_elements = table.find_elements(By.CLASS_NAME, 'app-course-code-col')
    return [course_code.find_element(By.TAG_NAME, 'a').text
            for course_code in course_code_elements]

def get_course_levels(table):
    """ Retrieve the levels for all the different courses from a given table of courses. """
    span_data = table.find_elements(By.TAG_NAME, 'span')
    span_str = [element.text for element in span_data]
    return list(filter(is_level, span_str))

def get_programme_courses(driver, programme):
    """ Retrieve what courses are included in the given programme. """
    url = 'https://kurser.lth.se/lot/programme?ay=22_23&programme=' + programme
    driver.get(url)
    all_courses = {}
    all_table_names = wait_find_elements(driver, By.TAG_NAME, "h2")

    all_tables = wait_find_elements(driver, By.TAG_NAME, "tbody")
    for index, table in enumerate(all_tables):
        yearly_courses = []
        course_codes = get_course_codes(table)
        course_levels = get_course_levels(table)
        for course_index, course_code in enumerate(course_codes):
            course = {}
            course['name'] = course_code
            course['level'] = course_levels[course_index]
            yearly_courses.append(course)
        all_courses[all_table_names[index].text] = yearly_courses
    print(all_courses)
    return all_courses

def main():
    """ Main method """
    programme = prompt_programme_info()
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
