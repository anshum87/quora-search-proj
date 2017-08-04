# quora-search-proj
Build a search index from a Quora questions database.
Use it to support search queries of various kinds.

Usage:

Install Eclipse, Python and pydev support. Install Google app engine from eclipse.
Download the code and open it with eclipse. Run as a Google App Engine project.

Now your project is running on localhost. These are the API's that the server supports:

http://localhost:8080/Init     This is to initialize the server to build the search index.

http://localhost:8080/SearchWords?words=food,light&freqs=1,2    This is to search for the words food and light
in the database. Currently freqs is not supported. It might be supported in the future. It can be used to
specify the minimum number of times each word must be present in the question to be counted.
The output is the list of matching questions along with the count of the number of words that match the words from the query.

http://localhost:8080/topN?patt=box&cnt=100     This is to get the top 100 words(by word frequency count) 
that match the pattern 'box' and lists out their frequencies in the database.

http://localhost:8080/bottomN?patt=Shirt|Pant&cnt=100      This is to get the bottom 100 words(by word frequency count) 
that match the pattern Shirt or Pant. The matching is case insensitive.


Anshum Gupta, Vinit Gupta, D.B.Cooper

