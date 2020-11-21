#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk                             #importing ntlk library
from nltk.corpus import brown           # to import brown corpus


# In[2]:


test_sentence_tokens = ['the','google','uses','the','nlp','in','its','google','assistant','which','is','a','very','effective','technique','.']


# In[3]:


import nltk                             
nltk.download('brown')
words = brown.words()


# In[4]:


words = brown.words()
fdist1 = nltk.FreqDist(w.lower() for w in words)

total_words = len(words)

print('Frequency of tokens in sample sententence in Brown according to NLTK:')

for word in test_sentence_tokens:
    print(word,fdist1[word])


# In[5]:


words2 = []
previous = 'EMPTY'
sentences = 0
for word in words:
    if previous in ['EMPTY','.','?','!']:
        ## insert word_boundaries at beginning of Brown,
        ## and after end-of-sentence markers (overgenerate due to abbreviations, etc.)
        words2.append('*start_end*')
    if fdist1[word]==1:
        ## words occurring only once are treated as Out of Vocabulary Words(OOV)
        words2.append('*oov*')         
    else:
        words2.append(word)
    previous = word
words2.append('*start_end*') ## assume one additional *start_end* at the end of Brown

fdist2 = nltk.FreqDist(w.lower() for w in words2)


# In[6]:


print('Calculating bigram counts for sentence, including bigrams with sentence boundaries, i.e., *BEGIN* and *END*')
print('Assuming some idealizations: all periods, questions and exclamation marks end sentences;')

bigrams = nltk.bigrams(w.lower() for w in words2)
## get bigrams for words2 (words plus OOV)

cfd = nltk.ConditionalFreqDist(bigrams)

# for token1 in cfd:
#     if not '*oov*' in cfd[token1]:
#         cfd[token1]['*oov*']=1
#         ## fudge so there can be no 
#         ## 0 bigram

def get_unigram_probability(word):
    if word in fdist1:
        unigram_probability = fdist2[word]/total_words
    else:
        unigram_probability = fdist2['*oov*']/total_words
    return(unigram_probability)

def multiply_list(inlist):
    out = 1
    for number in inlist:
        out *= number
    return(out)

def get_bigram_probability(first,second):
    if not second in cfd[first]:
        print('Backing Off to Unigram Probability for',second)
        unigram_probability = get_unigram_probability(second)
        return(unigram_probability)
    else:
        bigram_frequency = cfd[first][second]
    unigram_frequency = fdist2[first]
    bigram_probability = bigram_frequency/unigram_frequency
    return(bigram_probability)

def calculate_bigram_freq_of_sentence_token_list(tokens):
    prob_list = []
    ## assume that 'START' precedes the first token
    previous = '*start_end*'
    for token in tokens:
        if not token  in fdist2:
            token = '*oov*'
        next_probability = get_bigram_probability(previous,token)
        print(previous,token,(float('%.3g' % next_probability)))
        prob_list.append(next_probability)
        previous = token
    ## assume that 'END' follows the last token
    next_probability = get_bigram_probability(previous,'*start_end*')
    print(previous,'*start_end*',next_probability)
    prob_list.append(next_probability)
    probability = multiply_list(prob_list)
    print('Total Probability',float('%.3g' % probability))
    return(probability)



result = calculate_bigram_freq_of_sentence_token_list(test_sentence_tokens)


# In[ ]:





# In[ ]:




