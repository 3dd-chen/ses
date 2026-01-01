# SES - Samsung 教育序號產生器

大學時期在 3C 門市打工時開發的小工具，用來自動化處理 Samsung 星學力教育優惠序號，方便配合門市折扣銷售。

## 📌 專案背景

當時在校園門市工作，每天需要處理大量的 Samsung 教育優惠序號申請。為了提高工作效率，開發了這套自動化系統：

- **自動擷取**：從 Gmail 信箱中自動抓取教育優惠郵件
- **序號解析**：解析郵件內容，提取各類產品折扣序號
- **資料同步**：將序號批次匯入 Google Sheets 方便門市人員查詢使用

## 🎯 支援的序號類型

| 產品類別 | 折扣 |
|---------|------|
| 指定平板 | 9 折 |
| 指定智慧手錶/手環 | 最低 7 折 |
| 指定耳機 | 7 折 |

## 🛠️ 技術架構

- **語言**：Python
- **Gmail API**：讀取教育優惠通知郵件
- **Google Sheets API**：資料儲存與共享
- **正則表達式**：解析 HTML 郵件內容

## 📂 檔案說明

| 檔案 | 說明 |
|-----|------|
| `interface.py` | CLI 互動介面 |
| `normal_serials.py` | 一般序號擷取主程式 |
| `save_serials.py` | 序號儲存功能 |
| `work.py` | 主要工作流程 |
| `fill.py` | 資料填充輔助 |

## ⚙️ 使用前準備

1. 設定 Google Cloud Console 專案並啟用 Gmail API 與 Google Sheets API
2. 下載 `credentials.json` 並放置於專案根目錄
3. 設定 Google Sheets 服務帳戶並下載 `sheet_credentials.json`
4. 安裝相依套件：

```bash
pip install google-auth google-auth-oauthlib google-api-python-client gspread pandas pillow pyfiglet
```

## 🚀 執行方式

```bash
python interface.py
```

或直接執行批次檔：

```bash
World_Gym_何教練.bat
```

## 📝 備註

這是個學生時期的練習專案，主要用於學習 Google API 串接與自動化流程設計。程式碼風格可能不夠成熟，但確實在當時提升了不少工作效率！

---

*此專案僅供學習參考，請勿用於商業用途。*