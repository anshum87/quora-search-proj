from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import logging

from core.indexbuilder import IndexBuilder

class MainPage(webapp.RequestHandler):
        
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!!')
        

_index_builder = IndexBuilder(); 

class InitIndex(webapp.RequestHandler):
    def get(self):
        global _index_builder;
        _index_builder.Build('data/quora_duplicate_questions_orig.tsv');
        self.response.out.write(len(_index_builder._index.search_table));
        
class SearchProcessor(webapp.RequestHandler):
        
    def get(self):
        global _index_builder;
        
        wordlist = self.request.get('words',"").split(",")
        freqlist = self.request.get('freqs',"").split(",")
        if(freqlist==['']):
            freqlist=[1]*len(wordlist);
            
        logging.info("Searching Results for" + str(wordlist) + "\t" + str(freqlist));
        
        [wordliststats, answerlist] = _index_builder.Search(wordlist, freqlist);
        self.response.headers['Content-Type'] = 'text/plain'
        
        res='Word    #Questions    #OccurenceCount'
        for word in wordliststats:
            s1 = 0
            s2 = 0
            response = ""
            for aword in wordliststats[word]:
                s1 += wordliststats[word][aword][0]
                s2 += wordliststats[word][aword][1]
                response+= '\t' + aword + '\t' + str(wordliststats[word][aword][0]) + '\t' + str(wordliststats[word][aword][1]) + '\n'
            
            res += '\n' + word + '\t' + str(s1) + '\t' + str(s2) + '\n' + response.decode('utf-8') + '\n'
        
             
        res += '\n\nAnswer    CountAll\n'
        for answer in answerlist:
            res+= answer[1].decode('utf-8') + '\t' + str(answer[2]) + '\n'
              
        self.response.out.write(res);
              
        
       
        
class TopNHandler(webapp.RequestHandler):
    
    def get(self):
        global _index_builder;
        
        cnt = int(self.request.get('cnt'));
        patt = self.request.get('patt');
        
        response = _index_builder.TopResults(cnt, patt);
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(response);
        
class BottomNHandler(webapp.RequestHandler):
    
    def get(self):
        global _index_builder;
        
        cnt = int(self.request.get('cnt'));
        patt = self.request.get('patt');
        response = _index_builder.BottomResults(cnt, patt);
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(response);
            
#===============================================================================
# class SearchWords(webapp.RequestHandler):
#     _search_processor = new SearchProcessor();
#     def get(self):
#         wordlist = self.request.get('wordlist')
#         freqlist = self.request.get('freqlist')
#         numreq = self.request.get('num')
#         
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write(wordlist + "--" + freqlist);
#         results= _search_processor.ExecuteQuery(_index_builder.GetSearchIndex(), 
#                        wordlist.split(','), freqlist.split(','), numreq);
#         self.response.write(ProcessResult(results))
#         
#     def ProcessResult(results):
#         return results.toString()
#===============================================================================
        


app = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/Init', InitIndex),
                                      ('/SearchWords',SearchProcessor),
                                      ('/WordsFraction/.*', MainPage),
                                      ('/topN', TopNHandler),
                                      ('/bottomN', BottomNHandler)],
                                     debug=True)

 
def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
