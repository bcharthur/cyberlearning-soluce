import requests
from bs4 import BeautifulSoup
import base64
import re
import time
import os


# URL de la page à scraper ATTENTION JETON A CHANGER EN FONCTION DE LA SESSION
url = 'https://cyber-learning.fr/cyber-challenge/programmation/b64/sujet.php?jeton=U3hP680ou318'


# Dossier de téléchargement pour les fichiers
download_folder = 'downloads'
os.makedirs(download_folder, exist_ok=True)  # Créer le dossier s'il n'existe pas


# Créer une session pour conserver les cookies et autres informations de session
session = requests.Session()


def extract_code_between_brackets(text):
   # Utilise une expression régulière pour extraire le texte entre crochets []
   match = re.search(r'\[(.*?)\]', text)
   if match:
       return match.group(1)
   else:
       return 'Code non trouvé'


while True:
   start_time = time.time()


   try:
       # Récupérer le contenu de la page
       response = session.get(url)
       response.raise_for_status()  # Vérifie si la requête a réussi
       soup = BeautifulSoup(response.text, 'html.parser')


       # Rechercher la chaîne de caractères en base64 dans le texte brut de la page
       base64_pattern = re.compile(r'Décodez : RkxBRyA9([A-Za-z0-9+/=]+)')
       match = base64_pattern.search(response.text)


       if match:
           base64_string = match.group(1)
       else:
           raise ValueError("La chaîne de caractères en base64 n'a pas été trouvée.")


       # Décoder la chaîne de caractères en base64
       decoded_bytes = base64.b64decode(base64_string)
       decoded_string = decoded_bytes.decode('utf-8')


       # Préparer les données pour le formulaire
       form_data = {
           'resultat': decoded_string
       }


       # Soumettre le formulaire
       response = session.post(url, data=form_data)
       response.raise_for_status()  # Vérifie si la requête a réussi


       # Vérifier si le message "BRAVO" est présent dans la réponse
       if "BRAVO" in response.text:
           print("Formulaire soumis avec succès.")
           # Extraire le texte entre crochets []
           code_obtenu = extract_code_between_brackets(response.text)
           print(f"Code obtenu : {code_obtenu}")


           # Vérifier s'il y a un lien vers une image dans la page
           soup = BeautifulSoup(response.text, 'html.parser')
           img_tag = soup.find('img', src=True)
           if img_tag:
               img_url = img_tag['src']
               img_filename = os.path.join(download_folder, os.path.basename(img_url))
               img_response = requests.get(img_url)
               img_response.raise_for_status()  # Vérifie si le téléchargement de l'image a réussi
               with open(img_filename, 'wb') as f:
                   f.write(img_response.content)
               print(f"Image téléchargée avec succès : {img_filename}")
           else:
               print("Aucune image trouvée à télécharger.")
       else:
           print("Échec de l'affichage du code obtenu.")


   except requests.RequestException as e:
       print(f"Erreur lors de la requête HTTP : {e}")


   except (ValueError, base64.binascii.Error) as e:
       print(f"Erreur lors du traitement des données : {e}")


   except Exception as e:
       print(f"Erreur inattendue : {e}")


   finally:
       # Pause pour respecter les limites de temps et éviter de surcharger le serveur
       time_elapsed = time.time() - start_time
       if time_elapsed < 1.5:  # Ajustez ce délai si nécessaire
           time.sleep(1.5 - time_elapsed)


       # Pause avant la prochaine itération (ajustez la durée selon vos besoins)
       time.sleep(0.5)
