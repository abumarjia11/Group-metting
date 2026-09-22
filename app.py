from flask import Flask, request, session, redirect
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.secret_key = "mysecretkey123"
socketio = SocketIO(app, cors_allowed_origins="*")

users = {"admin": {"pass": "admin123", "approved": True}}

LOGIN_PAGE = """
<h2>লগইন / রেজিস্ট্রেশন</h2>
<form action='/register' method='post'>
<input name='name' placeholder='নাম'><br><br>
<input name='password' type='password' placeholder='পাসওয়ার্ড'><br><br>
<button>রেজিস্ট্রেশন করুন</button>
</form><hr>
<form action='/login' method='post'>
<input name='name' placeholder='নাম'><br><br>
<input name='password' type='password' placeholder='পাসওয়ার্ড'><br><br>
<button>লগইন করুন</button>
</form>
"""

CHAT_PAGE = """
<h3>স্বাগতম {user} ভাই</h3><div id='chat'></div>
<input id='m' placeholder='মেসেজ লিখুন'><button onclick='send()'>Send</button>
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script>
var socket = io();
function send(){socket.emit('message', {msg: document.getElementById('m').value}); document.getElementById('m').value='';}
socket.on('message', function(d){document.getElementById('chat').innerHTML += "<p><b>"+d.user+":</b> "+d.msg+"</p>";});
</script>
"""

@app.route('/')
def home():
    if 'user' in session:
        return CHAT_PAGE.format(user=session['user'])
    return LOGIN_PAGE

@app.route('/register', methods=['POST'])
def reg():
    n=request.form['name']; p=request.form['password']
    if n in users: return "এই নামে আছে"
    users[n]={"pass":p,"approved":False}
    return "রেজিস্ট্রেশন হয়েছে, এডমিন এপ্রুভ করলে ঢুকতে পারবেন। <a href='/'>Back</a>"

@app.route('/login', methods=['POST'])
def log():
    n=request.form['name']; p=request.form['password']
    if n not in users or users[n]['pass']!=p: return "ভুল পাসওয়ার্ড"
    if not users[n]['approved']: return "ERROR: এডমিন এখনো অনুমোদন দেয়নি!"
    session['user']=n
    return redirect('/')

@app.route('/admin')
def admin():
    pending=[u for u,d in users.items() if not d['approved']]
    return f"Pending: {pending}<br><form action='/approve' method='post'><input name='name'><button>Approve</button></form>"

@app.route('/approve', methods=['POST'])
def approve():
    n=request.form['name']
    if n in users: users[n]['approved']=True
    return f"{n} Approved <a href='/admin'>Back</a>"

@socketio.on('message')
def msg(data):
    socketio.emit('message', {'user':session['user'], 'msg':data['msg']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
