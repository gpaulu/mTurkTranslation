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



<br>**Setup Instructions**
- You need your AWS access key and secret key. These will need to be used in "mturk.py" on lines ###, and in "createQualificationType.py" on lines 65 and 66
- Make sure you have 'pip' installed. Then run 'pip install pyyaml nltk' to install NLTK for the sentence parsing library. Test the installation by running 'python import nltk'. Run 'nltk.download()' from python to open the NLTK downloader. Then download 'punkt' from the Models menu.
- Make sure you have 'boto' installed. There is a tutorial in the website
http://boto.readthedocs.org/en/latest/ 
- You need to save a text file for your input in the source folder. We have provided "giveMouseCookie.txt" as a sample.
- If you wish to submit to the HIT to the SANDBOX, change SANDBOX value to true, on line 8 in "createQualificationType.py", and on line ### in "mturk.py"
- To change the number of HITs per sentence, change the value of HIT1_MAX_ASSIGN and HIT2_MAX_ASSIGN (HIT1 for translation task and HIT2 for the selection task)


<br>**Running the Program**
- Run "python createQualificationType.py" to create a Qualification that is linked to your account. This only needs to be run once, and you can check that the qualification exists from your Requester Dashboard under Manage->Qualifcation Types
- Run "python mturk.py" and enter the file name (e.g. Input test file to translate: giveMouseCookie.txt)
- A message will appear indicating that the program is "Waiting for HITs to be completed", which will iterate every 30 seconds. 
- When a HIT is submitted by a qualified worker, the result is stored. Once several workers submit answers for the same sentence, the second HIT is created to have qualified workers vote on the best translation.
