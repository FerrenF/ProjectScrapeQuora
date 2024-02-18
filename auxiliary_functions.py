import time
import dateparser
import random

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By


# -------------------------------------------------------------
# remove 'k'(kilo) and 'm'(million) from Quora numbers
# -------------------------------------------------------------
def convert_number(number):
    if 'K' in number:
        n = float(number.lower().replace('k', '').replace(' ', '')) * 1000
    elif 'M' in number:
        n = float(number.lower().replace('m', '').replace(' ', '')) * 1000000
    else:
        n = number
    return int(n)


# -------------------------------------------------------------
# convert Quora dates (such as 2 months ago) to DD-MM-YYYY format
# -------------------------------------------------------------
def convert_date_format(date_text):
    try:
        if "Updated" in date_text:
            date = date_text[8:]
        else:
            date = date_text[9:]
        date = dateparser.parse(date_text).strftime("%Y-%m-%d")
    except:  # when updated or answered in the same week (ex: Updated Sat)
        date = dateparser.parse("7 days ago").strftime("%Y-%m-%d")
    return date

SCROLL_DELAY_MIN = 0.2
SCROLL_DELAY_RANGE = 0.1
SCROLL_INCREMENT = 1000
SCROLL_REPOSITION_INTERVAL = 5

def reposition_cursor(driver):
    window_width = driver.execute_script("return window.innerWidth;")
    window_height = driver.execute_script("return window.innerHeight;")
    middle_x = window_width // 2
    middle_y = window_height // 2
    noise_x = random.randint(-window_width/2, window_width/2)
    noise_y = random.randint(-window_width/2, window_width/2)
    final_x = middle_x + noise_x
    final_y = middle_y + noise_y
    actions = ActionChains(driver)
    actions.move_by_offset(final_x, final_y)
    actions.perform()

def scroll_up(self, nb_times):
    for iii in range(0, nb_times):
        self.execute_script(f"window.scrollBy(0,-{SCROLL_INCREMENT})")
        time.sleep(SCROLL_DELAY_MIN+random.randrange(0,round(SCROLL_DELAY_RANGE*10),1)/10)

def scroll_down(self, type_of_page='users', max_loop: int = 0):
    global SCROLL_INCREMENT, SCROLL_DELAY_MIN, SCROLL_DELAY_RANGE, SCROLL_REPOSITION_INTERVAL
    print("Scrolling Page...")
    # Scrolling loop
    running = True
    previous_page = 0
    loop = 0
    attempts = 3  # Number of attempts to check if the page has loaded
    while running and attempts > 0 and loop < max_loop:
        element = self.find_element(By.XPATH, "/html/body")
        element.send_keys(Keys.END)
        loop += 1
        if loop % SCROLL_REPOSITION_INTERVAL == 0:
            print("Move the cursor a bit.")
            reposition_cursor(self)

        current_scroll_height = self.execute_script("return document.body.scrollHeight;")
        how_long_is_this_gonna_take = round(current_scroll_height / SCROLL_INCREMENT)
        if how_long_is_this_gonna_take > 25:
            # oh man it's starting to really get big... how much can we start scrolling and reduce latency?
            SCROLL_INCREMENT *= 1.
            if SCROLL_DELAY_MIN > 0.05:
                SCROLL_DELAY_MIN *= 0.985
        print(f"Back to top...{how_long_is_this_gonna_take} scrolls...")
        scroll_up(self, how_long_is_this_gonna_take)

        time.sleep(random.randrange(2, 5, 1))
        current_page = len(self.page_source)
        if previous_page == current_page:
            attempts -= 1
            print(f"Page didn't change...{attempts}")
        else:
            attempts = 3  # Reset attempts if the page has loaded successfully
        previous_page = current_page
        print(f"Scrolling...{current_scroll_height} Loop counter: {loop}")
