"""
Utility functions

David Bergh
berghdavid@hotmail.com
"""

import json
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
TIMEOUT_MAX = 5

def init_webdriver():
    """ Initialize a clean new webdriver =) """
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=options)

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

def get_data_dir_path(filename):
    """ Computes the data directory path based on current file structure. """
    script_dir = os.path.dirname(__file__)
    rel_path = "..\\data\\" + filename
    return os.path.join(script_dir, rel_path)

def write_object_into_json_file(obj, file_name):
    """ Write any python object to a file in json format. """
    file_path = get_data_dir_path(file_name)
    print(f"Writing to {file_path}")
    with open(file_path, mode="w", encoding='utf-8') as file:
        file.write(json.dumps(obj, indent=4))
        file.close()

def read_json_file_into_object(file_name):
    """ Read a json file and parse it into a python object. """
    file_path = get_data_dir_path(file_name)
    print(f"Reading from {file_path}")
    with open(file_path, mode="r", encoding='utf-8') as file:
        obj = json.loads(file.read())
        file.close()
        return obj
