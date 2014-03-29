from boto.mturk.connection import MTurkConnection, QuestionFormAnswer
from boto.mturk.qualification import Qualifications, Requirement
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
import nltk.data
from sets import Set
import time

SANDBOX = True

def createQualification(language): #returns the qualType
	title = "English to " + language + " Translator Qualification"
	descrip = "Obtain a qualification to complete tasks requiring translation from English to " + language
	status = 'Active'
	keywords = "qualification, translation"
	retry_delay = 10 #small for testing, should be alot bigger or not specified
	test_duration = 300 #5 minutes
	answer_key=None 
	answer_key_xml=None 
	auto_granted=False 
	auto_granted_value=1
	#string to check for translation:
	test_trans = "Siempre como huevos para desayuno cuando me despierto." #"I always eat eggs for breakfast when I wake up"
	#---------------  BUILD OVERVIEW -------------------
	 
	qual_overview = Overview()
	qual_overview.append_field('Title', title)
	qual_overview.append_field('Text' , descrip)
	
	#---------------  BUILD FREE TEXT ANSWER -------------------
	
	
	#---------------  BUILD QUESTION -------------------
	qual_qc = QuestionContent()
	qual_qc.append_field('Title','Please translate the sentence')
	qual_qc.append_field('Text', test_trans)		#This is where the actual question is printed
	
	qual_fta = FreeTextAnswer()
	 
	qual_q1 = Question(identifier="translation",
	              content=qual_qc,
	              answer_spec=AnswerSpecification(qual_fta))
	 
	#--------------- BUILD THE QUESTION FORM -------------------
	 
	qual_question_form = QuestionForm()
	qual_question_form.append(qual_overview)
	qual_question_form.append(qual_q1)
	
	#--------------- CREATE THE QUALIFICATION TYPE -------------------
	
	qualType = mtc.create_qualification_type(title, 
					descrip, 
					status, 
					keywords, 
					retry_delay,
					qual_question_form,	#the "test" value
					answer_key,
					answer_key_xml,
					test_duration,
					auto_granted,
					auto_granted_value)
					
	return qualType

ACCESS_ID =''
SECRET_KEY = ''
if SANDBOX:
	HOST = 'mechanicalturk.sandbox.amazonaws.com' 
else: 
	HOST = 'mechanicalturk.amazonaws.com'

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
					  aws_secret_access_key=SECRET_KEY,
					  host=HOST)
	
qualification_type = createQualification("Spanish") #use this to edit our qualification. WILL REQUIRE NEW NAME, OR DELETING THE OLD ONE