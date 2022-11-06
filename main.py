from flask import Flask,request
from flask import render_template
from werkzeug.utils import secure_filename

import PyPDF2 
import os
import re
#from typing_extensions import TypeVarTuple
import time

import os
from time import time,sleep

from RecursiveSummarize import Summarize
from twilio.rest import Client
#from summarizer.sbert import SBertSummarizer
from pprint import pprint





app = Flask(__name__)


UPLOAD_FOLDER = os.path.abspath(os.getcwd())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def computeWhatsAppMessage(text,name,Topic ):
    
    account_sid = ""
    auth_token = "" 
    client = Client(account_sid, auth_token)
    Topictext = f"TOPIC: {Topic}"
    nameText = f"Dear,{name}"
    finalText = nameText+'\n\n'+Topictext + "\n\n" +text
    
    message = client.messages.create( 
                                from_='whatsapp:+14155238886',   
                                body=finalText,      
                                to='whatsapp:+919901934660'
                            ) 
    
    print(message.sid)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()





def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)




def ComputeSMSMessage(text,name,Topic):
    
    #account_sid = 'AC836bb0f81c5a79925addb8d0cb265b73'
    #auth_token = '4e0542b1317d1f73a9601ee2f0459963'

    account_sid = ""
    auth_token = "" 


    client = Client(account_sid, auth_token)
    Topictext = f"TOPIC: {Topic}"
    nameText = f"Dear, {name}"
    finalText = nameText+'\n\n'+Topictext + "\n\n" +text
    message = client.messages.create (
    body=finalText,
    from_="+14699566640",
    to="+919901934660"
     )
    print(message.body)

  


@app.route('/HomePage' ,methods = ["GET","POST"])
def index():

    if (request.method == "GET"):
        return render_template("sah.html")

    else:
        
        

        
        # if 'file' not in request.files:
        #     print("no file")
        #     return render_template("sah.html")

        file = request.files['file']
        name = request.form['name']
        
        email = request.form['email']
        
        no = request.form['no']
        
        Topic = request.form['Topic']
        
        
        
        
        filename = secure_filename(file.filename)
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filePath)
        pdfFileObj = open(filePath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # printing number of pages in pdf file 
        maxPages = pdfReader.numPages

        
        
        
        allData = []
        for page in range(maxPages):
            
            pageObj = pdfReader.getPage(page)
            text = pageObj.extractText()
            text = text.replace("\n","")
            text = text.split('.')
            text = [re.sub('[^A-Za-z0-9]+', ' ', sent) for sent in text]
            text = ". ".join([sent.strip() for sent in text])
            allData.append(text)
            
        text = "".join(allData)
        summarized = Summarize(text)
        if request.form.get('SMS'):
            ComputeSMSMessage(summarized,name,Topic)
        if request.form.get('w'):
            computeWhatsAppMessage(summarized,name,Topic)
        return render_template("sah.html")



@app.route('/GetAnswer' ,methods = ["GET","POST"])
def getAnswer():
    return

if __name__ == "__main__":
    app.run(debug = True)
