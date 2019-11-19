# -*- coding: utf-8 -*-

import os
import re
import time
import datetime
import settings
import secrets
import traceback
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

def today():
    return str(datetime.datetime.now())[:10].replace('-', '/')

def year():
    return str(datetime.datetime.now())[:4]

def cwd():
    return os.path.dirname(os.path.abspath(__file__)) + '/'

def page_src():
    src = browser.page_source
    with open(cwd() + '/page_src.txt', 'w') as f:
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

    # Leave from "Today's pick up" page
    browser.get('https://www.omiai-jp.com/search')
    time.sleep(1)
    
    
def get_person():
    person = Person()
    person.time = now()
    person.name = browser.find_element_by_id('om-modal-member-detail-basis-nickname').text
    person.age = int(browser.find_element_by_id('om-modal-member-detail-basis-age').text[:2])
    person.area = browser.find_element_by_id('om-modal-member-detail-basis-area').text
    person.body = browser.find_element_by_id('om-modal-member-detail-form').text[3:]
    person.education = browser.find_element_by_id('om-modal-member-detail-school-education').text[3:].replace('\n', '-')
    person.job = browser.find_element_by_id('om-modal-member-detail-occupation').text[3:]
    person.income = browser.find_element_by_id('om-modal-member-detail-annual-income').text[3:]
    person.hometown = browser.find_element_by_id('om-modal-member-detail-hometown-area').text[4:]
    person.inmate = browser.find_element_by_id('om-modal-member-detail-inmate').text[4:]

    tmp = browser.find_element_by_id('om-modal-member-detail-height').text[-5:-2]
    if(tmp):
        person.height = int(tmp) 

    pattern = r'user_id="(\d*?)" action="(.)*?" nickname="' + person.name + '"'
    result = re.search(pattern, page_src())
    person.user_id = result.group(1)

    return person
    

# Search who meets your conditions among "new members"
def search_partners():
    browser.find_element_by_xpath('//*[@id="om-global-menu"]/div[2]/ul/li[1]').click()
    time.sleep(1)
    browser.find_element_by_class_name('om-button-search-menu').click()
    browser.find_element_by_id('om-search-menu-fresh').click()
    browser.find_element_by_id('om-dialog-fresh-information-close').click()
    time.sleep(2)
    
    people_fp = [] # contain Person object who was set a footprint
    people_int = [] # contain Person object who was send "いいね"

    n_limit = 10
    i_loop = 0
        
    while len(people_fp) < n_limit or i_loop < 100:
        elms = browser.find_elements_by_class_name('essential-line')
        for elm in elms:
            if len(people_fp) >= 10:
                break
            
            # Narrow the search results with their ages and areas.
            age = int(elm.text[:2])
            area = elm.text.split(' ')[1]
            if age not in settings.ages_accept:
                continue
            if area not in settings.areas_accept:
                continue
            elm.click()
            time.sleep(1)        

            # Temporarily collect personal infomation from current personal page.
            person = get_person()
            people_fp.append(person)
            
            # Send "いいね" if conditions are met.
            if True:
                try:
                    browser.find_element_by_xpath('//*[@id="om-member-detail-footer-button"]/div/div[1]/div[1]').click()
                    time.sleep(1)
                    people_int.append(person)
                    browser.back()
                    time.sleep(3)

                    # Search "new members" agein
                    browser.find_element_by_xpath('//*[@id="om-search-header"]/div[1]/div/div/div').click()
                    browser.find_element_by_id('om-search-menu-fresh').click()                    
                    time.sleep(2)
    
                    break
                except:
                    print('Exception occured when looking personal pages:')
                    traceback.print_exc()

        i_loop += 1

    return people_fp, people_int


def get_visitors():
    browser.find_element_by_id('om-global-menu-column-footprint').click()
    time.sleep(1)

    people = []

    n_limit = 10
    i_loop = 0

    while len(people) < n_limit and i_loop < 1000:
        try:
            elm = browser.find_element_by_xpath('//*[@id="common-list"]/div[1]/div[' + str(i_loop) + ']/div/div/div[2]/div[1]/div/div[1]')
            ActionChains(browser).move_to_element(elm)
            elm.click()
            time.sleep(1)
            if('om-modal-member-detail' in browser.current_url):
                people.append(get_person())
                browser.back()
        except:
            pass

        i_loop += 1
        continue
        
    return people


def get_matched():
    browser.find_element_by_id('om-global-menu-column-message').click()
    time.sleep(1)

    pattern = r'data-user-id="(\d*?)"'
    user_ids = re.findall(pattern, page_src())
    N = len(user_ids)

    elms = browser.find_elements_by_class_name('om-list-last-action-date')

    people = []
    if len(elms) != N:
        print('Warning! # of UserID and action-date are not equal.')
    else:
        for i in range(N):
            tmp = elms[i].text
            if '前' in tmp or ':' in tmp:
                tmp = today()
            elif year() not in tmp:
                tmp = year() + '/' + tmp
            people.append(Person(time = tmp ,user_id = user_ids[i]))

    return people

    
    
if __name__ == '__main__':
    print("Started at " + now())

    try:
        login()

        people_fp, people_int = search_partners()
        print("# of footprints\t" + str(len(people_fp)))    
        with open(cwd() + 'footprints.txt', 'a') as f:
            for p in people_fp:
                p.show()
                f.write(p.info_secret())
        
        print("# of interests\t" + str(len(people_fp)))    
        with open(cwd() + 'interests.txt', 'a') as f:
            for p in people_fp:
                p.show()
                f.write(p.info_secret())

        people_vs = get_visitors()
        print("# of visitors\t" + str(len(people_vs)))    
        with open(cwd() + 'visitors.txt', 'a') as f:
            for p in people_vs:
                p.show()
                f.write(p.info_secret())

        people_mch = get_matched()
        print("# of matching\t" + str(len(people_mch)))    
        with open(cwd() + 'matching.txt', 'a') as f:
            for p in people_mch:
                p.show()
                f.write(p.info_secret())
            
    except:
        print('Exception occured in main() method:')
        traceback.print_exc()

    browser.quit()
    print("Finished at " + now())
