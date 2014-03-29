mTurkTranslation
================

Texas A&M University<br> Computer Science and Engineering <br>
CSCE 438 Distributed Data Intensive System<br><br>
Team name: **The alpha**<br>
Team member: Erick Chaves, Guinn Paul Unger, Sujin Lee<br>

Translate text using amazon mechanical turk!
--------------------------------------------

<br>**Description**<br>
There are many books and documents translated from one language to other languages. Usually only one person works to translate the books or documents and it costs a lot of money. However, the translation sometimes does not work perfectly.<br>
This program helps to solve the problem. The program uses 'Amazon Mechanical Turk' (AMT). AMT divides big task to small tasks and turkers will work on it.Many workers join the work that translates the books or documents by a sentence. Therefore, the quality of translated documents is increased. Also, a requester who wants to translate a book can save money.There would be many people who can speak several languages and the languages they speak could be diverse. The requester can get several versions of translated documents at one time.



<br>**Instruction**
- You need your AWS access key and secret key. (line number is ###)
- Make sure you have 'pip install'. Then do 'pip install pyyaml nltk' to install NLTK for the sentence parsing library. Test the installation by running 'python import nltk'. Run 'nltk.download()' from python to open the NLTK downloader. Then download 'punk' from the Models menu.
- Make sure you have 'boto'. There is a tutorial in the website
http://boto.readthedocs.org/en/latest/ 
- You need to save a text file with the code in the source folder.
- If you wish to submit to the hit to the SANDBOX, change SANDBOX value to TRUE
- To change the number of HITs per sentence, change the value of HIT1_MAX_ASSIGN and HIT2_MAX_ASSIGN (HIT1 for translation task and HIT2 for the selection task)
- First time you run it creates qualitification type, uncommand the line number ###
- You can run 'python mturk.py' from the command promt.
