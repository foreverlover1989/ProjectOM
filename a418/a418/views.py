from django.shortcuts import render
import paramiko
def index(request):
	ip = '47.100.214.209'
	user = 'root'
	pawd = 'gsy19970628.'
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=ip,username=user,password=pawd,port=22)
	stdin,stdout,stderr = ssh.exec_command('uname')
	result = stdout.read().decode()
	content = {'result':result}
	return render(request,'index.html',content)