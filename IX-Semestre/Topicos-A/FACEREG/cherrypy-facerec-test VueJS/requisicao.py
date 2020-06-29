# importing the requests library 
import requests 

def acesso(opcao):
    # defining a params dict for the parameters to be sent to the API 
    URL = "http://192.168.1.4/"+str(opcao)
    # sending get request and saving the response as response object 
    r = requests.get(url = URL) 
    print(r)