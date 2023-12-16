from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime, timedelta


options = Options()
options.add_experimental_option("detach", True)
options.add_argument('--no-sanbox')
options.add_argument('--disable-notificatioon')
options.add_argument('--disable-infobars')


# Build Scraper Function...
def ScrapTiktokPost(browser, search):
    data = []

    # Searching...

    search_input = browser.find_element(By.XPATH,
                                        "//*[@id='app-header']/div/div[2]/div/form/input")
    search_input.send_keys(search)
    search_input.send_keys(Keys.ENTER)
    sleep(5)

    # menu video
    ii = 0
    while ii < 1:
        try:
            browser.find_element(
                By.XPATH, '//*[@id="search-tabs"]/div[1]/div[1]/div[1]/div[3]').click()
            ii = 1
        except:
            ii = 0
            sleep(5)

    # Load more
    i = 0
    while i < 1:
        try:
            lenOfpage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            match = False
            while (match == False):
                lastCount = lenOfpage
                sleep(2)
                lenOfpage = browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                if lastCount == lenOfpage:
                    match = True
                    raise ValueError(lenOfpage)
            sleep(2)
        except ValueError as ve:
            print(f"Caught an exception: {ve}")
            p = f"{ve}"
            if int(p) > 2000:
                i = 1

    # Scrap Post...

    cards = browser.find_elements(
        By.CLASS_NAME, "css-1soki6-DivItemContainerForSearch")

    for card in cards:
        # ================================Post Description==============================

        desc_part = card.find_element(
            By.CLASS_NAME, "css-1iy6zew-DivContainer")
        tags = [tag.text for tag in desc_part.find_elements(By.TAG_NAME, "a")]
        desc = [des.text for des in desc_part.find_elements(
            By.TAG_NAME, "span")]
        desc = ' '.join(desc)
        tags = ' '.join(tags)

        # ==================================Post Owner==================================

        desc_part = card.find_element(By.CLASS_NAME, "css-1kw4mmh-DivPlayLine")
        username = desc_part.find_element(By.TAG_NAME, "a")
        user_link = username.get_attribute("href")
        user_img = username.find_element(
            By.TAG_NAME, "img").get_attribute("src")
        name = username.find_element(By.TAG_NAME, "p").text
        vidCount = desc_part.find_element(
            By.CLASS_NAME, "css-ws4x78-StrongVideoCount").text

        # ==============================Post Video========================================

        desc_part = card.find_element(By.CLASS_NAME, "css-bbkab3-DivContainer")
        post = desc_part.find_element(By.TAG_NAME, "a")
        post_link = post.get_attribute("href")
        post_img = post.find_element(By.TAG_NAME, "img").get_attribute("src")
        #post_vid = postfind_element(By.TAG_NAME,"video").get_attribute("src")
        posted_date = desc_part.find_element(
            By.CLASS_NAME, "css-dennn6-DivTimeTag").text

        data.append({desc, tags, name, user_img, user_link,
                    post_link, post_img, posted_date, vidCount})

    browser.close()
    return data


# Function to convert Posted Date from String To Date
def convert_to_date(date_str):
    try:
        # If the string is in 'YYYY-MM-DD' format, return it as is
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except ValueError:
        pass

    try:
        # If the string is in 'MM-DD' format, append the current year
        current_year = datetime.now().year
        return pd.to_datetime(f"{current_year}-{date_str}", format='%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        pass

    try:
        # If the string is in 'Xh ago' format, subtract hours from the current date
        hours_ago = int(date_str.split('h')[0])
        current_date = datetime.now() - timedelta(hours=hours_ago)
        return current_date.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # If all conversion attempts fail, return NaN
    return pd.NaT


# Function to convert Count Viewer from String To Numbre
def StringToNumber(strr):
    if 'K' in strr:
        hours_ago = float(strr.split('K')[0]) * 1000
    elif 'M' in strr:
        hours_ago = float(strr.split('M')[0]) * 1000000
    else:
        hours_ago = float(strr)
    return hours_ago


# ================================ MAIN ==================================================

columns = ['Description', 'Tags', 'Username', 'User_Img',
           'User_Link', 'Post_Link', 'Post_Img', 'Posted_Date', 'Viewer_Count']
df = pd.DataFrame(columns=columns)
WordsToSearch = ['morocco', 'maroc', 'المغرب']

for search in WordsToSearch:

    # THIS INITIALIZES THE DRIVER (AKA THE WEB BROWSER)
    browser = webdriver.Chrome(options=options)

    # load the webpage
    browser.get('https://www.tiktok.com')

    # Get the Data
    db = ScrapTiktokPost(browser, search)

    df = df.append(db, ignore_index=True)
    print(len(db))

# The DataFrame after conversion
df['Posted_Date'] = df['Posted_Date'].apply(convert_to_date)
df['Viewer_Count'] = df['Viewer_Count'].apply(StringToNumber)

# Save the Data into File CSV
df.to_csv(r'C:\Users\dell\Desktop\Job\ScrapingTikTokPost.csv', index=False)
