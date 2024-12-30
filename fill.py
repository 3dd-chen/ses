import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import hashlib
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def run_instance():
    with sync_playwright() as playwright:
        run(playwright)

def get_md5_from_timestamp() -> str:
    timestamp = f"{time.time()}{random.random()}"
    return generate_md5(timestamp)

def generate_md5(input_string: str) -> str:
    # Convert string to bytes using UTF-8 encoding
    input_bytes = input_string.encode('utf-8')
    # Create MD5 hash object
    md5_hash = hashlib.md5(input_bytes)
    # Return hexadecimal representation
    return md5_hash.hexdigest()[:5]

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://samsung-education-promotion.twsamsungcampaign.com")
    page.locator(".checkstyle").first.click()
    page.locator("div:nth-child(2) > .mycheckbox > .checkstyle").click()
    page.locator("div:nth-child(3) > .mycheckbox > .checkstyle").first.click()
    page.locator("div:nth-child(4) > .mycheckbox > .checkstyle").click()
    page.locator("div:nth-child(5) > .mycheckbox > .checkstyle").click()
    page.locator("div:nth-child(6) > .mycheckbox > .checkstyle").click()
    page.locator("#txtEmail").click()
    page.locator("#txtEmail").fill(f"b10902033+{get_md5_from_timestamp()}@gapps.ntust.edu.tw")
    page.locator("#txtCellPhone").click()
    page.locator("#txtCellPhone").fill(f"09" + "".join(random.choices("0123456789", k=8)))
    page.goto("https://samsung-education-promotion.twsamsungcampaign.com/#kv")
    #page.get_by_role("link", name="填寫完成 >").click()

    #time.sleep(50000)
    # ---------------------
    context.close()
    browser.close()

try:
    with open("set.txt", "r") as f:
        num_runs = int(f.read().strip())
except FileNotFoundError:
    num_runs = 1  # Default to 1 run if file not found

# Main execution
if __name__ == '__main__':
    # Use number of CPU cores or limit to reasonable number
    max_workers = min(multiprocessing.cpu_count(), 4)
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all runs to process pool
        futures = [executor.submit(run_instance) for _ in range(num_runs)]
        
        # Wait for completion
        for i, future in enumerate(futures, 1):
            future.result()
            print(f"Completed run {i}/{num_runs}")
        #time.sleep(2)  # Add delay between runs

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.edge.options import Options
# from playwright.sync_api import sync_playwright
# import time
# import random
# import datetime

# i = 0
# edge_options = Options()
# edge_options.add_argument("--inprivate")

# #edge_options.add_argument("--headless")  # 加入這一行以設置headless模式

# timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# with open("flag.txt", "r") as f:
#     content = f.read()

# # 將內容改寫為 "1"
# content = "1"

# # 將改寫後的內容寫回到 flag.txt
# with open("flag.txt", "w") as f:
#     f.write(content)

# # 將現實時間戳記儲存成檔案
# with open("timestamp.txt", "w") as timestamp_file:
#     timestamp_file.write(f"{timestamp}\n")

# try:
#     with open("set.txt", "r") as f:
#         current_set = int(f.read())
# except FileNotFoundError:
#     current_set = 0

# # 使用 Edge 瀏覽器
# for _ in range(current_set):

#     # read an int from a file
#     with open("count.txt", "r") as file:
#         count = int(file.read())

#     driver = webdriver.Edge(options=edge_options)


#     # 前往網頁
#     driver.get("https://samsung-education-promotion.twsamsungcampaign.com/")
#     #driver.minimize_window()  # 將瀏覽器最小化到工具列
#     time.sleep(5)

#     # 生成加入的數字
#     num = random.randint(1, 2)

#     # 遍歷每個數字，填寫相應的電子郵件地址
#     email = "b10902033+" + str(count) + "@gapps.ntust.edu.tw"
#     email_field = driver.find_element("id", "txtEmail")
#     email_field.send_keys(email)
#     count += 1
#     with open("count.txt", "w") as file:
#         file.write(str(count))

#     #time.sleep(num)

#     # 使用 JavaScript 勾選 input 元素
#     driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckPhone'))
#     #time.sleep(random.randint(1, 2))
#     driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckMonitor'))
#     #time.sleep(random.randint(1, 2))
#     driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckTablet'))
#     #time.sleep(random.randint(1, 2))
#     driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckWatch'))
#     #time.sleep(random.randint(1, 2))
#     driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckEarPhone'))
#     #time.sleep(random.randint(1, 2))
#     driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckStorage'))
#     #time.sleep(random.randint(1, 2))
    
#     # 隨機生成手機號碼
#     phone_number = "09" + "".join(random.choices("0123456789", k=8))
#     #time.sleep(random.randint(1, 2))

#     # 找到手機號碼的輸入欄位並填寫值
#     phone_input = driver.find_element("id","txtCellPhone")
#     phone_input.send_keys(phone_number)
#     #time.sleep(random.randint(1, 2))

#     #time.sleep(random.randint(1, 3))

#     complete_link = driver.find_element("id", "lnkbtnSubmit")
#     complete_link.click()

#     # 等待 10 秒鐘
#     #time.sleep(5)

#     # 找到填寫完成連結元素
#     complete_link = driver.find_element(By.CSS_SELECTOR, "a.lbbtn.mybtn")

#     # 使用 ActionChains 模擬滑鼠移動到連結元素並點擊
#     #actions = ActionChains(driver)
#     #actions.move_to_element(complete_link).click().perform()

#     time.sleep(1)

#     # 關閉瀏覽器
#     driver.quit()