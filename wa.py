import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from urllib.request import urlopen
import json

#load browser=======================================
#jika blm login, login dulu dengan scan qrcode
osname = os.getlogin()
chrome_options = Options()
#windows
chrome_options.add_argument("user-data-dir=C:\\Users\\"+osname+"\\AppData\\Local\\Google\\Chrome\\User Data")
#linux
#chrome_options.add_argument("user-data-dir=/tmp/tarun")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://web.whatsapp.com')
input("Press ENTER after login into Whatsapp Web and your chats are visiable.")
#end load browser======================================

sudah = []
def kirim_wa():
    #load json========================================
    # url = "https://webme1.brokerxplorer.com/wajson"
    # response = urlopen(url) 
    # data_json = json.loads(response.read())
    #tambah json https://webme.brokerxplorer.com/wame/?nomor=081515460563&pesan=kode%20verifikasi%20Anda%2053453
    with open('isimsg.json', 'r') as file:
        data_json = json.load(file)
    #end load json===================================
    print(data_json)
    count = 0
    if data_json:
        #loop json================================
        for item in data_json:
            nomor = item.get('nomor')
            kode = item.get('kode')
            image_path = ""
            if(item.get('img')):
                image_path = item.get('img')
            #print(f'Nomor: {nomor}, Kode: {kode}')
            if len(nomor) > 5:
                #sudah.append(nomor)
                try:
                    url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(nomor, kode)
                    sent = False
                    driver.get(url)
                    try:
                        click_btn = WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="send"]')))
                    except Exception as e:
                        print("Sorry message could not sent to " + str(nomor))
                    else:
                        
                        sleep(5)
                        if(image_path):
                            attach_btn = driver.find_element(By.CLASS_NAME, 'x1h4ghdb')
                            attach_btn.click()
                            sleep(3)
                            # Find and send image path to input
                            msg_input = driver.find_elements(By.CSS_SELECTOR, '.x1gja9t input')[1]
                            
                            msg_input.send_keys(image_path)
                            sleep(3)
                            # Start the action chain to write the message
                            actions = ActionChains(driver)
                            actions.send_keys(Keys.ENTER)
                            actions.perform()
                            sleep(3)
                            os.remove(image_path)
                        else:
                            click_btn.click()
                        sent = True
                        sleep(10)
                        print('Message sent to: ' + str(nomor))
                        data_json.remove(item)
                    count = count + 1
                except Exception as e:
                    print('Failed to send message to ' + str(nomor) + str(e))
            else:
                data_json.remove(item)
        with open('isimsg.json', 'w') as file:
            json.dump(data_json, file, indent=2)
    #driver.quit()

if __name__ == '__main__':
    while True:
        kirim_wa()
        time.sleep(5)
