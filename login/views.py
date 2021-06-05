from django.shortcuts import render
import pyrebase
from django.contrib import auth
"""
config = {
    'apiKey': "AIzaSyAnVF25jIKjpU_beBQk6OwP_9wXG1cWhaU",
    'authDomain': "miniproject-e3e80.firebaseapp.com",
    'projectId': "miniproject-e3e80",
    'databaseURL': "https://miniproject-e3e80-default-rtdb.firebaseio.com/",
    'storageBucket': "miniproject-e3e80.appspot.com",
    'messagingSenderId': "221808349120",
    'appId': "1:221808349120:web:01974c56122bcc54798225",
    'measurementId': "G-B4ZNJ2ZTP9"
}
"""
config = {
    'apiKey': "AIzaSyBLeV-23dCRZkogp0H80LRrPLOHw9G42w0",
    'authDomain': "nodemcu-6c3f8.firebaseapp.com",
    'databaseURL': "https://nodemcu-6c3f8-default-rtdb.firebaseio.com",
    'projectId': "nodemcu-6c3f8",
    'storageBucket': "nodemcu-6c3f8.appspot.com",
    'messagingSenderId': "921174287550",
    'appId': "1:921174287550:web:c3beb2e83f13f60e132aef",
    'measurementId': "G-B97KTKRPPE"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request,"pages/login.html")


def postsignIn(request):

   
        email = request.POST.get('email')
        passw = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email,passw)
        except:
            message = "Invalid Credentials"
            return render(request,"pages/login.html",{"msg":message})
        
        session_id = user['idToken']
        request.session['uid']=str(session_id)

        a = database.child("upload").shallow().get().val()
    
        l = []
        smoke_data = []
        for i in a:
            l.append(i)
        for i in l:
            name = database.child("upload").child(i).child("name").get().val()
            s = database.child("upload").child(i).child("smoke").child("conc").get().val()

            p = database.child("upload").child(i).child("heart beat").child("rate").get().val()
            if float(s) >= 400.0:
                smoke_data.append([name,i,"High Smoke"])
            elif float(p) < 60.0:
                smoke_data.append([name,i,"Low Pulse Rate"])
            else: 
                smoke_data.append([name,i,"Normal"])
        
        
        return render(request,"index.html",{"finalList":smoke_data})
    

def logout(request):
    auth.logout(request)
    return render(request,'pages/login.html') 