from flask import Flask,request,render_template,redirect,Response
p=Flask(__name__)
@p.route('/')
def w():
 return render_template('index.html')
def v():
 p.v(host='0.0.0.0',port=3456)
if __name__=='__main__':
 v()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

