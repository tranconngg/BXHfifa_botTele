# fifa_crawler.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import csv
from datetime import datetime

class FIFADataCrawler:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    def get_filename(self):
        today = datetime.now().strftime('%m%d%Y')
        filename = f'fifa_{today}.csv'
        return filename

    def crawl_data(self):
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service)

        driver.get('https://kqbd.mobi/bang-xep-hang-fifa')

        try:
            table = driver.find_element(By.XPATH, "/html/body/div/div/div[5]/div/div[3]/table")
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]

            data = []

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 4:
                    xh_kv = columns[0].text
                    dt_qg = columns[1].text
                    xh_fifa = columns[2].text
                    diem_hien_tai = columns[3].text

                    data.append([xh_kv, dt_qg, xh_fifa, diem_hien_tai])

            filename = self.get_filename()
            filepath = os.path.join('data', filename)

            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['XH KV', 'ĐTQG', 'XH FIFA', 'Điểm hiện tại'])
                writer.writerows(data)

            print(f"Dữ liệu đã được lưu vào {filename}")

        except Exception as e:
            print(f"Lỗi rồi: {e}")

        finally:
            driver.close()
