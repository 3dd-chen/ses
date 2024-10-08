import os
from PIL import Image
import pyfiglet
import time


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_timestamp():
    while True:
        new_timestamp = input("扭轉時間 (格式: 2023-08-30 14:23:24)")
        print("\n")
        if new_timestamp == "-1":
            return "0"
        if len(new_timestamp) != 19 or new_timestamp[4] != '-' or new_timestamp[7] != '-' or new_timestamp[10] != ' ' or new_timestamp[13] != ':' or new_timestamp[16] != ':':
            print("北七有格式不看")
            print("\n")
        else:
            break

    with open("timestamp.txt", "w") as f:
        f.write(new_timestamp)
    print("好了")
    print("\n")
    return input("按 1 返回，0 回主選單: ")

def update_set():
    new_set = input("你今天要做幾組?")
    print("\n")
    if new_set == "-1":
        return "0"
    with open("set.txt", "w") as f:
        f.write(new_set)
    print("好了")
    print("\n")
    return input("按 1 返回，0 回主選單: ")

def go_to_world_gym():
    image_path = "world_gym.png"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        #image = image.resize((32, 32))  # 將圖像壓縮到 64x64 尺寸
        ascii_img = convert_image_to_ascii(image)
        print(ascii_img)
    else:
        print("找不到檔案啦")
        print("\n")
    return input("按 1 返回，0 回主選單: ")

def display_ascii_art(text):
    figlet = pyfiglet.Figlet(font='slant')
    ascii_text = figlet.renderText(text)
    print(ascii_text)

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    return image.convert("L")

def map_pixels_to_ascii(image, ascii_chars, range_width=25):
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        # 映射像素值到 ASCII 字符的索引，使其不超出列表範圍
        ascii_index = int(pixel_value * (len(ascii_chars) - 1) / 255)
        ascii_str += ascii_chars[ascii_index]
    return ascii_str


def convert_image_to_ascii(image):
    # 這裡需要定義 ASCII_CHARS 變數
    ASCII_CHARS = ["@", "#", "8", "&", "o", ":", "*", ".", " "]
    
    image = resize_image(image)
    image = grayscale_image(image)
    ascii_str = map_pixels_to_ascii(image, ASCII_CHARS)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    return ascii_img

def main():
    while True:
        clear_screen()
        print("======================================================")
        display_ascii_art("World Gym Coach He")
        print("======================================================")
        print("今日菜單:")
        print("\n")
        print("1.你今天要做幾組")
        print("\n")
        print("2.跟我去World Gym")
        print("\n")
        print("3.開始工作")
        print("\n")
        
        choice = input("你想怎樣? ")
        print("======================================================")
        if choice == "99":
            while True:
                back = update_timestamp()
                print("======================================================")
                if back == "0":
                    break
        elif choice == "1":
            while True:
                back = update_set()
                print("======================================================")
                if back == "0":
                    break
        elif choice == "2":
            while True:
                back = go_to_world_gym()
                print("======================================================")
                if back == "0":
                    break
        elif choice == "3":
            print("請耐心等我工作完")
            print("\n")
            time.sleep(3)
            break
        else:
            print("選這三小數字")

if __name__ == "__main__":
    main()
