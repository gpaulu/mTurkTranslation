from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
import nltk.data

def createHIT1(to_trans):
	title = 'Translate a sentence into spanish!'
	description = ('For realz. Just translate this sentence.')
	keywords = 'translate, language'
	 
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
	 
	#--------------- CREATE THE HIT -------------------
	 
	resultSet = mtc.create_hit(questions=question_form,
	               max_assignments=1,
	               title=title,
	               description=description,
	               keywords=keywords,
	               duration = 60*5,
	               reward=0.05)

	for hit in resultSet:
		print hit.HITId

	

 
ACCESS_ID ='***REMOVED***'
SECRET_KEY = '***REMOVED***'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
to_trans = raw_input('Input text to translate: ')

#do magin nltk stuff to find sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = tokenizer.tokenize(to_trans)

for sentence in sentences:
	createHIT1(sentence)


