import pyrebase

config={
    "apiKey": "AIzaSyAJInw2Ra5LdtIurVfPteq--ROFVNtZ85g",
    "authDomain": "baby-protector.firebaseapp.com",
    "databaseURL" : "https://www.gstatic.com/firebasejs/9.9.2/firebase-app.js",
    "projectId": "baby-protector",
    "storageBucket": "baby-protector.appspot.com",
    "messagingSenderId": "553047008472",
    "appId": "1:553047008472:web:568c9f71e00220ac66a3ad"
}
firebase=pyrebase.initialize_app(config)
storage= firebase.storage()
my_image="output/image1.png"

storage.child(my_image).put(my_image)

auth= firebase.auth()
email="learndatascienceskill@gmail.com"
password="123456"
user=auth.sign_in_with_email_and_password(email,password)
url=storage.child(my_image).get_url(user['idToken'])
print(url)