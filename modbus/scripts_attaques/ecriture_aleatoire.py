#! /usr/bin/python3

'''
Fichier : ecriture_aleatoire.py
Description : Écriture de valeurs générées aléatoirement sur les registres du serveur Modbus
Version : 1
'''

__auteur__ = 'jd'

import collections, random, sys
from pymodbus.client.sync import ModbusTcpClient

class ModbusException(Exception):
	_codes = {
		1:  'FONCTION ILLÉGALE',
		2:  'ADRESSE DE DONNÉES ILLÉGALE',
		3:  'VALEUR DE DONNÉES ILLÉGALE',
		4:  'ÉCHEC DU DISPOSITIF ESCLAVE',
		6:  'DISPOSITIF ESCLAVE OCCUPÉ'
	}

	def __init__(self, code):
		self.code = code
		self.message = ModbusException._codes[code] if ModbusException._codes.has_key(code) else 'Exception Modbus Inconnue'

	def __str__(self):
		return 'Erreur Modbus. Exception %d : %s' % (self.code, self.message)

def status(msg):
	sys.stderr.write(msg[:-1][:39].ljust(39,' ')+msg[-1:])

def connexion():
	try:
		# définition des variables global
		global c_normal, c_vert, ip, port, adr_debut, adr_fin, unitid, client
		
		# définition de couleurs pour l'esthétique
		c_normal = '\033[0m'
		c_vert = '\033[32m'

		# déclaration des variables
		ip = '127.0.0.1'
		port = 502
		adr_debut = 1
		adr_fin = 1000
		unitid = 1

	except IndexError:
		print('ERREUR : Pas de cible\n\n')
		exit()

	print('Connexion au PLC %s... ' % ip, end='')

	# connexion au serveur Modbus
	client = ModbusTcpClient(ip, port)
	client.connect()
	if client.socket == None:
		print('\n\nERREUR : Connexion impossible sur le PLC ayant pour adresse ip %s' %ip)
		exit()
	print(' Connecté.')

# fonction qui va écrire des valeurs aléatoires dans les registres
def ecriture_aleatoire():
	resultats = []
	adresse = 1
	for adresse in range(adr_debut, adr_fin):
		gen_aleatoire = random.randint(1337, 9999)
		ecriture_registre = client.write_registers(adresse, gen_aleatoire, unit=unitid)
		if ecriture_registre.function_code == 16:
			resultats.append(adresse)

	client.close()
	print('\nÉcriture dans les registres finie (%d adresses ont été essayées).' % (adr_fin-adr_debut+1))
	print("\nL'écriture a réussie sur ces %d adresses : " % len(resultats))
	print('\t'+c_vert+'[*]  '+c_normal+str(resultats))

# fonction qui va lire les registres
def lecture_registres():
	resultats = {}
	adresse = 1
	registres_teste = adr_fin - adr_debut + 1
	if registres_teste == 1:
		ecriture_registre = client.read_holding_registers(adr_debut, 1, unit=unitid)
		if ecriture_registre.function_code == 3:
			resultats[adresse] = ecriture_registre.registres[0]
	else:
		for adresse in range(adr_debut, adr_fin):
			ecriture_registre = client.read_holding_registers(adresse, 1, unit=unitid)
			if ecriture_registre.function_code == 3:
				resultats[adresse] = ecriture_registre.registers[0]

	client.close()
	print('\n\nLa lecture des registres est finie (%d registres ont été essayées) :\n' % (registres_teste))

	# rangement du dictionnaire avant affichage
	resultats_ranges = collections.OrderedDict(sorted(resultats.items()))
	for adresse, valeur in resultats_ranges.items():
		print('\t'+c_vert+'[*]'+c_normal+'  Valeur du registre {0} : {1}'.format(adresse,valeur))

if __name__=='__main__':
	try:
		connexion()
		ecriture_aleatoire()
		lecture_registres()
	except KeyboardInterrupt:
		status('Vous avez appuyé sur Ctrl-C\n')