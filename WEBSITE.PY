import random, threading, webbrowser
from flask.json import jsonify
from flask import Flask, request,render_template
import re, os, time

app=Flask(__name__)
def search(regex_compiled, base_dir):
    for filename in os.listdir(base_dir):
        completeFile = os.path.join(base_dir,filename)
        if not os.path.isfile(completeFile):
            #Recursive Searches in multiple directories
            search(regex_compiled,completeFile)

        try:
            with open(completeFile) as eachFile:
                content = eachFile.read()
                #Search in an individual File
                match =regex_compiled.search(content)
                if match is not None:
                    #if Match found write the output in a temporary file
                    file1 = open("matchFound.txt","a+")
                    snippet=match.group()
                    print(snippet)
                    file1.write("<tr><td>"+completeFile+"</td><td></td><td>\""+match.group(0)+"\"</td></tr>")
        #ALlow the exceptions for persmission as it tries to open a directory as a file
        except (PermissionError, UnicodeDecodeError) as e:
            #print("Excetion occured is :",e)   #Check Exception
            pass

@app.route('/')
def my_form():
    #Take the path and keyword from the file in myform.html
    return render_template('myform.html')

@app.route('/', methods=['POST'])
def home():
    path= request.form['path']
    word = request.form['word']
    word = "(.*?)"+word+"(.*?)"
    #for Case Insensitive search results
    regex_compiled= re.compile(word)#,re.IGNORECASE)
    start_time = time.time()
    file1= open("matchFound.txt","w")
    file1.write("<tr><th>Path of the File</th><th>Code Snippet</th></tr>")
    file1.close()
    search(regex_compiled,path)
    file1 = open("matchFound.txt", 'r+')
    content = file1.read()
    file1.close()
    os.remove("matchFound.txt")
    return "<html><body><table>"+content+"</table></body></html>"


if __name__=="__main__":
    port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
    app.run(port=port,debug=False)
