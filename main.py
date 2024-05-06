import random
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from datetime import datetime
import json
import sys

############################--CONSTANTS--############################

#Put your own credentials
EMAIL_USER = "example@gmail.com"
EMAIL_PSW = "Password123"

#Delay in seconds recomended || delay > 40
DELAY = 5

#Directory to save json files
DIR = "your/directory"

#####################################################################


def login(driver):
    driver.get("https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser&ec=asw-gmail-globalnav-signin&ddm=0")

    #Send the mail part
    email_gap = driver.find_element(By.ID, "identifierId")
    email_gap.send_keys(EMAIL_USER)
    time.sleep(0.5)
    email_gap.send_keys(Keys.RETURN)

    time.sleep(8)

    #send password part
    driver.save_screenshot('screenshot.png')
    psw_gap = driver.find_element(By.NAME, "Passwd")
    psw_gap.send_keys(EMAIL_PSW)
    time.sleep(0.5)
    psw_gap.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Login successful\n")


def check_loop(driver):

    #First sample of email for compare with the check one
    prev_email = driver.find_element(By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div[1]/div/table/tbody/tr[1]").accessible_name
    prev_email = prev_email.split(", ")

    #Main loop refreshing every DELAY seconds
    while True:

        check = driver.find_element(By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div[1]/div/table/tbody/tr[1]").accessible_name.split(", ")

        #Compare name, subject and hour between the prev_email and check mail
        if check[0] != prev_email[0] or check[1] != prev_email[1] or check[2] != prev_email[2]:
            try:
                print(f"new email detected from {check[1]}")

                full_content = driver.find_element(By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div[1]/div/table/tbody/tr[1]")

                #Use of actionchains for press combination of keys
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).click(full_content).key_up(Keys.CONTROL).perform()
                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

                windows = driver.window_handles

                driver.switch_to.window(windows[-1])

                #Extract all the info in the mail
                time.sleep(2.5)
                full_content = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]").text
                subject = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/h2").accessible_name
                hour = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/span[2]").accessible_name
                hour = hour[:5]
                name = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[1]/table/tbody/tr/td/h3/span/span[1]/span").text
                email_address = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[1]/table/tbody/tr/td/h3/span/span[3]").text
                email_address = email_address[1:-1]

                #Determine the file name with date, hour, name, and a random number to minimize the probability of having the same name twice
                file_name = str(datetime.now().date()) + "_" + hour[:2] + "_" + hour[3:] + "_" + name + str(random.randint(0, 99)) + ".json"
                data = [{
                    "Subject": subject,
                    "Content": full_content,
                    "Email": email_address,
                    "Name": name,
                    "Hour": hour
                }]

                json_dump(data, file_name)

                driver.close()
                time.sleep(0.5)
                driver.switch_to.window(windows[-2])
                prev_email = check[1:]
                time.sleep(3)
            except:
                print("ERROR")

        time.sleep(DELAY)

def json_dump(data, file_name):

    file_dir = DIR + file_name

    with open(file_dir, "w") as file:
        json.dump(data, file)

    print(f"\nJSON file exported successfully as {file_name}")



if __name__ == "__main__":
    # Must be Chrome for bypass antibot
    driver = uc.Chrome()

    login(driver)
    check_loop(driver)

