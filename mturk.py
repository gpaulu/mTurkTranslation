from __future__ import print_function
from boto.mturk.connection import MTurkConnection, QuestionFormAnswer
from boto.mturk.qualification import Qualifications, Requirement
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
import nltk.data
from sets import Set
import time
from collections import defaultdict

HIT1_MAX_ASSIGN = 1
HIT2_MAX_ASSIGN = 1

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
				#print workerAnswer
				qualReqID = request.QualificationRequestId
				#check answer for key words
				if workerAnswer.find("always") and workerAnswer.find("eat") and workerAnswer.find("eggs") and workerAnswer.find("breakfast") and (workerAnswer.find("wake") or workerAnswer.find("get")):
					mtc.grant_qualification(qualReqID)
				else:
					mtc.reject_qualification_request(qualReqID)

def createHIT1(to_trans,context):

	
	
	title = 'Translate a sentence into spanish!'
	description = ('For realz. Just translate this sentence.')
	keywords = 'translate, language'
	#qualifications = Qualificatiosn(qualificationType)
	
	#---------------  BUILD OVERVIEW -------------------
	 
	overview = Overview()
	overview.append_field('Title', title)
	overview.append(FormattedContent('<p>' + context + '</p>' + '<p><b>' + to_trans + '</b></p>'))
	 
	 
	#---------------  BUILD QUESTION 2 -------------------
	 
	qc1 = QuestionContent()
	qc1.append_field('Title','Please translate the bolded sentence')
	 
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
				   max_assignments=HIT1_MAX_ASSIGN,
				   title=title,
				   description=description,
				   keywords=keywords,
				   duration = 60*5,
	               reward=0.05,
				   qualifications=quals)

	
	return resultSet[0].HITId

def createHIT2(possibleAnswers,sentence, context):
	title = 'Pick the best translation!'
	description = ('Pick the best translation!')
	keywords = 'translate, language'

	ratingsDic = {}
	ratings = []
	i = 0
	for answer in possibleAnswers:
		ratings.append((answer,i))
		ratingsDic[i] = answer
		i = i + 1
	 
	#---------------  BUILD OVERVIEW -------------------
	 
	overview = Overview()
	overview.append_field('Title', title)
	overview.append(FormattedContent('<p>' + context + '</p>' + '<p><b>' + sentence + '</b></p>'))
	 
	 
	#---------------  BUILD QUESTION 2 -------------------
	 
	qc1 = QuestionContent()
	qc1.append_field('Title','Please pick the best translation for the bolded sentence above.')
	 
	fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',
                      selections=ratings,
                      type='text',
                      other=False)
 
	q1 = Question(identifier='pick',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)
	 
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
				   max_assignments=HIT2_MAX_ASSIGN,
				   title=title,
				   description=description,
				   keywords=keywords,
				   duration = 60*5,
				   reward=0.05,
				   qualifications=quals)

	
	return (resultSet[0].HITId,ratingsDic)

def get_all_reviewable_hits(mtc):
	page_size = 50
	hits = mtc.get_reviewable_hits(page_size=page_size)
	total_pages = float(hits.TotalNumResults)/page_size
	int_total= int(total_pages)
	if(total_pages-int_total>0):
		total_pages = int_total+1
	else:
		total_pages = int_total
	pn = 1
	while pn < total_pages:
		pn = pn + 1
		print("Request hits page %i" % pn)
		temp_hits = mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
		hits.extend(temp_hits)
	return hits	

def waitUntilHIT1Complete(mtc, hitIds):
	rev_hitIds = Set()
	while True:
		print('Waiting for HITs to be completed')
		#check for qualification requests
		#if there are any, and the turker passed the test, grant the qualificatioins
		qualifyWorker()
		time.sleep(30) #sleep for 1 min
		rev_hits = get_all_reviewable_hits(mtc)
		for rev_hit in rev_hits:
			rev_hitIds.add(rev_hit.HITId)
		if rev_hitIds.issuperset(hitIds):
			return rev_hits

