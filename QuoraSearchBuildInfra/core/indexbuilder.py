#!/usr/bin/python

import csv
from collections import defaultdict
import logging
import re

class SearchIndex():
    norm_table=defaultdict(lambda:set())
    search_table=defaultdict(lambda:defaultdict(lambda:list()))
    ques_table=defaultdict()
    
    def Reset(self):
        self.search_table.clear()
        self.ques_table.clear()
        self.norm_table.clear()
        
        
class WordNormalizer():
    def GetNormalizedWord(self, word):
        return re.sub('[^A-Za-z0-9]+', '', word)
    

class IndexBuilder():
    _index = SearchIndex();

    
    def Build(self, qfilename):
        self._index.Reset();
        
        csvfile = open(qfilename, 'rb')
        csvreader = csv.reader(csvfile, delimiter='\t')
        csvreader.next()
        
        tempcnt=defaultdict(lambda:0)
        
        wn = WordNormalizer()
        
        for row in csvreader:
            #print logging.info("rowq %s", row[3]);
            tempcnt.clear()
            
            if(self._index.ques_table.get(row[1])==None):
            
                for word in row[3].split():
                    tempcnt[word]+=1;
                    norm_word=wn.GetNormalizedWord(word)
                    self._index.norm_table[norm_word].add(word)
                    self._index.norm_table[word].add(word)
                    
                for word in tempcnt:   
                    self._index.search_table[word][tempcnt[word]].append(row[1]);
                        
                self._index.ques_table[row[1]]=row[3];
                
                        
            if(self._index.ques_table.get(row[2])==None):
                
                tempcnt.clear()
                
                for word in row[4].split():
                    tempcnt[word]+=1;
                    norm_word=wn.GetNormalizedWord(word)
                    self._index.norm_table[norm_word].add(word)
                    self._index.norm_table[word].add(word)
                    
                for word in tempcnt:   
                    self._index.search_table[word][tempcnt[word]].append(row[2]);
                
                self._index.ques_table[row[2]]=row[4];
                
                
    def BuildWordCountStats(self, word):
        word_stat = defaultdict(lambda:list()) # num_ques, num_occurrences
        for aword in self._index.norm_table[word]:
            word_stat[aword]=[sum((len(self._index.search_table[aword][c])) for c 
                                           in self._index.search_table[aword]),
                              sum((len(self._index.search_table[aword][c]))*c for c 
                                           in self._index.search_table[aword])
                              ]
        
        return word_stat
                
    
    def Search(self, wordlist, freqlist):
        answerset = defaultdict(lambda:0)
        wordliststats = defaultdict()
        
        for word in wordlist:
            wordliststats[word]=self.BuildWordCountStats(word)
            for aword in self._index.norm_table[word]:
                for nc in self._index.search_table[aword]:
                    #if nc<freqlist[i]:
                    #   continue
                    for qid in self._index.search_table[aword][nc]:
                        answerset[qid]+=nc;
               
        
        answerlistsorted = sorted(answerset, key=lambda qid : 
                                  list([answerset[qid], 
                                    self._index.ques_table[qid]]),
                                  reverse = True)
        
        response_list = []
                
        for qid in answerlistsorted:            
            response_list.append([qid, self._index.ques_table[qid], answerset[qid]]);
                              
        return [wordliststats, response_list]
    
    
    def TopResults(self, cnt, patt):
        filt_words = filter(lambda w: ((patt=='') or (re.match(patt, w))), 
                                         self._index.search_table)
        
        topwords = (sorted(filt_words, key=lambda d:-1*sum(len(self._index.search_table[d][c]) for c 
                                           in self._index.search_table[d])))[:cnt];
        answerstr = "";
        for w in topwords:
            answerstr += w+'\t' + str(sum(len(self._index.search_table[w][c]) for c 
                                           in self._index.search_table[w])) + '\t' + str(sum((len(self._index.search_table[w][c]))*c for c 
                                           in self._index.search_table[w])) + '\n';
        
        return answerstr
    
    def BottomResults(self, cnt, patt):      
        filt_words = filter(lambda w: ((patt=='') or (re.match(patt, w))), 
                                         self._index.search_table)
        
        topwords = (sorted(filt_words, key=lambda d:sum(len(self._index.search_table[d][c]) for c 
                                           in self._index.search_table[d])))[:cnt];
        answerstr = "";
        for w in topwords:
            answerstr += w+'\t' + str(sum(len(self._index.search_table[w][c]) for c 
                                           in self._index.search_table[w])) + '\t' + str(sum((len(self._index.search_table[w][c]))*c for c 
                                           in self._index.search_table[w])) + '\n';
        
        return answerstr
                