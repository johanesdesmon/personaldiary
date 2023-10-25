from flask import Flask, render_template,jsonify,request 

from pymongo import MongoClient

from datetime import datetime
import certifi
ca = certifi.where()


client = MongoClient('mongodb+srv://ncc1477:Qwedsa123!@cluster0.kkwb2cl.mongodb.net', tlsCAFile=ca)

db = client.ncc1477


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles':articles})

@app.route('/diary',methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    time = today.strftime('%Y.%m.%d')




    doc = {
        'file' : filename,
        'profile' : profilename,
        'title' : title_receive,
        'content' : content_receive,
        'time' : time
    }
    db.diary.insert_one(doc)
    return jsonify ({'msg' : 'data saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
