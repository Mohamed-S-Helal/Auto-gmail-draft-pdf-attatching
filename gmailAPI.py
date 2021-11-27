import os
from datetime import datetime
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders as encoder
import mimetypes
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# this is the path of the folder containing the files you can change
old_folder = '.\\' 

# this is the credentials file you must download from your account and name it 'credentials.json' and put it in the same folder as the script file and 
credentials_file = 'credentials.json'

# this is the path of the folder you can change
new_folder = '.\\folder' 

# this is the part of the name you can change    
test = 'testName'

# this is the sender email (your email) you can change
sender_email = 'mohamed.salah.pet@gmail.com'
# this is the reciever email you can change       
receiver_email = 'mohsalhel@gmail.com'
# this is the email title you can change        
email_title = 'this is the subject line'        

# this is the email body message you can change
email_body = '''
This is the message body
You can even write multiple lines :)
'''     

date = str(datetime.date(datetime.now()))
new_file = os.path.join(new_folder, date+'-'+test+'.pdf')

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, file) for file in files if file.endswith('.pdf')]
    return max(paths, key=os.path.getctime)

old_file = os.path.join(old_folder, newest(old_folder))

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, 
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id,
                body=message).execute()

        print('Message Id: {}'.format(message['id']))

        return message
    except Exception as e:
        print('An error occurred: {}'.format(e))
        return None
    
def create_draft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()
    return draft

  except :
    return None


def create_message_with_attachment(sender,to,subject,message_text,file):
    
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject 
    message.attach(MIMEText(message_text, 'plain'))

    (content_type, encoding) = mimetypes.guess_type(file)
    (main_type, sub_type) = content_type.split('/', 1)
    filename = os.path.basename(file)
    
    with open(file, 'rb') as f:
        myf = MIMEBase(main_type, sub_type)
        myf.set_payload(f.read())
        myf.add_header('Content-Disposition', 'attachment', filename=filename)
        encoder.encode_base64(myf)

    message.attach(myf)

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw_message.decode()}


if __name__ == "__main__":
    os.rename(old_file, new_file)
    service = get_service()
    user_id = 'me'
    msg = create_message_with_attachment(sender_email, receiver_email, email_title, email_body, new_file)
    create_draft(service, user_id, msg)
