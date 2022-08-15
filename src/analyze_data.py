"""
Data analyzer for grades and LTH programmes

David Bergh
berghdavid@hotmail.com
"""

from utils import read_json_file_into_object

def prompt_user_programme():
    """ Ask the user what programme is currently being studied. """
    return input("What programme are you studying? (A, BME, V, etc.): ")

def prompt_user_spec(programme_courses):
    """ Ask the user what specialization is currently being studied. """
    print("What specialization are you studying? (Press enter for none): ")
    specs = []
    for spec, value in programme_courses.items():
        if 'Specialisering' in spec:
            specs.append({
                'name': spec,
                'courses': value
            })
    for index, spec in enumerate(specs):
        print(str(index + 1) + '. ' + str(spec['name']))
    while True:
        inp = input()
        try:
            if inp == "":
                return None
            inp_nbr = int(inp) - 1
            if 1 <= inp_nbr <= len(specs):
                spec = specs[inp_nbr]
                print(f"Chosen specialization: {spec['name']}")
                return spec
            print("Could not read that number, try again")
        except ValueError:
            print("Could not read that number, try again")

def parse_data(programme):
    """ Parse the json data stored in the 'data' folder and return them as python objects. """
    programme_file_name = programme + '-programme.json'
    grades_file_name = 'grades.json'
    try:
        programme_json = read_json_file_into_object(programme_file_name)
    except FileNotFoundError:
        programme_json = None
    try:
        grades_json = read_json_file_into_object(grades_file_name)
    except FileNotFoundError:
        grades_json = None
    return (programme_json, grades_json)

def print_compulsories_left(programme_courses, completed_courses):
    """ Print the compulsory courses which are not yet completed. """
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
    print("These compulsory courses from years 1-3 are left:")
    for course in compulsories_left:
        print(course['name'])

def merge_grades(grades):
    """ Merge all the taken courses into one dictionary. """
    courses = {}
    for semester in grades.values():
        courses = courses | semester
    return courses

def merge_programme_with_completed_courses(completed_courses, programme):
    """
    Merge the taken courses with the courses from the programme. This is used to determine the hp
    from the taken courses. """
    print(programme)
    #for semester in completed_courses:
    #    print(semester)
    return None

def analyze_grades(programme_courses, grades, spec):
    """ Analyze and print current education status. """
    ### Programme requirements ###
    # 300 hp
    # 180 hp from the first 3 years
    # 75 hp from advanced level (includes masters thesis)
    # 45 hp from one spec. 30 hp from A-level courses within that spec
    # 45 hp from within program
    # 15 hp from wherever
    completed_courses = merge_grades(grades)
    print_compulsories_left(programme_courses, completed_courses)
    merge_programme_with_completed_courses(completed_courses, programme_courses)
    #specs_left = get_specs_left(programme_courses, completed_courses)
    # TODO: Scan specialization completion

def main():
    """ Main method """
    programme = prompt_user_programme()
    (programme_courses, my_grades) = parse_data(programme)
    if not programme_courses:
        print(f"Could not find {programme}-programme data...")
        print("Hint: Try running the programme scraper first")
        return
    if not my_grades:
        print("Could not find grades data...")
        print("Hint: Try running the Ladok scraper first")
        return
    spec = prompt_user_spec(programme_courses)
    analyze_grades(programme_courses, my_grades, spec)
    print("Done")

if __name__ == '__main__':
    main()
