"""
Data analyzer for grades and LTH programmes

David Bergh
berghdavid@hotmail.com
"""

from utils import read_json_file_into_object

def prompt_user_programme():
    """ Ask the user what programme is currently being studied. """
    return input("What programme are you studying? (A, BME, V, etc.): ")

def parse_data(programme):
    """ Parse the json data stored in the 'data' folder and return them as python objects. """
    programme_file_name = programme + '-programme.json'
    grades_file_name = 'grades.json'
    programme_json = read_json_file_into_object(programme_file_name)
    grades_json = read_json_file_into_object(grades_file_name)
    return (programme_json, grades_json)

def main():
    """ Main method """
    programme = prompt_user_programme()
    (programme_courses, my_grades) = parse_data(programme)
    if not programme_courses:
        print(f"Could not find {programme}-programme data...")
        print("Hint: Try running 'python src/scrape_programmes.py'")
        return
    if not my_grades:
        print("Could not find grades data...")
        print("Hint: Try running 'python src/scrape_grades.py'")
        return
    # TODO: Analyze data objects
    print("Done")

if __name__ == '__main__':
    main()
