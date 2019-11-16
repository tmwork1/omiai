# -*- coding: utf-8 -*-

import os
import re
import time
import datetime
import settings
import secrets
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class Person():
    def __init__(self, time='', user_id='', name='', age=0, area='', height=0, body='', education='', job='', income='', hometown='', inmate=''):
        self.time = time
        self.user_id = user_id
        self.name = name
        self.age = age
        self.area = area
        self.height = height
        self.body = body
        self.education = education
        self.job = job
        self.income = income
        self.hometown = hometown
        self.inmate = inmate

    def show(self):
        text = ''
        for key, val in self.__dict__.items():
            text += str(key) + ":" + str(val) + "\t"
        print(text)
        
    def info(self):
        text = ''
        for key, val in self.__dict__.items():
            text += str(key) + ":" + str(val) + "\t"
        return text + '\n'
        
    def info_secret(self):
        return str(self.time) + '\t' + str(self.user_id) + '\n'

    
browser = webdriver.Chrome('/usr/local/bin/chromedriver')


def now():
    return str(datetime.datetime.now())[:-7].replace('-', '/')    


def page_src():
    src = browser.page_source
    with open(os.getcwd() + '/page_src.txt', 'w') as f:
        f.write(src)
    return src
        
def move(window_title):
    for w in browser.window_handles:
        browser.switch_to.window(w)
        if browser.title == window_title:
            return

        
def login():
    browser.get('https://fb.omiai-jp.com/');
    browser.find_element_by_class_name('js-register-btn-01').click()
    move('Facebook')
    browser.find_element_by_name('email').send_keys(secrets.facebook_account)
    browser.find_element_by_name('pass').send_keys(secrets.facebook_pass)
    browser.find_element_by_name('login').click()
    time.sleep(5)

    move('Omiai')
    if('https://www.omiai-jp.com/search#overlay:om-modal-pickup:' in browser.current_url):
        browser.find_element_by_class_name('om-remove btn-dialog-close').click()
        time.sleep(5)
    
    
def get_person():
    person = Person()
    person.time = now()
    person.name = browser.find_element_by_id('om-modal-member-detail-basis-nickname').text
    person.age = int(browser.find_element_by_id('om-modal-member-detail-basis-age').text[:2])
    person.area = browser.find_element_by_id('om-modal-member-detail-basis-area').text
    person.height = int(browser.find_element_by_id('om-modal-member-detail-height').text[-5:-2])
    person.body = browser.find_element_by_id('om-modal-member-detail-form').text[3:]
    person.education = browser.find_element_by_id('om-modal-member-detail-school-education').text[3:].replace('\n', '-')
    person.job = browser.find_element_by_id('om-modal-member-detail-occupation').text[3:]
    person.income = browser.find_element_by_id('om-modal-member-detail-annual-income').text[3:]
    person.hometown = browser.find_element_by_id('om-modal-member-detail-hometown-area').text[4:]
    person.inmate = browser.find_element_by_id('om-modal-member-detail-inmate').text[4:]

    pattern = r'user_id="(\d*?)" action="(.)*?" nickname="' + person.name + '"'
    result = re.search(pattern, page_src())
    person.user_id = result.group(1)

    return person
    

def set_footprints():
    browser.find_element_by_class_name('column').click()
    time.sleep(1)
    browser.find_element_by_class_name('om-button-search-menu').click()
    browser.find_element_by_id('om-search-menu-fresh').click()
    browser.find_element_by_id('om-dialog-fresh-information-close').click()
    time.sleep(2)
    
    people = []
    elms = browser.find_elements_by_class_name('essential-line')
    for elm in elms:
        age = int(elm.text[:2])
        area = elm.text.split(' ')[1]
        if age not in settings.ages_accept:
            continue
        if area not in settings.areas_accept:
            continue

        elm.click()
        time.sleep(1)        
        people.append(get_person())        
        browser.back()

    return people


def get_visitors():
    browser.find_element_by_id('om-global-menu-column-footprint').click()
    time.sleep(1)

    people = []
    N = -1

    while True:
        N += 1
        if(N > 100):
            break
        try:
            elm = browser.find_element_by_xpath('//*[@id="common-list"]/div[1]/div[' + str(N+1) + ']/div/div/div[2]/div[1]/div/div[1]')
            ActionChains(browser).move_to_element(elm)
            elm.click()
            time.sleep(1)
            if('om-modal-member-detail' in browser.current_url):
                people.append(get_person())
                browser.back()
        except:
            continue
    
    return people

        
    
if __name__ == '__main__':
    print("Started at " + now())

    login()

    people_fp = set_footprints()
    print("# of footprints\t" + str(len(people_fp)))    
    with open(os.getcwd() + '/footprints.txt', 'a') as f:
        for p in people_fp:
            p.show()
            f.write(p.info_secret())

    people_vs = get_visitors()
    print("# of visitors\t" + str(len(people_vs)))    
    with open(os.getcwd() + '/visitor.txt', 'a') as f:
        for p in people_vs:
            p.show()
            f.write(p.info_secret())
    
    browser.quit()
    print("Finished at " + now())
