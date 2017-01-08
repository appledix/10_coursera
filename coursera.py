import argparse
import json
import operator
import os
import random
import re

from bs4 import BeautifulSoup
import lxml
import openpyxl
import requests


NUMBER_OF_COURSES = 20

def get_output_location_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx_output_location", help="<directory>/<filename>", type=str)
    location = parser.parse_args().xlsx_output_location
    return (location if location.endswith('.xlsx') else '{}.xlsx'.format(location))

def is_file_location_valid(file_location):
    directory = os.path.dirname(file_location)
    return os.path.basename(file_location) \
    and (not os.path.exists(file_location)) \
    and (not operator.xor(bool(directory), os.path.isdir(directory)))

def get_courses_list(coursera_feed_xml_url):
    xml_feed = requests.get(coursera_feed_xml_url).content
    document = lxml.etree.fromstring(xml_feed)
    return [node[0].text for node in document]

def get_random_courses(courses_list, number_of_courses):
    total_number_of_courses = len(courses_list)
    random_numbers = random.sample(range(total_number_of_courses), number_of_courses)
    return [courses_list[number] for number in random_numbers]

def get_raw_html(url):
    request = requests.get(url)
    request.encoding = 'utf8'
    return request.text

def get_course_name(soup): 
    return soup.find("div", class_="course-title").text

def get_course_language(soup):
    table = soup.find("table", class_="basic-info-table")
    for row in table.find_all("tr"):
        cols = row.find_all("td")        
        row_title = cols[0].text
        row_data = cols[1].text
        if row_title == 'Language':
            return row_data
    return 'Missing'

def get_course_start_date(soup):
    json_string = soup.find("script", type="application/ld+json")
    if json_string:   
        json_data = json.loads(json_string.text)
        course_info = json_data["hasCourseInstance"][0]
        if "startDate" in course_info:
            return course_info["startDate"]
    return 'Missing'

def get_course_duration(soup):
    weeks_syllabus = soup.find("div", class_="rc-WeekView")
    if weeks_syllabus:
        return len(weeks_syllabus.find_all("div", class_="week"))
    else:
        return 'Missing'

def get_course_rating(soup):
    rating_info = soup.find("div", class_="ratings-text")
    if rating_info:
        return get_rating_from_text(rating_info.text)
    else:
        return 'Missing'

def get_rating_from_text(text):
    return re.search(r'\d\.?\d?', text).group(0)

def get_course_data(course_url):
    course_page = get_raw_html(course_url)
    soup = BeautifulSoup(course_page, "html.parser")
    return {"name": get_course_name(soup),
            "URL": course_url,
            "language": get_course_language(soup),
            "start_date": get_course_start_date(soup),
            "number_of_weeks": get_course_duration(soup),
            "average_rating": get_course_rating(soup)}

def create_xlsx_book(courses_data):
    book = openpyxl.Workbook()
    sheet = book.active
    sheet.append(['Name',
        'URL',
        'Language',
        'Start date',
        'Number of weeks',
        'Average rating'])
    for course in courses_data:
        sheet.append([course['name'],
            course['URL'],
            course['language'],
            course['start_date'],
            course['number_of_weeks'],
            course['average_rating']])
    return book

def output_xlsx_book_to_file(xlsx_book, file_location):
    xlsx_book.save(file_location)


def main():
    file_location = get_output_location_from_terminal()
    if is_file_location_valid(file_location):
        courses_list = get_courses_list("https://www.coursera.org/sitemap~www~courses.xml")
        random_courses = get_random_courses(courses_list, NUMBER_OF_COURSES)
        courses_data = [get_course_data(course_url) for course_url in random_courses]    
        xlsx_book = create_xlsx_book(courses_data)
        output_xlsx_book_to_file(xlsx_book, file_location)
    else:
        print('Incorrect xlsx output location.')
        return

if __name__ == '__main__':
    main()


