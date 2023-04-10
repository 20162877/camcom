import requests
import time   

def login(ENDPOINT, data):
    
    # sending post request
    r = requests.post(url = ENDPOINT+'login', json=data)
    print(f"USER :{data['username']} JUST LOGGED IN")


def logout(ENDPOINT, data):
    r = requests.post(url = ENDPOINT+'logout', json=data)    
    print(f"USER :{data['username']} JUST LOGGED OUT")
    

if __name__=='__main__':
    # defining the api-endpoint 
    ENDPOINT = "http://127.0.0.1:5000/" 
    users = ['mohan','syam','mohd','ram','zaid']
    pwds = ['mohan@123','syam@123','mohd@123','ram@123','zaid@123']
    
    # r = requests.get(ENDPOINT+'job')
    # print(r.text)
    
    # Number of user wants to login with given list : Hard Coded 4
    for i in range(4):                    
        login(ENDPOINT,{'username':users[i],'password':pwds[i]})
        time.sleep(10)
    
    time.sleep(20)
    # Number of user wants to login with given list : Hard Coded 4 
    # Note: Considering user is logged in and irrespective of assigned task
    for i in range(4):        
        logout(ENDPOINT,{'username':users[i]})
        time.sleep(3)                        
