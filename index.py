from flask import Flask, request, render_template, flash, jsonify, redirect
import requests
import json
from flask_wtf import Form
from wtforms import validators,StringField, IntegerField,SubmitField, BooleanField
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'development key'

def PilihCapsMon(r,w,x):
    if r == True and w ==True and x == True:
        return "mon", "allow rwx"
    elif r == True and w == True and x == False:
        return "mon", "allow rw"
    elif r == True and w == False and x == True:
        return "mon", "allow rx"
    elif r == True and w == False and x == False:
        return "mon", "allow r"
    elif r == False and w == True and x == True:
        return "mon", "allow wx"
    elif r == False and w == False and x == True:
        return "mon", "allow x"
    elif r == False and w == True and x == False:
        return "mon", "allow w"
    elif r == False and w == False and x == False:
        return None

def PilihCapsOsd(r,w,x):
    if r == True and w ==True and x == True:
        return "osd", "allow rwx"
    elif r == True and w == True and x == False:
        return "osd", "allow rw"
    elif r == True and w == False and x == True:
        return "osd", "allow rx"
    elif r == True and w == False and x == False:
        return "osd", "allow r"
    elif r == False and w == True and x == True:
        return "osd", "allow wx"
    elif r == False and w == False and x == True:
        return "osd", "allow x"
    elif r == False and w == True and x == False:
        return "osd", "allow w"
    elif r == False and w == False and x == False:
        return None 

def PilihCapsMds(r,w,x):
    if r == True and w ==True and x == True:
        return "mds", "allow rwx"
    elif r == True and w == True and x == False:
        return "mds", "allow rw"
    elif r == True and w == False and x == True:
        return "mds", "allow rx"
    elif r == True and w == False and x == False:
        return "mds", "allow r"
    elif r == False and w == True and x == True:
        return "mds", "allow wx"
    elif r == False and w == False and x == True:
        return "mds", "allow x"
    elif r == False and w == True and x == False:
        return "mds", "allow w"
    elif r == False and w == False and x == False:
        return None    

def DefEntity(x,y,z):
    if form.MONr.data ==True or form.MONw.data == True or form.MONx.data==True:
        data = {}

class BuatUser(Form):
    userID = StringField('userID')
    OSDr   = BooleanField('read')
    OSDw   = BooleanField('write')
    OSDx   = BooleanField('execute')
    MONr   = BooleanField('read')
    MONw   = BooleanField('write')
    MONx   = BooleanField('execute')
    MDSr   = BooleanField('read')
    MDSw   = BooleanField('write')
    MDSx   = BooleanField('execute')
    submit = SubmitField()

class BuatVolume(Form):
    poolID = IntegerField('PoolID')
    capacity = IntegerField('capacity')
    submit = SubmitField()

@app.route('/')
def index():
    r = requests.get('http://10.10.6.1:6969/api/v0.1/health.json')
    return render_template('home.html',data =json.loads(r.text))

@app.route('/AddUser')
def adduser():
    r = requests.get('http://10.10.6.1:6969/api/v0.1/auth/list.json')
    return render_template('adduser.html', data =json.loads(r.text))

@app.route('/AddUser/DelUser/<string:entity>', methods = ['GET','PUT'])
def deluser(entity):
    requests.put('http://10.10.6.1:6969/api/v0.1/auth/del', params={"entity":entity})
    return render_template('success.html')

@app.route('/AddUser/form', methods = ['GET','POST','PUT'])
def adduserform():
    form = BuatUser(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('Isi seluruhnya')
            return render_template('form.html', form=form)
        else:
            requests.put('http://10.10.6.1:6969/api/v0.1/auth/get-or-create', 
                params={"entity":"client."+form.userID.data, "caps":[ 
                PilihCapsMon(form.MONr.data,form.MONw.data,form.MONx.data),
                PilihCapsOsd(form.OSDr.data,form.OSDw.data,form.OSDx.data),
                PilihCapsMds(form.MDSr.data,form.MDSw.data,form.MDSx.data)]})
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('form.html', form=form)

@app.route('/AddVolume',methods = ['GET','POST'])
def addvolume():
    req = requests.get('http://10.10.6.1/api/v0.1/osd/pool/ls.json')
    pools = req.output
    r = requests.get('http://10.10.6.1/api/v0.1/osd/pool/stats', params=pools)
    form = BuatVolume(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('Isi seluruhnya')
            return render_template('addvolume.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('addvolume.html', form=form)

@app.route('/LinkUserVolume')
def linkuservolume():
    return render_template('home.html')

@app.route('/latihanjson', methods=['GET'])
def latihanjson():
    r = requests.get('http://10.10.6.1:6969/api/v0.1/auth/list.json')
    return render_template('parsing_json.html',data =json.loads(r.text))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
