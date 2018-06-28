# coding: utf-8
import subprocess, time, os, getpass, smtplib

os.system('cls')

pingAlto = 100 # Tempo máximo de resposta / Alerta por e-mail.
intervalo = 1 # Intervalo em segundos entre as requisições.
dadosLimite = 30 # limite de armazenamento de dados.

emailOrigem = 'seuemail@gmail.com'
emailDestino = 'destino@email'

def sendmail(toaddr, msg, passwd):
	try:
		relogio='['+time.strftime('%H:%M:%S')+']'
		fromaddr = emailOrigem
		username = fromaddr
		password = passwd
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		content= '\r\n'.join([
				'From: %s' % fromaddr,
				'To: %s' % toaddr,
				'Subject: %s' % msg,
				'',
				'Enviado as %s por ping.py' % relogio
				])
		server.sendmail(fromaddr, toaddr, content)
		print('\nEmail enviado.')
		server.quit()
	except:
		pass

def ping(ip, passwd):
	lst=[];pingsAltos=[]
	try:
		with open(ip.replace('.','_')+'.txt', 'r') as r:
			for x in r:
				x=x.strip()
				lst.append(float(x))
	except Exception as e:
		# print(e)
		pass

	while 1:
		try:
			with open(ip.replace('.','_')+'.txt', 'a') as f:
				a=str(subprocess.Popen('ping -n 1 '+ip, stdout=subprocess.PIPE ).communicate()[0]).split('tempo=')[1].split('ms')[0]
				f.write(str(float(a))+'\n')
				lst.append(float(a))
			time.sleep(intervalo)
			os.system('cls')
			print('\n[@] Endereço:', ip)
			print('\n[!] Ping: {:.2f}ms'.format(float(a)))
			print('[/] Média: {:.2f}ms'.format(sum(lst)/len(lst)))
			print('[#] Dados:', str(len(lst))+'/'+str(dadosLimite))
			with open(ip.replace('.','_')+'.txt', 'r') as r:
				tmp_lst = []
				for x in r:
					x=x.strip()
					tmp_lst.append(float(x))
				print('\n[+] Média geral: {:.2f}\n'.format(sum(tmp_lst)/len(tmp_lst)))
			if (sum(lst)/len(lst))>pingAlto:
				sendmail(emailDestino, '# PING ALTO: {:.2f}ms - [{}]'.format(float(sum(lst)/len(lst)),ip), passwd )
				pingsAltos.append('['+time.strftime('%H:%M:%S')+']'+' -> '+str(float(a))+'ms.')
				lst=[]
				time.sleep(10)
			if len(lst)>=dadosLimite:lst=[]
			if len(pingsAltos)>0:
				for _ping in pingsAltos:
					print('[!]', _ping)
		except Exception as e:
			print('Não foi possível pingar no endereço:', ip)
			print('Erro:', e)
			exit(0)

def main():
	passwd=getpass.getpass('[!] Digite a senha do e-mail: ')
	ip=str(input('\n[@] Endereço do IP: '))
	ping(ip, passwd)

if __name__ == '__main__':
		main()
