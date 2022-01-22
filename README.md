# TLInternship2020


Find Webpages relevant to COVID-19's economic impact.

This project aims to find links which relevant to COVID-19's economic impact. The project is based on NLP and NLTK libraries.

Beautiful soup for scrapping the links.

Only one file is used to run the entire project (however, project cab be converted into multiple files in multiple modules.)

Workflow of the project:
Including main function we have 6 functions:

Input: Take valid input ranges from 0 to 10 from user.(That will decide accuracy of the result)

output: Final_urls__{input_taken_from_user}_.csv
column name: Url
Values: actual url paths.
(Note: it can have max to max 1000 URLS and min can be 0(min condition will occur if we don't get any match considering user's preference and predefined content.)


1)Working of main method:\
    &emsp;1.1)Take valid input from user ranging from 0 to 10\
    &emsp;1.2)Convert it into required value by dividing it by 10. That will be 'cosine_similarity_preference'. Also, print cosine cosine_similarity_preference and expected output file name on console.\
    &emsp;1.3)Do some initializaion e.g.  Lemmatization of word, Stop words in english language, Word Counter.\
    &emsp;1.4)Get prepopulated_tokens by calling prepopulate_data method(Details in 2nd point) input parameters varibles created in step 1.3. i.e. Lemmatization of word, Stop words in english language, Word Counter.\
    &emsp;1.5) For video also do some compilation.\
    &emsp;1.6) Initialize file_name variable with file path in our case it's
    "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-16/segments/1585370490497.6/warc/CC-MAIN-20200328074047-20200328104047-00000.warc.gz" \
    &emsp;1.7) Now everything would be in try block. If having some exception then print it and stop.\
    &emsp;1.8) Using get_data_in_stream (Details in 3rd point)method get stream data. Input parameter for the method is file_name\
    &emsp;1.9) create empty list for output i.e.final_url_output\
    &emsp;1.10)Iterate through stream and do operation for each record.\
    &emsp;1.11)If record is of type 'warcinfo' or  it's not valid one then please ignore and move ahead with next record.\
    &emsp;1.12) Get content from the stream record if having some encoding then decode that.\
    &emsp;1.13)If my content having some data and it's english then follow steps below.\
   &emsp; 1.14)Get cleaned content text by calling get_text_from_html method (Details in 4th point) input parameters- from 1.1 and contents\
    &emsp;1.15)Using data from 1.14 get it's tokens and store into contents_tokens variable.\
    &emsp;1.16)Now using 1.4 and 1.15 tokens call get_cosine method and get cosine_similarity.\
    &emsp;1.17)If cosine_similarity >= user prefence then add it into our output list which was created at step no 1.9\
    &emsp;1.18) If list is having already 1000 urls then don't proceed ahead just exit from the loop.\
    &emsp;1.19) Create dict with column name as 'Url' and values will be our final output list. Convert that into expected .csv output file.\
 
 2)Working of prepopulate_data method:\
  &emsp;  2.1)Taken list of URL's for articles relating to COVID 19 economic impact.(Note: that can be taken externally as per user's demand.)\
    &emsp;2.2) extract data from the above urls using data_extraction method(Detailed in 5th point)\
    &emsp;2.3)Using data from 2.2 create token containing number words and number of occurances. Print it and return as output.\
    
    
 3)Working of get_data_in_stream method:\
     &emsp;3.1) If file name starts with http or https then using requests package method .get get raw data and pass it to the stream and return it.\
     &emsp;3.2)Else simply open file and store data into stream and return it.\
     
 4)Working of get_text_from_html method:\
     &emsp;4.1)Using BeautifulSoup we will parse content from the html.\
     &emsp;4.2)There would be some datacleaning like removing white spaces, phrases, special characters and some other stuff will be happen.\
     &emsp;4.3)Final cleaned version of data will be return as output\
5) Working of data_extraction method:\
     &emsp;5.1) requesting url content and it's getting passed to the get_text_from_html method and it's result will be return as output.\

 6)Working of get_cosine method:\
      &emsp;Usinng this method cosine similarity between 2 docs would be identified and it's cosine score would be returned.\
      &emsp;6.1) Numerator value would be calculated for both documents by doing intersection and vector multiplication.\
      &emsp;6.2)Denominator value would be calculated for both documents.\
      &emsp;6.3)If Denominator is zero then simply return 0.0\
      &emsp;6.4)Else do calculte Numerator/Denominator and return floating result as cosine distance i.e. cosine similarity between 2 docs.\
