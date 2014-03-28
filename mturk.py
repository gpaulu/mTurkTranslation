from boto.mturk.connection import MTurkConnection, QuestionFormAnswer
from boto.mturk.qualification import Qualifications, Requirement
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
import nltk.data

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

def qualifyWorker():
	#check for qualification
	#if not qualified, display test? (test should check that input contains the words we are looking for)
		#if test passed, autogrant, else reject
	#once qualification is granted, let the worker access the HIT
	qualReqResult = mtc.get_qualification_requests(QUALIFICATION_ID,
					page_size=100)
	
	numRequests = qualReqResult.TotalNumResults
	
	for request in qualReqResult:
		workerID = request.SubjectId
		#questFormAnswer = QuestionFormAnswer()
		questFormAnswer = request.answers
		for answers in questFormAnswer:
			for answer in answers[0].fields:
				workerAnswer = answer
				print workerAnswer
				qualReqID = request.QualificationRequestId
				#check answer for key words
				if workerAnswer.find("always") and workerAnswer.find("eat") and workerAnswer.find("eggs") and workerAnswer.find("breakfast") and (workerAnswer.find("wake") or workerAnswer.find("get")):
					mtc.grant_qualification(qualReqID)
				else:
					mtc.reject_qualification_request(qualReqID)

def createHIT1(to_trans, qualificationType):

	
	
	title = 'Translate a sentence into spanish!'
	description = ('For realz. Just translate this sentence.')
	keywords = 'translate, language'
	#qualifications = Qualificatiosn(qualificationType)
	
	# ratings =[('Very Bad','-2'),
	#          ('Bad','-1'),
	#          ('Not bad','0'),
	#          ('Good','1'),
	#          ('Very Good','1')]
	 
	#---------------  BUILD OVERVIEW -------------------
	 
	overview = Overview()
	overview.append_field('Title', title)
	overview.append(FormattedContent(to_trans))
	 
	 
	#---------------  BUILD QUESTION 2 -------------------
	 
	qc1 = QuestionContent()
	qc1.append_field('Title','Plese translate the sentence')
	 
	fta1 = FreeTextAnswer()
	 
	q1 = Question(identifier="translation",
	              content=qc1,
	              answer_spec=AnswerSpecification(fta1))
	 
	#--------------- BUILD THE QUESTION FORM -------------------
	 
	question_form = QuestionForm()
	question_form.append(overview)
	question_form.append(q1)
	 
	#--------------- CREATE QUALIFICATION REQUIREMENT -------------------
	qual_req = Requirement(qualification_type_id=QUALIFICATION_ID,
					comparator="Exists")
	
	quals = Qualifications(requirements=[qual_req])
	#--------------- CREATE THE HIT ------------------- 
	resultSet = mtc.create_hit(questions=question_form,
	               max_assignments=1,
	               title=title,
	               description=description,
	               keywords=keywords,
	               duration = 60*5,
	               reward=0.05,
				   qualifications=quals)

	for hit in resultSet:
		print hit.HITId

	

 
ACCESS_ID ='***REMOVED***'
SECRET_KEY = '***REMOVED***'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
QUALIFICATION_ID = '***REMOVED***'

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

#qualifications = mtc.get_all_qualifications_for_qual_type(QUALIFICATION_ID)				  
				  
#qualification_type = createQualification("Spanish") #use this to edit our qualification. WILL REQUIRE NEW NAME, OR DELETING THE OLD ONE
qualification_type = mtc.get_qualification_type(QUALIFICATION_ID)[0]
to_trans = raw_input('Input text to translate: ')

#do magin nltk stuff to find sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = tokenizer.tokenize(to_trans)

#check for qualification requests
#if there are any, and the turker passed the test, grant the qualificatioins
qualifyWorker()

for sentence in sentences:
	createHIT1(sentence, qualification_type)
	



