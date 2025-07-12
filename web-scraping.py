import pandas as pd
from playwright.sync_api import sync_playwright

def run():
    data = []
    keywords = ["วิศวกรรม ปัญญาประดิษฐ์" , "วิศวกรรม คอมพิวเตอร์"] 

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://course.mytcas.com/")
        page.wait_for_load_state("networkidle")

        base_url = "https://course.mytcas.com"

        for keyword in keywords:
            print(f"\n🔍 ค้นหา: {keyword}")
            search_input = page.locator("input[placeholder='พิมพ์ชื่อมหาวิทยาลัย คณะ หรือหลักสูตร']")
            search_input.fill("")  
            page.wait_for_timeout(500)
            search_input.fill(keyword)
            search_input.press("Enter")
            page.wait_for_timeout(2000)

            results = page.locator(".t-programs > li")
            count = results.count()
            print(f"  เจอ {count} รายการ")

            for i in range(count):
                li = results.nth(i)
                title_full = li.inner_text().strip()
                link = li.locator("a").get_attribute("href")
                full_link = link if link.startswith("http") else base_url + link

                lines = title_full.splitlines()
                if len(lines) >= 3:
                    faculty = lines[1].strip().replace('›', ' > ')
                    university = lines[2].strip()
                else:
                    faculty = ""
                    university = ""

                fee_text = "ไม่พบข้อมูล"
                type = ""
                program_name = ""

                if link:
                    detail_page = browser.new_page()
                    detail_page.goto(full_link)
                    detail_page.wait_for_load_state("networkidle")

                    dt_locator = detail_page.locator("dt:has-text('ชื่อหลักสูตร')").nth(0)
                    if dt_locator.count() > 0:
                        program_name = detail_page.evaluate(
                            "(dt) => dt.nextElementSibling?.innerText",
                            dt_locator.element_handle()
                        )

                    dt_locator = detail_page.locator("dt:has-text('ประเภทหลักสูตร')")
                    if dt_locator.count() > 0:
                        type = detail_page.evaluate(
                            "(dt) => dt.nextElementSibling?.innerText",
                            dt_locator.element_handle()
                        )

                    dt_locator = detail_page.locator("dt:has-text('ค่าใช้จ่าย')")
                    if dt_locator.count() > 0:
                        fee_text = detail_page.evaluate(
                            "(dt) => dt.nextElementSibling?.innerText",
                            dt_locator.element_handle()
                        )

                    detail_page.close()

                print(f"\n{i+1}. 🎓 {program_name}")
                print(f"     🏛️ มหาวิทยาลัย: {university}")
                print(f"     📚 ประเภทหลักสูตร: {type}")
                print(f"     🏫 คณะ: {faculty}")
                print(f"     💸 ค่าใช้จ่าย: {fee_text}")
                print(f"     🔗 ลิงก์: {full_link}")

                data.append({
                    "คำค้น": keyword,
                    "มหาวิทยาลัย": university,
                    "คณะ": faculty,
                    "หลักสูตร": program_name,
                    "ประเภทหลักสูตร": type,
                    "ลิงก์": full_link,
                    "ค่าใช้จ่าย": fee_text
                })

        browser.close()

    df = pd.DataFrame(data)
    df.to_excel("web/data/data.xlsx", index=False)
    print("\nบันทึกข้อมูลทุกคำค้นเสร็จแล้ว")

if __name__ == "__main__":
    run()
