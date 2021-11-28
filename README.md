# Auto-gmail-draft-pdf-attatching
## This script does the follows:
- retrieve the most recent pdf file from a specified windows folder: you can change the path in the script
- rename it to "date - name" : today's date and a variable name that you could modify
- move it to a different folder, which you could also specify
- prepare a draft email (gmail) - via the gmail API
- the mail structure is : subject: test x, mail text: test y
- add the downloaded pdf as an attachment to the email
- the email remains a draft for you to review before sending
- you can also unhash a line in the code to make it send the email
### Please make sure you enable gmail API and create credentials and download the credential json file. you will find detailed explanation in the code. you may be asked to give access to the script through the browser only at the first run.
### Also make sure to pip install any missing modules. 
