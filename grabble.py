import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome('/Users/Krish/.wdm/drivers/chromedriver/81.0.4044.138/mac64/chromedriver')

#browser.get('http://www.seleniumhq.org/')
browser.get('https://www.playsnatch.io/games/botmatch-6tob9lh')
enter = browser.find_element_by_id('name')
enter.send_keys('Krish')
enter = browser.find_element_by_id('join-button')
enter.click()

#time.sleep(5)
enter = browser.find_element_by_id('start-button')
enter.click()

#browser.implicitly_wait(40)
#time.sleep(10)

#thr=''
#base='tile'

#for x in range(0,6):
#    for y in range(0,13):
#       thr = 'tile' + '-' + str(x) + '-' + str(y)
#        now = browser.find_element_by_id(thr)
#        print(now)

#result = requests.get('https://www.playsnatch.io/games/weeshree-vlen6g7')
#src = result.content

#for tile in soup.find_all(id='tile'):
#   if tile.text != '':
#       letters.append(tile.text);

#print(initial)

#######################################################################################

#Beginning of Word formation

class TrieNode:
    def __init__(self):
        self.child = [None] * 26
        self.leaf = False
        self.big = ''


def insert(root, key):
    n = len(key)
    pChild = root
    for i in range(0,n):
        index = int(ord(key[i]) - ord('a'))
        #print(index)
        if(pChild.child[index] == None):
            pChild.child[index] = TrieNode()

        pChild = pChild.child[index]

    pChild.leaf = True

def searchWord(root, amt, st, answer):

    max = len(answer.big)
    if(root.leaf == True):
        if(len(st)>max):
            max = len(st)
            answer.big = st
            #return

    for i in range(0,26):
        if amt[i]!=0 and root.child[i] != None:
            c = chr(i + ord('a'))
            amt[i]-=1
            searchWord(root.child[i], amt, st+c, answer)
            amt[i]+=1

def searchSteal(root, amt, st, answer,word):

    max = len(answer.big)
    if (root.leaf == True and check(st,word)):
        if (len(st) > max):
            max = len(st)
            answer.big = st

    for i in range(0, 26):
        if amt[i] != 0 and root.child[i] != None:
            c = chr(i + ord('a'))
            amt[i] -= 1
            searchSteal(root.child[i], amt, st + c, answer,word)
            amt[i] += 1

def check(st, word):
    length = len(word)

    if (st[0:length] == word):
        return False
    if(len(st)<=len(word)):
        return False

    broken_word = list(word)
    broken_st = list(st)
    amt_word = [0]*26
    amt_st = [0]*26

    for i in range(0, len(st)):
        if (i<len(word)):
            amt_word[ord(broken_word[i]) - ord('a')] += 1
            amt_st[ord(broken_st[i]) - ord('a')] += 1
        else:
            amt_st[ord(broken_st[i]) - ord('a')] += 1

    for i in range(0,26):
        if amt_st[i] < amt_word[i]:
            return False

    return True


def findAllWords(root, amt, steal, word):
    max =0

    root.big =''
    pChild = root
    answer = root
    hold = ''

    for i in range(0,26):
        if(amt[i]!=0 and pChild.child[i] != None):
            hold += chr(i+ord('a'))
            amt[i]-=1
            if(steal):
                searchSteal(pChild.child[i], amt, hold, answer, word)
            else:
                searchWord(pChild.child[i], amt, hold, answer)
            amt[i]+=1
            hold = ''

#    print(answer.big)
    if (answer.big != ''):
        enter = browser.find_element_by_id('word-field')
        enter.send_keys(answer.big)
        enter.send_keys(Keys.RETURN)


file = "/Users/Krish/Desktop/short_dict.txt"
f = open(file, "r")
root = TrieNode()
line = ""

for line in f:
    insert(root, line.strip())

#end of word formation

#######################################################################################

def grab_pot():
    soup = BeautifulSoup(browser.page_source, 'lxml')
    initial = soup.find_all(id='tiles')
    letters = initial[0].find_all('div')

    bag = []

    for let in letters:
        if let.get_text() != ' ':
            bag.append(let.get_text().lower())

    amt = [0] * 26

    for i in range(0, len(bag)):
        amt[ord(bag[i]) - ord('a')] += 1

    findAllWords(root, amt, False,'')

#    print(bag)

def steal():
    soup = BeautifulSoup(browser.page_source, 'lxml')
    word_bag =[]
    words = soup.find_all(class_='player-word')
    for word in words:
        word_bag.append(word.get_text().lower())
    #print(word_bag)

    initial = soup.find_all(id='tiles')
    letters = initial[0].find_all('div')

    bag = []

    for let in letters:
        if let.get_text() != ' ':
            bag.append(let.get_text().lower())


    for word in word_bag:
        bag = getBag()
        broken = list(word)
        avail = bag + broken

        amt = [0] * 26
        for i in range(0, len(avail)):
            amt[ord(avail[i]) - ord('a')] += 1

        findAllWords(root,amt,True,word)


def getBag():
    soup = BeautifulSoup(browser.page_source, 'lxml')
    initial = soup.find_all(id='tiles')
    letters = initial[0].find_all('div')

    bag = []

    for let in letters:
        if let.get_text() != ' ':
            bag.append(let.get_text().lower())

    return bag

#first_word =''
#first_word != "Game"
while(True):

    #time.sleep(1)

    grab_pot()

    #time.sleep(1)

    steal()

    #time.sleep(1)

    #soup = BeautifulSoup(browser.page_source, 'lxml')
    #message = soup.find_all(id="turn-message")
    #first_word = (message[0].get_text()).split()[0]








