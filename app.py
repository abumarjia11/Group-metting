from flask import Flask, request, session, redirect
app = Flask(__name__)
app.secret_key = "123"
users = {"admin": {"pass": "admin123", "approved": True}}

@app.route('/')
def home():
    if 'user' in session:
        return f"<h3>Hi {session['user']}</h3><p>Login Success! Chat feature next step e add korbo.</p><a href='/admin'>Admin Panel</a>"
    return """
    <h2>Group Login</h2>
    <form action='/register' method='post'><input name='name' placeholder='Name'><input name='password' placeholder='Pass'><button>Register</button></form>
    <form action='/login' method='post'><input name='name' placeholder='Name'><input name='password' placeholder='Pass'><button>Login</button></form>
    """

@app.route('/register', methods=['POST'])
def reg():
    n=request.form['name']; p=request.form['password']
    users[n]={"pass":p,"approved":False}
    return "Wait for admin approve. <a href='/'>Back</a>"

@app.route('/login', methods=['POST'])
def log():
    n=request.form['name']; p=request.form['password']
    if n not in users or users[n]['pass']!=p: return "Wrong pass"
    if not users[n]['approved']: return "ERROR: Admin not approved"
    session['user']=n
    return redirect('/')

@app.route('/admin')
def admin():
    pending = [u for u,d in users.items() if not d['approved']]
    return f"Pending: {pending}<br><form action='/approve' method='post'><input name='name'><button>Approve</button></form>"

@app.route('/approve', methods=['POST'])
def approve():
    n=request.form['name']
    if n in users: users[n]['approved']=True
    return f"{n} approved"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
