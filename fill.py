import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import hashlib
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def run_instance():
    start_time = time.time()
    with sync_playwright() as playwright:
        result = run(playwright)
    duration = time.time() - start_time
    return duration

def get_md5_from_timestamp() -> str:
    timestamp = f"{time.time()}{random.random()}"
    return generate_md5(timestamp)

def generate_md5(input_string: str) -> str:
    input_bytes = input_string.encode('utf-8')
    return hashlib.md5(input_bytes).hexdigest()[:5]

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True, args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'])
    context = browser.new_context(
        viewport={'width': 800, 'height': 600},
        java_script_enabled=True,
        bypass_csp=True
    )
    page = context.new_page()
    
    try:
        # Block unnecessary resources
        page.route("**/*", lambda route: route.abort() 
                  if route.request.resource_type in ["image", "stylesheet", "font", "media", "other"] 
                  else route.continue_())
        
        # Load initial page
        page.goto("https://samsung-education-promotion.twsamsungcampaign.com", 
                 wait_until='domcontentloaded')
        
        # Click checkboxes
        page.evaluate("""() => {
            const selectors = [
                '.checkstyle',
                'div:nth-child(2) > .mycheckbox > .checkstyle',
                'div:nth-child(3) > .mycheckbox > .checkstyle',
                'div:nth-child(4) > .mycheckbox > .checkstyle',
                'div:nth-child(5) > .mycheckbox > .checkstyle',
                'div:nth-child(6) > .mycheckbox > .checkstyle'
            ];
            selectors.forEach(selector => {
                document.querySelector(selector)?.click();
            });
        }""")
        
        form_data = {
            'email': f"b10902033+{get_md5_from_timestamp()}@gapps.ntust.edu.tw",
            'phone': f"09{''.join(random.choices('0123456789', k=8))}"
        }
        
        # Fill form using single evaluate call
        page.evaluate("""(data) => {
            document.querySelector('#txtEmail').value = data.email;
            document.querySelector('#txtCellPhone').value = data.phone;
        }""", form_data)
        
        page.get_by_role("link", name="填寫完成 >").click()
                 
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        context.close()
        browser.close()

if __name__ == '__main__':
    total_start_time = time.time()
    max_workers = min(multiprocessing.cpu_count() * 2, 8)
    
    try:
        with open("set.txt", "r") as f:
            num_runs = int(f.read().strip())
    except FileNotFoundError:
        num_runs = 1
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_instance) for _ in range(num_runs)]
        
        for i, future in enumerate(futures, 1):
            try:
                duration = future.result()
                print(f"Run {i}/{num_runs}: {duration:.2f}s")
            except Exception as e:
                print(f"Run {i} failed: {str(e)}")
                continue

    print(f"Total time: {time.time() - total_start_time:.2f}s")