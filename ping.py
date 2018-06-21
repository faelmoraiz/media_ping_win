# coding: utf-8
import subprocess, time, os

os.system('cls')
ip=str(input('IP: '))
lst=[]

try:
	r=open(ip+'.txt', 'r')
	for x in r:
		x=x.strip()
		lst.append(int(x))
except:
	pass

while 1:
	with open(ip+'.txt', 'a') as f:
		a=str(subprocess.Popen('ping -n 1 '+ip, stdout=subprocess.PIPE ).communicate()[0]).split('tempo=')[1].split('ms')[0]
		f.write(str(float(a))+'\n')
		lst.append(float(a))
	time.sleep(1)
	os.system('cls')
	print('Ping: {:.2f}ms'.format(float(a)))
	print('Média: {:.2f}ms'.format(sum(lst)/len(lst)))
	print('Dados:', str(len(lst)))
