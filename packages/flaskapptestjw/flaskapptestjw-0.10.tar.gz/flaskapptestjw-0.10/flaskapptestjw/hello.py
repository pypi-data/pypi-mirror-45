from flask import Flask,request,render_template,redirect,Response
m=Flask(__name__)
@m.route('/')
def X():
 return render_template('index.html')
def l():
 m.run(host='0.0.0.0',port=3456)
if __name__=='__main__':
 l()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

