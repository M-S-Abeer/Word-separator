from my_corpus import MyCorpus as mc
from ahocorapy import KeywordTree as AhoCora
import functools

lib = mc()
aho = AhoCora(case_insensitive=True)

def buildTrie():
    for word in lib.wordList:
        aho.add(str(word))
    aho.finalize()

buildTrie()

def bigramScore(res):
    cnt=res[0] in lib.wordList
    for i in range(1, len(res)):
        if((res[i-1], res[i]) in lib.bigrams):
            cnt+=2
        # elif res[i] in lib.wordList:
        #     cnt+=1
        elif res[i] not in lib.wordList:
            cnt-=1
        # else:
        #     cnt-=1
    return cnt

results=set()

def storeResult(score, line):
    results.add((score, tuple(line)))

def countChar(line):
    ans=int(0)
    for word in line:
        ans+=len(word)+int(1)
    return ans

def printResult():
    mn=min([sc[0] for sc in results])
    res=[ [items[0]-mn+1, (" ").join(list(items[1]))] for items in list(results)]
    res.sort(key=lambda x: (-x[0], x[1].count(' ')))
    # print("pqr: ", res)
    return res
    # print(res)
    max_len=int(max(countChar(sc[1]) for sc in res))
    for score, line in res:
        print("{:{x}} [Score: {}]".format(str((" ").join(line)), score-mn+1, x=max_len))
        # print((" ").join(line), "[ Score -> ", score-mn+1, "]")

def bruteForce(qText, word_starts, pos: int, strt: int, len: int, res):
    if pos==len: #Base Case
        storeResult(bigramScore(res), res)
        # print("Result: ", res, bigramScore(res))
        return None
    next_words=3 # determines how many valid positions it will check
    for i in range(pos, len):
        if not word_starts[i]:
            continue
        for val in word_starts[i]:
            tmp=res.copy()
            if i>strt:
                tmp.append(qText[strt:i])
            tmp.append(qText[i:i+val])
            # print(tmp, "from", i, val)
            bruteForce(qText, word_starts, i+val, i+val, len, tmp)
        next_words-=1
        if not next_words:
            return None


### Gets query text and returns word tokens
def query(qText=""):
    qText+="." #ending indicator
    qText=qText.replace(" ", "").lower()
    results.clear()
    # print(qText)
    ### Run aho-corasick and generate lists of possible words in each end-points
    all_result=aho.search_all(qText) # gets the list of all possible dictionary words in format(word, start_pos)
    qLen=len(qText)
    word_starts=[[] for i in range (0, qLen)] # list of possible word length from each position
    word_starts[-1].append(int(1))

    for val, pos in all_result:
        # print(val, pos, len(val))
        word_starts[pos].append(int(len(val)))
    
    # print(all_result)
    # print(word_starts)
    # print(qLen)
    ### Call brute-force for smaller sentences
    bruteForce(qText, word_starts, int(0), int(0), int(qLen), [])
    return printResult()
    ### Try randomized algorithm for larger sentences

# take queries
# while(True):
#     qText=str(input("Enter your query sentence: "))
#     print('Your query: "' + qText + '"')
#     query(str(qText))
