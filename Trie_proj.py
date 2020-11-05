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
        #print(st)

    for i in range(0,25):
        if amt[i]!=0 and root.child[i]!= None:
            c = chr(i + ord('a'))
            amt[i]-=1
            searchWord(root.child[i], amt, st+c, answer)
            amt[i]+=1


def findAllWords(root, amt):
    max =0

    pChild = root
    answer = root
    hold = ''

    for i in range(0,25):
        if(amt[i]!=0 and pChild.child[i] != None):
            hold += chr(i+ord('a'))
            amt[i]-=1
            searchWord(pChild.child[i], amt, hold, answer)
            amt[i]+=1
            hold = ''
    print(answer.big)


file = "/Users/Krish/Desktop/short_dict.txt"
f = open(file, "r")
root = TrieNode()
line = ""

for line in f:
    #print(line)
    insert(root, line.strip())


#try:
#   print('hi')
#    while f.next():
 #       print('im in')
  #      line = f.readline()
   #     print(line)
    #    insert(root, line)
#except:
#    f.close()

arr = ['u','r','w','q','s','d','g','i','e','a','h','c','v']
amt = [0] * 26

for i in range(0,len(arr)):
    amt[ord(arr[i])-ord('a')] += 1

findAllWords(root, amt)












