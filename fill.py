from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
import time
import random
import datetime

i = 0
edge_options = Options()
edge_options.add_argument("--inprivate")

#edge_options.add_argument("--headless")  # 加入這一行以設置headless模式

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("flag.txt", "r") as f:
    content = f.read()

# 將內容改寫為 "1"
content = "1"

# 將改寫後的內容寫回到 flag.txt
with open("flag.txt", "w") as f:
    f.write(content)

# 將現實時間戳記儲存成檔案
with open("timestamp.txt", "w") as timestamp_file:
    timestamp_file.write(f"{timestamp}\n")

try:
    with open("set.txt", "r") as f:
        current_set = int(f.read())
except FileNotFoundError:
    current_set = 0

# 使用 Edge 瀏覽器
for _ in range(current_set):

    # read an int from a file
    with open("count.txt", "r") as file:
        count = int(file.read())

    driver = webdriver.Edge(options=edge_options)


    # 前往網頁
    driver.get("https://samsung-education-promotion.twsamsungcampaign.com/")
    #driver.minimize_window()  # 將瀏覽器最小化到工具列
    time.sleep(5)

    # 生成加入的數字
    num = random.randint(1, 2)

    # 遍歷每個數字，填寫相應的電子郵件地址
    email = "b10902033+" + str(count) + "@gapps.ntust.edu.tw"
    email_field = driver.find_element("id", "txtEmail")
    email_field.send_keys(email)
    count += 1
    with open("count.txt", "w") as file:
        file.write(str(count))

    #time.sleep(num)

    # 使用 JavaScript 勾選 input 元素
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckPhone'))
    #time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckMonitor'))
    #time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckTablet'))
    #time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckWatch'))
    #time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckEarPhone'))
    #time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckStorage'))
    #time.sleep(random.randint(1, 2))
    
    # 隨機生成手機號碼
    phone_number = "09" + "".join(random.choices("0123456789", k=8))
    #time.sleep(random.randint(1, 2))

    # 找到手機號碼的輸入欄位並填寫值
    phone_input = driver.find_element("id","txtCellPhone")
    phone_input.send_keys(phone_number)
    #time.sleep(random.randint(1, 2))

    #time.sleep(random.randint(1, 3))

    complete_link = driver.find_element("id", "lnkbtnSubmit")
    complete_link.click()

    # 等待 10 秒鐘
    #time.sleep(5)

    # 找到填寫完成連結元素
    complete_link = driver.find_element(By.CSS_SELECTOR, "a.lbbtn.mybtn")

    # 使用 ActionChains 模擬滑鼠移動到連結元素並點擊
    #actions = ActionChains(driver)
    #actions.move_to_element(complete_link).click().perform()

    time.sleep(1)

    # 關閉瀏覽器
    driver.quit()

'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
import time
import random
import datetime  # Import the datetime module for timestamp

i = 0
edge_options = Options()
edge_options.add_argument("--inprivate")
#edge_options.add_argument("--headless")  # 加入這一行以設置headless模式



def generate_chinese_name():
    # 隨機選擇姓氏
    surnames = ["趙", "錢", "孫", "李", "周", "吳", "鄭", "王", "馮", "陳", "褚", "衛", "蔣", "沈", "韓", "楊", "朱", "秦", "尤", "許", "何", "呂", "施", "張", "孔", "曹", "嚴", "華", "金", "魏", "陶", "姜", "戚", "謝", "鄒", "喻", "柏", "水", "竇", "章", "雲", "蘇", "潘", "葛", "奚", "范", "彭", "郎", "魯", "韋", "昌", "馬", "苗", "鳳", "花", "方", "俞", "任", "袁", "柳", "酆", "鮑", "史", "唐", "費", "廉", "岑", "薛", "雷", "賀", "倪", "湯", "滕", "殷", "羅", "畢", "郝", "鄔", "安", "常", "樂", "於", "時", "傅", "皮", "卞", "齊", "康", "伍", "余", "元", "卜", "顧", "孟", "平", "黃", "和", "穆", "蕭", "尹"]
    surname = random.choice(surnames)
    
    # 隨機生成名字字數（2到3個字）
    name_length = random.randint(1, 2)
    
    # 隨機生成名字
    characters = ["亞", "倫", "彥", "仁", "軒", "宇", "婕", "心", "琪", "雅", "晨", "雨", "蓉", "明", "翰", "琪", "偉", "宏", "美", "玲", "宗", "君", "怡", "建", "宇", "佩", "珊", "志", "文", "靜", "廷"]
    given_name = "".join(random.choices(characters, k=name_length))
    
    # 組合成完整的名字
    full_name = surname + given_name
    return full_name


