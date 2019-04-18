from django.shortcuts import render
from django.http import HttpResponse
import paramiko
import os
import re
# Create your views here.
def index(request):
	mem = []
	config = []
	m = []
	configch = ('核心数','cup型号')
	l = ['id','cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l',
		"cat /proc/cpuinfo | grep 'model name' |uniq",'free -m','hostname','uname -r',
		'cat /etc/redhat-release','df -h']
	if request.method == "POST":
		user = request.POST['user']
		password = request.POST['passwd']
		ip = request.POST['IP']
		# 创建ssh客户端
		ssh = paramiko.SSHClient()
		#允许连接不在know_host中的主机
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		#连接服务器
		ssh.connect(hostname=ip,port=22,username=user,password=password)
		stdin, stdout, stderr = ssh.exec_command('id')
		result = stdout.read().decode()
		resultsplit = result.split(' ')
		if resultsplit[0][4] == '0' and resultsplit[1][4] == '0':
			result1 = '管理员'
		else:
			result1 = '普通用户'

		for i in l:
			if i == 'id':
				#执行命令
				stdin, stdout, stderr = ssh.exec_command('id')
				result = stdout.read().decode()
				resultsplit = result.split(' ')
				if resultsplit[0][4] == '0' and resultsplit[1][4] == '0':
					result1 = '管理员'
				else:
					result1 = '普通用户'
			elif i == l[1]:
				stdin, stdout, stderr = ssh.exec_command(i)
				config.append(stdout.read().decode())
			elif i == l[2]:
				stdin, stdout, stderr = ssh.exec_command(i)
				config.append(stdout.read().decode()[12:])
			elif i == l[3]:
				stdin, stdout, stderr = ssh.exec_command(i)
				mem1 = stdout.read().decode().split(' ')
				for i in mem1:
					if i.isdigit():
						mem.append(i)
				mema = mem[0]
				memb = mem[1]
			elif i == l[4]:
				stdin, stdout, stderr = ssh.exec_command(i)
				Hostname = stdout.read().decode()
			elif i == l[5]:
				stdin, stdout, stderr = ssh.exec_command(i)
				Uname = stdout.read().decode()
			elif i == l[6]:
				stdin, stdout, stderr = ssh.exec_command(i)
				Linux = stdout.read().decode()
			elif i == l[7]:
				stdin, stdout, stderr = ssh.exec_command(i)
				Diskl = stdout.read().decode().split(' ')
				
				for i in Diskl:
					if 'G' in i:
						m.append(i)
					elif 'M' in i:
						m.append(i)
				Diska = m[0]
				Diskb = m[1]

		result2 = dict(zip(configch,config))
		context = {'user':user,'ip':ip,'result':'已登录','result1':result1,'result2':result2,
				'mema':mema,'memb':memb,'hostname':Hostname,'uname':Uname,'linux':Linux,
				'diska':Diska,'diskb':Diskb,'title':'配置信息'}
		return render(request,'index.html',context)
	return render(request,'index.html')