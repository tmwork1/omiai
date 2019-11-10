# -*- coding: utf-8 -*-

import time
import os
import datetime
import settings
import secrets
from selenium import webdriver


class Person():
    def __init__(self, time='', name='', age=0, area='', height=0, body='', education='',
                 job='', income='', hometown='', inmate=''):
        self.time = time
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
        
        

browser = webdriver.Chrome('/usr/local/bin/chromedriver')

def now():
    return str(datetime.datetime.now())[:-7].replace('-', '/')    

def write_page_src():
    with open(os.getcwd() + '/page_src.txt', 'w') as f:
        f.write(browser.page_source)

def switch_window(window_title):
    for w in browser.window_handles:
        browser.switch_to.window(w)
        if browser.title == window_title:
            return
        
def login():
    browser.get('https://fb.omiai-jp.com/');
    browser.find_element_by_class_name('js-register-btn-01').click()
    switch_window('Facebook')
    browser.find_element_by_name('email').send_keys(secrets.facebook_account)
    browser.find_element_by_name('pass').send_keys(secrets.facebook_pass)
    browser.find_element_by_name('login').click()
    time.sleep(10)        
    
def leave_footprints(person_list):
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
        time.sleep(1)

        person = Person()
        person.time = now()
        person.name = browser.find_element_by_id('om-modal-member-detail-basis-nickname').text
        person.age = age
        person.area = area
        person.height = int(browser.find_element_by_id('om-modal-member-detail-height').text[-5:-2])
        person.body = browser.find_element_by_id('om-modal-member-detail-form').text[3:]
        person.education = browser.find_element_by_id('om-modal-member-detail-school-education').text[3:].replace('\n', ' ')
        person.job = browser.find_element_by_id('om-modal-member-detail-occupation').text[3:]
        person.income = browser.find_element_by_id('om-modal-member-detail-annual-income').text[3:]
        person.hometown = browser.find_element_by_id('om-modal-member-detail-hometown-area').text[4:]
        person.inmate = browser.find_element_by_id('om-modal-member-detail-inmate').text[4:]
        person_list.append(person)
        
        browser.back()

        
def test():
    print(settings.ages_accept)


    
if __name__ == '__main__':
    people = []

    print("Browsing started at " + now())
    login()
    leave_footprints(people)   
    browser.quit()
    print("Browsing finished at " + now())
    
    print("# of people\t" + str(len(people)))    
    with open(os.getcwd() + '/people.txt', 'a') as f:
        for p in people:
            p.show()
            f.write(p.info())
        
