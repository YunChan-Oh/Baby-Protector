from distutils.log import info
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
auth=firebase.auth()

email="learndatascienceskill@gmail.com"
password="123456"
#auth.create_user_with_email_and_password(email,password)

user= auth.sign_in_with_email_and_password(email, password)
#print(user)
#print(user['idToken'])

info= auth.get_account_info(user['idToken'])
#print(info)

#auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)