from __future__ import print_function
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
import nltk.data
from sets import Set
import time
from collections import defaultdict

HIT1_MAX_ASSIGN = 1
HIT2_MAX_ASSIGN = 1

def createHIT1(to_trans):
	title = 'Translate a sentence into spanish!'
	description = ('For realz. Just translate this sentence.')
	keywords = 'translate, language'
	 
	#---------------  BUILD OVERVIEW -------------------
	 
	overview = Overview()
	overview.append_field('Title', title)
	overview.append(FormattedContent(to_trans))
	 
	 
	#---------------  BUILD QUESTION 2 -------------------
	 
	qc1 = QuestionContent()
	qc1.append_field('Title','Please translate the sentence')
	 
	fta1 = FreeTextAnswer()
	 
	q1 = Question(identifier="translation",
				  content=qc1,
				  answer_spec=AnswerSpecification(fta1))
	 
	#--------------- BUILD THE QUESTION FORM -------------------
	 
	question_form = QuestionForm()
	question_form.append(overview)
	question_form.append(q1)
	 
	#--------------- CREATE THE HIT -------------------
	 
	resultSet = mtc.create_hit(questions=question_form,
				   max_assignments=HIT1_MAX_ASSIGN,
				   title=title,
				   description=description,
				   keywords=keywords,
				   duration = 60*5,
				   reward=0.05)

	
	return (resultSet[0].HITId,to_trans)

def createHIT2(possibleAnswers,sentence):
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
	overview.append(FormattedContent(sentence))
	 
	 
	#---------------  BUILD QUESTION 2 -------------------
	 
	qc1 = QuestionContent()
	qc1.append_field('Title','Please pick the best translation for the sentence above.')
	 
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
	 
	#--------------- CREATE THE HIT -------------------
	 
	resultSet = mtc.create_hit(questions=question_form,
				   max_assignments=HIT2_MAX_ASSIGN,
				   title=title,
				   description=description,
				   keywords=keywords,
				   duration = 60*5,
				   reward=0.05)

	
	return (resultSet[0].HITId,sentence,ratingsDic)

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

 
ACCESS_ID ='***REMOVED***'
SECRET_KEY = '***REMOVED***'
HOST = 'mechanicalturk.sandbox.amazonaws.com'

hitIds = Set()
hitsDic = {}
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
					  aws_secret_access_key=SECRET_KEY,
					  host=HOST)
 
to_trans = raw_input('Input text to translate: ')

#do magin nltk stuff to find sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = tokenizer.tokenize(to_trans)

for sentence in sentences:
	hitId, sentence = createHIT1(sentence)
	hitIds.add(hitId)
	hitsDic[hitId] = sentence

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
	hitId, sentence, answers = createHIT2(val,key)
	hitIds.add(hitId)
	hitsDic[hitId] = sentence
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

for sentence, dic in votes.iteritems():
	translations[sentence] = answersDic[sentence][keyWithMaxVal(dic)]

for sentence in sentences:
	print(translations[sentence],end=' ')




