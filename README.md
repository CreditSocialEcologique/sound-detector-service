# sound-detector
Tool to detect and prevent sound pollution

Pour installer la version qui utilise le microphone de l'ordinateur :
```bash
sudo apt install python3-pyaudio
pip install sounddevice
python3 fromMicrophone.py
```

Pour utiliser les données d'un arduino, utiliser le script fromArduino.py

L'arduino envoie 0 ou 1 toute les secondes. Cela permet de savoir si on a dépassé le seuil de nuisance sonore (a reglé avec le potentiomètre).
L'application va ensuite lire ce qui a été envoyé et selon ce qu'envoie l'arduino, va faire une requete pour diminuer le score sonore de l'utilisateur.
L'utilisateur est déterminé dans le script vu qu'un appareil correspond à un logement appartenant à un utilisateur.

Si vous n'êtes pas sous linux, il faudra probablement changer le port de l'arduino (COM3 par exemple sous windows)