def keyWithMaxVal(dic):
	max_val = -1
	max_key = -1
	for key, value in dic.iteritems():
		if value > max_val:
			max_val = value
			max_key = key
	return max_key

def getContext(idx, sentences):
	ret = ''
	for sentenceInx in xrange(max(0,idx-4),min(len(sentences),idx+4)):
		ret += ' ' + sentences[sentenceInx]
	return ret.strip()

#fuction to delete existing hits, only for testing purposes
def deleteExistingHITs():
	existingHits = list(mtc.get_all_hits())
	for hit in existingHits:
		mtc.disable_hit(hit.HITId)
	return
 
ACCESS_ID =''
SECRET_KEY = ''
HOST = 'mechanicalturk.sandbox.amazonaws.com' if SANDBOX  else 'mechanicalturk.amazonaws.com'
QUALIFICATION_ID = ''

hitIds = Set()
hitsDic = {}


mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
					  aws_secret_access_key=SECRET_KEY,
					  host=HOST)

#qualifications = mtc.get_all_qualifications_for_qual_type(QUALIFICATION_ID)				  
				  
#qualification_type = createQualification("Spanish") #use this to edit our qualification. WILL REQUIRE NEW NAME, OR DELETING THE OLD ONE
qualification_type = mtc.get_qualification_type(QUALIFICATION_ID)[0]
to_trans = raw_input('Input test file to translate: ')
with open(to_trans, "r") as myfile:
	data=myfile.read()
#do magin nltk stuff to find sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = tokenizer.tokenize(data)

#deleteExistingHITs() #uncomment for testing

for idx, sentence in enumerate(sentences):
	context = getContext(idx,sentences)
	hitId = createHIT1(sentence,context)
	hitIds.add(hitId)
	hitsDic[hitId] = (sentence, context)

rev_hits = waitUntilHIT1Complete(mtc,hitIds)

possibleAns = defaultdict(Set)

for hit in rev_hits:
	if hit.HITId in hitIds:
		assignments = mtc.get_assignments(hit.HITId)
		for assignment in assignments:
			#print("Answers of the worker %s" % assignment.WorkerId)
			for question_form_answer in assignment.answers[0]:
				for value in question_form_answer.fields:
					#print("%s: %s" % (hitsDic[hit.HITId],value))
					possibleAns[hitsDic[hit.HITId]].add(value)
			#print("--------------------")
			mtc.approve_assignment(assignment.AssignmentId)
		mtc.disable_hit(hit.HITId)

print('Creating the second stage HITS')

hitIds = Set()
answersDic = {}

for key, val in possibleAns.iteritems():
	sentence, context = key
	hitId, answers = createHIT2(val,sentence,context)
	hitIds.add(hitId)
	hitsDic[hitId] = (sentence, context)
	answersDic[sentence] = answers

rev_hits = waitUntilHIT1Complete(mtc,hitIds)

votes = {}

for hit in rev_hits:
	if hit.HITId in hitIds:
		assignments = mtc.get_assignments(hit.HITId)
		for assignment in assignments:
			#print("Answers of the worker %s" % assignment.WorkerId)
			for question_form_answer in assignment.answers[0]:
				#print( question_form_answer)
				for value in question_form_answer.fields:
					#print( "%s: %s" % (hitsDic[hit.HITId],answersDic[int(value)]))
					if hitsDic[hit.HITId] not in votes:
						votes[hitsDic[hit.HITId]] = {}
					if int(value) not in votes[hitsDic[hit.HITId]]:
						votes[hitsDic[hit.HITId]][int(value)] = 0
					votes[hitsDic[hit.HITId]][int(value)] += 1

			#print( "--------------------")
			mtc.approve_assignment(assignment.AssignmentId)
		mtc.disable_hit(hit.HITId)

translations = {}

for key, dic in votes.iteritems():
	sentence, context = key
	translations[sentence] = answersDic[sentence][keyWithMaxVal(dic)]

for sentence in sentences:
	print(translations[sentence],end=' ')




