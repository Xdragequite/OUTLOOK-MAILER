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

        print(f"Message was successfully delivered to {data['email']}")

    except Exception as _:
        print(f"Could not send message to :  {data['email']}")

    finally:
        driver.close()
        driver.quit()

def main():
    filepaths = []

    print("""
░█─░█ ░█▀▀▀ ░█─── ░█▀▀▀█ ▀█▀ ░█▄─░█ ░█▀▀█ 　 ░█▀▄▀█ ─█▀▀█ ▀█▀ ░█─── ░█▀▀▀ ░█▀▀█ 
░█▀▀█ ░█▀▀▀ ░█─── ─▀▀▀▄▄ ░█─ ░█░█░█ ░█─░█ 　 ░█░█░█ ░█▄▄█ ░█─ ░█─── ░█▀▀▀ ░█▄▄▀ 
░█─░█ ░█▄▄▄ ░█▄▄█ ░█▄▄▄█ ▄█▄ ░█──▀█ ─▀▀█▄ 　 ░█──░█ ░█─░█ ▄█▄ ░█▄▄█ ░█▄▄▄ ░█─░█
        """)

    cookies_folder = str(input(
        "[1] Enter cookies folder path :"
    ))
    email_text_path = str(input(
        "[2] Enter path to parsed emails :"
    ))
    content_text = str(input(
        "[3] Enter your main text to spam :"
    ))
    subject_text = str(input(
        "[4] Enter subject :"
    ))

    for file_name in os.listdir(cookies_folder):
        filepaths.append(cookies_folder+"\\"+file_name)

    with open(email_text_path,'r') as text_file:
        emails = text_file.readlines()


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
