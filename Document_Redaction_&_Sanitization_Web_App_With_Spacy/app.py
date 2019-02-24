from flask import Flask,url_for,render_template,request,send_file,redirect
from flask_uploads import UploadSet,configure_uploads,ALL,DATA
from werkzeug import secure_filename

# Other Packages
import os
import spacy
nlp = spacy.load('en')

import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Initialize App
app = Flask(__name__)
# Configuration For Uploads
files = UploadSet('files',ALL)
app.config['UPLOADED_FILES_DEST'] = 'static/uploadedfiles'
configure_uploads(app,files)

# Functions to Sanitize and Redact 
def sanitize_names(text):
    docx = nlp(text)
    redacted_sentences = []
    for ent in docx.ents:
        ent.merge()
    for token in docx:
        if token.ent_type_ == 'PERSON':
            redacted_sentences.append("[REDACTED NAME]")
        else:
            redacted_sentences.append(token.string)
    return "".join(redacted_sentences)

def sanitize_places(text):
    docx = nlp(text)
    redacted_sentences = []
    for ent in docx.ents:
        ent.merge()
    for token in docx:
        if token.ent_type_ == 'GPE':
            redacted_sentences.append("[REDACTED PLACE]")
        else:
            redacted_sentences.append(token.string)
    return "".join(redacted_sentences)

def sanitize_date(text):
    docx = nlp(text)
    redacted_sentences = []
    for ent in docx.ents:
        ent.merge()
    for token in docx:
        if token.ent_type_ == 'DATE':
            redacted_sentences.append("[REDACTED DATE]")
        else:
            redacted_sentences.append(token.string)
    return "".join(redacted_sentences)

def sanitize_org(text):
    docx = nlp(text)
    redacted_sentences = []
    for ent in docx.ents:
        ent.merge()
    for token in docx:
        if token.ent_type_ == 'ORG':
            redacted_sentences.append("[REDACTED]")
        else:
            redacted_sentences.append(token.string)
    return "".join(redacted_sentences)

def writetofile(text):
	file_name = 'yourdocument' + timestr + '.txt'
	with open(os.path.join('static/downloadfiles',file_name),'w') as f:
		f.write(text)

		
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/sanitize',methods=['GET','POST'])
def sanitize():
	if request.method == 'POST':
		choice = request.form['taskoption']
		rawtext = request.form['rawtext']
		if choice == 'redact_names':
			result = sanitize_names(rawtext)
		elif choice == 'places':
			result = sanitize_places(rawtext)
		elif choice == 'date':
			result = sanitize_date(rawtext)
		elif choice == 'org':
			result = sanitize_org(rawtext)
		else:
			result = sanitize_names(rawtext)
	return render_template('index.html',rawtext=rawtext,result=result)


@app.route('/uploads',methods=['GET','POST'])
def uploads():
	if request.method == 'POST' and 'txt_data' in request.files:
		file = request.files['txt_data']
		choice = request.form['saveoption']
		filename = secure_filename(file.filename)
		file.save(os.path.join('static/uploadedfiles',filename))

		# Document Redaction Here
		with open(os.path.join('static/uploadedfiles',filename),'r+') as f:
			myfile = f.read()
			result = sanitize_names(myfile)
		if choice == 'savetotxt':
			new_res = writetofile(result)
			return redirect(url_for('downloads'))
		elif choice == 'no_save':
			pass
		else:
			pass

		


	return render_template('result.html',filename=filename,result=result,myfile=myfile)

@app.route('/downloads')
def downloads():
	files = os.listdir(os.path.join('static/downloadfiles'))
	return render_template('downloadsdirectory.html',files=files)

if __name__ == '__main__':
	app.run(debug=True)