from django.shortcuts import render
import paramiko
# Create your views here.
import requests
def index(requeset):
    if requeset.method == 'POST':
        print(11111111111111111)
        ip =requeset.POST('ip')
        print(11111111111,ip)
        user =requeset.POST('username')
        print(11111111111,user)

        password = requeset.POST('password')
        print(11111111111,password)

        li = paramiko.SSHClient()
        li.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        li.connect(password=password,port=22,hostname=ip,username=user)
        a,b,c = li.exec_command('id')
        id = b.read().decode()
        list_dict ={'id':id}
        li.close()
        return render(requeset,'index.html',list_dict)
    else:
        return render(requeset,'index.html')