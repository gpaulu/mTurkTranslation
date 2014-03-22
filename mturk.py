from boto.mturk.connection import MTurkConnection
 
ACCESS_ID ='***REMOVED***'
SECRET_KEY = '***REMOVED***'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
print mtc.get_account_balance()