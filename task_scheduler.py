import requests
import time 


if __name__=='__main__':
    # defining the api-endpoint 
    ENDPOINT = "http://127.0.0.1:5000/" 
    # users = ['mohan','syam','mohd','ram','zaid']
    # pwds = ['mohan@123','syam@123','mohd@123','ram@123','zaid@123']
    while True:
        
        r = requests.get(ENDPOINT+'task_assign')
        print(r.text)        
        time.sleep(1)
        
    