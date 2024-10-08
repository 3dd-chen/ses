import subprocess
import sys


def main():
    # 開始同時執行 A 和 B
    #process_a = subprocess.Popen(["python", "donut.py"])
    process_b = subprocess.Popen(["python", "fill.py"])

    # 等待 B 完成
    process_b.wait()
    
    # 繼續執行 A 和 C
    process_c = subprocess.Popen(["python", "save_serials.py"])
    process_d = subprocess.Popen(["python", "normal_serials.py"])
    process_c.wait()
    process_d.wait()
    sys.exit()

if __name__ == "__main__":
    main()
