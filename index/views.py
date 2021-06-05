from django.shortcuts import render
import pyrebase
from django.contrib import auth

# Create your views here.
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
json = ""

def main(request):
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
    


def status(request):
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
    
    return render(request,'pages/tables.html',{"finalList":smoke_data})

def postuser(request):
    
    c = request.GET.get('z')
    global json
    json = c
    gyro_x = database.child("upload").child(str(c)).child("gyro").child("x").get().val()
    gyro_y = database.child("upload").child(str(c)).child("gyro").child("y").get().val()
    gyro_z = database.child("upload").child(str(c)).child("gyro").child("z").get().val()

    pressure  = database.child("upload").child(str(c)).child("pressure").child("pressure").get().val()
    temp  = database.child("upload").child(str(c)).child("pressure").child("temperature").get().val()
    alti  = database.child("upload").child(str(c)).child("pressure").child("altitude").get().val()
    humidity  = database.child("upload").child(str(c)).child("pressure").child("humidity").get().val()

    pulse = database.child("upload").child(str(c)).child("heart beat").child("rate").get().val()

    smoke = database.child("upload").child(str(c)).child("smoke").child("conc").get().val()

    name = database.child("upload").child(str(c)).child("name").get().val()

    if float(smoke) >= 400.0:
        cond = "High Smoke"
    elif float(pulse) < 60.0:
        cond = "Low Pulse Rate"
    else: 
        cond = "Normal"

    p = float(pulse)
    if p<60:
        line_pulse = 60
    elif p>=75 and p<=95:
        line_pulse=10
    elif p>95 and p<=115:
        line_pulse=20
    elif p>115 and p<=135:
        line_pulse=30
    elif p>135 and p<=155:
        line_pulse=40
    else:
        line_pulse=80

    t = float(temp)
    if t<10:line_temp = 90
    elif t>10 and t<20:line_temp = 70
    elif t>20 and t<28:line_temp = 50
    elif t>28 and t<32:line_temp = 20
    elif t>32 and t<38:line_temp = 10
    elif t>38 and t<70:line_temp = 65
    else:line_temp = 90


    s = float(smoke)
    if s<10:line_s = 0
    elif s<400:line_s = 10
    elif s>400 and s<600:line_s = 40
    elif s>600 and s<800:line_s = 60
    else:line_s = 80
        
    data = {"x":gyro_x , "y":gyro_y , "z":gyro_z , "user":c , 
            "pr":pressure , "temp":temp , "altitude":alti , 
            "humidity":humidity , "smoke":smoke , "heart":pulse,"cond":cond, "name":name, "line_pulse":line_pulse, "line_temp":line_temp, "line_s":line_s}

    return render(request,'pages/profile.html',data)

def alert(request):
    
    database.child("upload").child(str(json)).child('alert').set(1)

    c = json
    gyro_x = database.child("upload").child(str(c)).child("gyro").child("x").get().val()
    gyro_y = database.child("upload").child(str(c)).child("gyro").child("y").get().val()
    gyro_z = database.child("upload").child(str(c)).child("gyro").child("z").get().val()

    pressure  = database.child("upload").child(str(c)).child("pressure").child("pressure").get().val()
    temp  = database.child("upload").child(str(c)).child("pressure").child("temperature").get().val()
    alti  = database.child("upload").child(str(c)).child("pressure").child("altitude").get().val()
    humidity  = database.child("upload").child(str(c)).child("pressure").child("humidity").get().val()

    pulse = database.child("upload").child(str(c)).child("heart beat").child("rate").get().val()

    smoke = database.child("upload").child(str(c)).child("smoke").child("conc").get().val()

    name = database.child("upload").child(str(c)).child("name").get().val()

    if float(smoke) >= 400.0:
        cond = "High Smoke"
    elif float(pulse) < 60.0:
        cond = "Low Pulse Rate"
    else: 
        cond = "Normal"
        
    message = "Alert Sent!!!"

    
    p = float(pulse)
    if p<60:
        line_pulse = 60
    elif p>=75 and p<=95:
        line_pulse=10
    elif p>95 and p<=115:
        line_pulse=20
    elif p>115 and p<=135:
        line_pulse=30
    elif p>135 and p<=155:
        line_pulse=40
    else:
        line_pulse=80

    t = float(temp)
    if t<10:line_temp = 90
    elif t>10 and t<20:line_temp = 70
    elif t>20 and t<28:line_temp = 50
    elif t>28 and t<32:line_temp = 20
    elif t>32 and t<38:line_temp = 10
    elif t>38 and t<70:line_temp = 65
    else:line_temp = 90

    s = float(smoke)
    if s<400:line_s = 10
    elif s>400 and s<600:line_s = 40
    elif s>600 and s<800:line_s = 60
    else:line_s = 80
    
    data = {"x":gyro_x , "y":gyro_y , "z":gyro_z , "user":c , 
            "pr":pressure , "temp":temp , "altitude":alti , 
            "humidity":humidity , "smoke":smoke , "heart":pulse,"cond":cond, "name":name, "msg":message, "line_s":line_s, "line_pulse":line_pulse, "line_temp":line_temp}

    

    return render(request,'pages/profile.html',data)