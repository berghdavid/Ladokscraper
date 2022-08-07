"""
Main program for Ladok webscraper

David Bergh
berghdavid@hotmail.com
"""

import analyze_data
import scrape_grades
import scrape_programmes

def prompt_action():
    """ Prompt the user for which program to run. """
    while True:
        print("What do you want to do (1-5)")
        print("1. Retrieve your Ladok grades")
        print("2. Retrieve education programme requirements")
        print("3. Analyze your coursework based on your taken courses and programme")
        print("4. Do everything")
        print("5. Exit")
        inp = input()
        if inp == '1':
            scrape_grades.main()
        elif inp == '2':
            scrape_programmes.main()
        elif inp == '3':
            analyze_data.main()
        elif inp == '4':
            scrape_grades.main()
            scrape_programmes.main()
            analyze_data.main()
        elif inp == '5':
            return
        else:
            print("Could not understand that command. Type any number between 1 and 5")

def main():
    """ Main method """
    prompt_action()
    print("Exiting...")

if __name__ == '__main__':
    main()
