import time
import settings
from selenium import webdriver


browser = webdriver.Chrome('chromedriver')
    
def switch_window(window_title):
    for w in browser.window_handles:
        browser.switch_to.window(w)
        if browser.title == window_title:
            return

def login():
    browser.get('https://fb.omiai-jp.com/');
    browser.find_element_by_class_name('js-register-btn-01').click()
    switch_window('Facebook')
    browser.find_element_by_name('email').send_keys(settings.facebook_account)
    browser.find_element_by_name('pass').send_keys(settings.facebook_pass)
    browser.find_element_by_name('login').click()

def leave_footprints():
    switch_window('https://www.omiai-jp.com/search')
    browser.find_element_by_class_name('om-button-search-menu').click()
    browser.find_element_by_id('om-search-menu-fresh').click()
    browser.find_element_by_id('om-dialog-fresh-information-close').click()
    time.sleep(2)

    essentials = browser.find_elements_by_class_name('essential-line')
    for ess in essentials:
        age = int(ess.text[:2])
        area = ess.text.split(' ')[1]
        if age not in settings.ages_accept:
            continue
        if area not in settings.areas_accept:
            continue
        ess.click()
        time.sleep(2)
        browser.back()
            
    
def test():
    print(settings.ages_accept)


    
if __name__ == '__main__':
    #test()
    login()
    time.sleep(2)
    leave_footprints()
    browser.quit()