# 產生現實時間戳記
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("flag.txt", "r") as f:
    content = f.read()

    # 將內容改寫為 "1"
content = "1"

    # 將改寫後的內容寫回到 flag.txt
with open("flag.txt", "w") as f:
    f.write(content)



# 將現實時間戳記儲存成檔案
with open("timestamp.txt", "w") as timestamp_file:
    timestamp_file.write(f"{timestamp}\n")

try:
    with open("set.txt", "r") as f:
        current_set = int(f.read())
except FileNotFoundError:
    current_set = 0

# 使用 Edge 瀏覽器

for _ in range(current_set):
    
    #read an int from a file
    with open("count.txt", "r") as file:
        count = int(file.read())
        
    
    driver = webdriver.Edge(options=edge_options)

    # 前往網頁
    driver.get("https://samsung-education-promotion.twsamsungcampaign.com/")
    driver.minimize_window()  # 將瀏覽器最小化到工具列
    time.sleep(5)
    # 生成加入的數字
    #numbers = [str(x) for x in range(39, 101)]
    # 隨機選擇數字1~10
    num = random.randint(1, 2)
    
    # 遍歷每個數字，填寫相應的電子郵件地址
    email = "b10902033+" + str(count) + "@gapps.ntust.edu.tw"
    email_field = driver.find_element("id","txtEmail")
    email_field.send_keys(email)
    count += 1
    with open("count.txt", "w") as file:
        file.write(str(count))
    
    time.sleep(num)
    

    # 使用 JavaScript 勾選 input 元素
    #driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'rbSES'))
    #time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckPhone'))
    time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckMonitor'))
    time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckTablet'))
    time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckWatch'))
    time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckEarPhone'))
    time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'ckStorage'))
    time.sleep(random.randint(1, 2))

    #name_field = driver.find_element('id', 'txtName')
    #name_field.send_keys(generate_chinese_name())
    #time.sleep(random.randint(1, 3))

    # 隨機選擇性別
    sex_options = ["rbSexM", "rbSexW"]
    selected_sex = random.choice(sex_options)
    driver.execute_script("arguments[0].checked = true;", driver.find_element('id', selected_sex))
    time.sleep(random.randint(1, 2))
   
    

    # 隨機生成手機號碼
    phone_number = "09" + "".join(random.choices("0123456789", k=8))
    time.sleep(random.randint(1, 2))

    # 找到手機號碼的輸入欄位並填寫值
    phone_input = driver.find_element("id","txtCellPhone")
    phone_input.send_keys(phone_number)
    time.sleep(random.randint(1, 2))

    #driver.execute_script("arguments[0].checked = true;", driver.find_element('id', 'rbStatusS'))
    #time.sleep(5)

    complete_link = driver.find_element("id","lnkbtnSubmit")
    complete_link.click()

            # 等待 10 秒鐘
    time.sleep(5)

            # 找到填寫完成連結元素
    complete_link = driver.find_element(By.CSS_SELECTOR, "a.lbbtn.mybtn")

            # 使用 ActionChains 模擬滑鼠移動到連結元素並點擊
    actions = ActionChains(driver)
    actions.move_to_element(complete_link).click().perform()

    time.sleep(5)
            
            # 關閉瀏覽器
    driver.quit()
'''
