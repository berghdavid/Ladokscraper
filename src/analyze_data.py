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

def get_compulsories_left(programme_courses, completed_courses):
    """ Get the compulsory courses which are not yet completed. """
    header_compulsories = [
        'Årskurs 1 - Obligatoriska kurser',
        'Årskurs 2 - Obligatoriska kurser',
        'Årskurs 3 - Obligatoriska kurser',
    ]
    compulsory_courses = []
    for header in header_compulsories:
        compulsory_courses += programme_courses[header]
    compulsories_left = []
    for compulsory in compulsory_courses:
        code = compulsory['name']
        if code not in completed_courses:
            compulsories_left.append(compulsory)
        elif completed_courses[code]['status'] not in ('Completed', 'credited') or \
             completed_courses[code]['grade'] not in ('3', '4', '5', 'G', 'credited'):
            compulsories_left.append(compulsory)
    return compulsories_left

def merge_programme_grades(grades):
    """ Merges all the taken courses into one dictionary. """
    courses = {}
    for programme in grades.values():
        courses = courses | programme
    return courses

def analyze_grades(programme_courses, grades):
    """ Analyze and print current education status. """
    ### Programme requirements ###
    # 300 hp
    # 180 hp from the first 3 years
    # 75 hp from advanced level (includes masters thesis)
    # 45 hp from one spec. 30 hp from A-level courses within that spec
    # 45 hp from within program
    # 15 hp from wherever
    completed_courses = merge_programme_grades(grades)
    compulsories_left = get_compulsories_left(programme_courses, completed_courses)
    print(compulsories_left)

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
    analyze_grades(programme_courses, my_grades)
    print("Done")

if __name__ == '__main__':
    main()
