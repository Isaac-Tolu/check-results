import sys, os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def main():
    load_dotenv()
    matricno = os.getenv('EPORTAL_MATRIC_NUMBER')
    password = os.getenv('EPORTAL_PASSWORD')
    session, semester, course = sys.argv[1:]

    driver = webdriver.Chrome()
    driver.get('https://eportal.oauife.edu.ng/login.php')
    login(driver, matricno, password, session, semester)
    result = get_result(driver, course)
    if result:
        print('Found')
        print(result)
    else:
        print('Not Found')

def login(
    driver:WebDriver,
    matricno:str, password:str,
    session:str, semester:str
):

    matricno_elem = driver.find_element(By.NAME, 'user_id')
    matricno_elem.clear()
    matricno_elem.send_keys(matricno)
    matricno_elem.send_keys(Keys.RETURN)

    password_elem = driver.find_element(By.NAME, 'pswd')
    password_elem.clear()
    password_elem.send_keys(password)

    session_sel = Select(driver.find_element(By.NAME, 'SessionF'))
    session_sel.select_by_visible_text(session)

    semester_sel = Select(driver.find_element(By.NAME, 'SemesterF'))
    semester_sel.select_by_visible_text(semester)

    submit_elem = driver.find_element(By.NAME, 'Submit')
    submit_elem.click()

def get_result(driver:WebDriver, course_name:str) -> 'dict|None':

    # Click on `View Semester Raw Score`
    srs_elem = driver.find_element(By.XPATH, "//div[@class='profile-menu']/ul/li[12]/a")
    srs_elem.click()

    # Get the results table element
    results_elem = driver.find_elements(By.XPATH, '//table/tbody/tr')
    # all_results = results_elem.find_elements(By.TAG_NAME, 'tr')

    for result_elem in results_elem:
        columns = result_elem.find_elements(By.TAG_NAME, 'td')

        if columns[0].text == course_name:
            result_info = {
                "Course Code": columns[0].text,
                "Course Title": columns[1].text,
                "Course Unit": columns[2].text,
                "CA Score": columns[3].text,
                "Exam Score": columns[4].text,
                "Total": columns[5].text
            }
            return result_info
        else:
            continue
    return None


if __name__ == '__main__':
    main()