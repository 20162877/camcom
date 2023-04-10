from flask import Flask, jsonify, request, session
import psycopg2
import psycopg2.extras
import threading
import time

DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'postgres'
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

app = Flask(__name__)
app.config["SECRET_KEY"] = "adfadfewere-asdfaf"
LOGGED_IN_USER = set()
LOGGED_IN_FREE_USER = {}
USER_TASK = {}

def executing_task(user):
    time.sleep(3)
    del USER_TASK[user]
    if user in LOGGED_IN_USER:        
        LOGGED_IN_FREE_USER[user]=True    
    print(f'{user} has finished his task')

@app.route('/task_assign', methods=['GET'])
def task_assign():            
    for user in LOGGED_IN_USER:
        print(LOGGED_IN_FREE_USER)
        print(f'Task assigned to user: {user}')
        if LOGGED_IN_FREE_USER[user] == True:            
            USER_TASK[user]=3
            LOGGED_IN_FREE_USER[user]=False
            threading.Thread(target=executing_task, args=(user,)).start()
        print(LOGGED_IN_FREE_USER)
    
    return jsonify({"task":"assigned task"})


@app.route('/login', methods=['POST'])
def login():    
    
    _json = request.json    
    username = _json['username']
    password = _json['password']    
    if username and password:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from public.flask_user where username=%s"
        sql_where = (username,)        
        cursor.execute(sql, sql_where)        
        row = cursor.fetchone()
        
        
        if row:            
            db_username = row['username']
            db_password = row['password']            
            if db_username == username and password == db_password :
                session['username'] = username
                LOGGED_IN_USER.add(username)
                LOGGED_IN_FREE_USER[username] = True
                cursor.close()
            resp = jsonify({'message':"you are logged in successfully"})
            resp.status_code = 200
            return resp
    else:
        resp = jsonify({"message":"bad request invalid user name or password"})
        resp.status_code = 400
        return resp
        
    return "done"

@app.route('/logout', methods=['POST'])
def logout():       
    _json = request.json
    username = _json['username']
           
    if username:                
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select * from public.flask_user where username=%s"
        sql_where = (username,)        
        cursor.execute(sql, sql_where)        
        row = cursor.fetchone()
        print(username)
        if row['username'] == username:
            session['username'] = None  
            if username in LOGGED_IN_USER:                   
                LOGGED_IN_USER.remove(username)
                del LOGGED_IN_FREE_USER[username]      
                return jsonify({'user':'user_logged_out'})
            return jsonify({'user':'user already logged_out'})
            

if __name__ == '__main__':    
    app.run(debug=True)    
    