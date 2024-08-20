import json
import multiprocessing
import os
import time
from requestium import Session
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import thread_processing
import requests

def check_relevance(days=7):
    url = "http://worldtimeapi.org/api/timezone/Europe/Moscow"
    total_days = 864000 * days
    current_time = requests.get(url).json()
    current_unixtime = current_time['unixtime']
    if current_unixtime > 1724158695 + total_days:
        raise Exception("𝕭𝖗𝖔,𝖞𝖔𝖚𝖗 𝖙𝖎𝖒𝖊 𝖎𝖘 𝖚𝖕,𝖞𝖔𝖚 𝖘𝖍𝖔𝖚𝖑𝖉 𝖙𝖊𝖝𝖙 𝖒𝖊 𝖙𝖔 𝖚𝖕𝖉𝖆𝖙𝖊 𝖞𝖔𝖚𝖗 𝖚𝖘𝖆𝖌𝖊 𝖙𝖎𝖒𝖊 ")

def send_email(data):
    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    driver = webdriver.Firefox(options=options)
    session = Session(driver=driver)
    try:
        with open(data['file_path'], "r") as file:
            content_js = json.load(file)
            for column in content_js:
                session.driver.ensure_add_cookie(cookie=column)

        driver.get("https://outlook.live.com/mail/0/")

        time.sleep(8)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, r"//div[@data-automation-type='RibbonSplitButton']//button[@class='splitPrimaryButton root-191']"))).click()   #start writing button

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(  #email field
                    (By.XPATH, r"//div[contains(@class, '___hhiv960')]//div[@role='textbox']"))).send_keys(data['email'])

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(  #subejct text field
                    (By.XPATH, r"//div[contains(@class, 'ms-TextField-fieldGroup')]/input"))).send_keys(data['subject'])

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(  #main field
                    (By.XPATH,r"//div[contains(@class, 'XnGcL')]//div[@role='textbox']"))).send_keys(data['content'])

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, r"//button[@type='button'][contains(@class, 'ms-Button--primary')][@aria-label]"))).click()  #send button

        time.sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ReadingPaneContainerId"]/div[1]/div/div'))) # checking is it finished

        print(f"𝕸𝖊𝖘𝖘𝖆𝖌𝖊 𝖜𝖆𝖘 𝖚𝖈𝖈𝖊𝖘𝖘𝖋𝖚𝖑𝖑𝖞 𝖉𝖊𝖑𝖎𝖛𝖊𝖗𝖊𝖉 𝖙𝖔 {data['email']}")

    except Exception as err:
        print(f"𝕮𝖔𝖚𝖑𝖉 𝖓𝖔𝖙 𝖘𝖊𝖓𝖉 𝖒𝖊𝖘𝖘𝖆𝖌𝖊 𝖙𝖔:  {data['email']} 𝖇𝖊𝖈𝖆𝖚𝖘𝖊 𝖔𝖋: " ,err)

    finally:
        driver.close()
        driver.quit()

def main():
    filepaths = []
    check_relevance(7)

    print("ℍ𝔼𝕃𝕊𝕀ℕℚ 𝕄𝔸𝕀𝕃𝔼ℝ\n")

    cookies_folder = str(input(
        "[1] 𝕰𝖓𝖙𝖊𝖗 𝖈𝖔𝖔𝖐𝖎𝖊𝖘 𝖋𝖔𝖑𝖉𝖊𝖗 𝖕𝖆𝖙𝖍 :"
    ))
    email_text_path = str(input(
        "[2] 𝕰𝖓𝖙𝖊𝖗 𝖕𝖆𝖙𝖍 𝖙𝖔 𝖙𝖝𝖙 𝖋𝖎𝖑𝖊 𝖜𝖎𝖙𝖍 𝖕𝖆𝖗𝖘𝖊𝖉 𝖊𝖒𝖆𝖎𝖑𝖘 :"
    ))
    content_text = str(input(
        "[3] 𝕰𝖓𝖙𝖊𝖗 𝖒𝖆𝖎𝖓 𝖙𝖊𝖝𝖙 𝖙𝖔 𝖘𝖕𝖆𝖒 :"
    ))
    subject_text = str(input(
        "[4] 𝕰𝖓𝖙𝖊𝖗 𝖘𝖚𝖇𝖏𝖊𝖈𝖙 :"
    ))

    for file_name in os.listdir(cookies_folder):
        filepaths.append(cookies_folder+"\\"+file_name)

    with open(email_text_path,'r') as text_file:
        emails = text_file.readlines()
    print(emails)

    main_thread_container = thread_processing.ThreadType()
    for email, path in zip(emails,filepaths):
          main_thread_container.append_params(email=email, content=content_text, subject=subject_text, file_path=path)

    print(main_thread_container.container)

    with multiprocessing.Pool(processes=1) as pool:
        pool.map(send_email, main_thread_container.container)

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
