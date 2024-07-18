# Base 64 décodage (20 points)
# A vous de jouer et décoder rapidement le message.
#
# Page du challenge : https://cyber-learning.fr/cyber-challenge/programmation/b64/sujet.php?jeton=JETON
#
# Proposition de code par br0nson
# LinkedIn : t.ly/fra3R


import requests  # Pour faire des requêtes HTTP
from bs4 import BeautifulSoup  # Pour parser le HTML
import base64  # Pour décoder les chaînes en base64
import re  # Pour les expressions régulières
import time  # Pour les pauses et la mesure du temps
import os  # Pour les opérations sur les fichiers et dossiers
import sys  # Pour gérer les interruptions du script
from colorama import Fore, Style, init  # Pour la coloration du texte dans la console

# Initialisation de colorama
init(autoreset=True)

# URL de la page à scraper ATTENTION JETON A CHANGER EN FONCTION DE LA SESSION (le jeton fait 12 caractères)
url = 'https://cyber-learning.fr/cyber-challenge/programmation/b64/sujet.php?jeton=JETON'

# Vérification du jeton
if 'jeton=JETON' in url:
    print(f"{Fore.RED}{Style.BRIGHT}Pense à remplacer ton jeton mon grand ;){Style.RESET_ALL}")
    sys.exit(1)

# Dossier de téléchargement pour les fichiers
download_folder = 'downloads'
os.makedirs(download_folder, exist_ok=True)  # Créer le dossier s'il n'existe pas

# Créer une session pour conserver les cookies et autres informations de session
session = requests.Session()

def extract_code_between_brackets(text):
    """
    Utilise une expression régulière pour extraire le texte entre crochets []
    """
    match = re.search(r'\[(.*?)\]', text)
    return match.group(1) if match else 'Code non trouvé'

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("===================================")
    print("  Challenge Base 64 - Décodage")
    print("  Programmation - 20 points")
    print("")
    print("  Présenté par br0nson")
    print("  LinkedIn : t.ly/fra3R ")
    print("===================================")
    print("")

    print(f"{Fore.GREEN}Démarrage du script de scraping...{Style.RESET_ALL}")
    while True:
        start_time = time.time()  # Enregistrer l'heure de début pour mesurer le temps écoulé

        try:
            # Récupérer le contenu de la page
            response = session.get(url)
            response.raise_for_status()  # Vérifie si la requête a réussi
            soup = BeautifulSoup(response.text, 'html.parser')

            # Rechercher la chaîne de caractères en base64 dans le texte brut de la page
            base64_pattern = re.compile(r'Décodez : RkxBRyA9([A-Za-z0-9+/=]+)')
            match = base64_pattern.search(response.text)

            if not match:
                raise ValueError("La chaîne de caractères en base64 n'a pas été trouvée.")

            base64_string = match.group(1)

            # Décoder la chaîne de caractères en base64
            decoded_bytes = base64.b64decode(base64_string)
            decoded_string = decoded_bytes.decode('utf-8')

            # Préparer les données pour le formulaire
            form_data = {'resultat': decoded_string}

            # Soumettre le formulaire
            response = session.post(url, data=form_data)
            response.raise_for_status()  # Vérifie si la requête a réussi

            # Vérifier si le message "BRAVO" est présent dans la réponse
            if "BRAVO" in response.text:
                print(f"{Fore.GREEN}Formulaire soumis avec succès.{Style.RESET_ALL}")
                # Extraire le texte entre crochets []
                code_obtenu = extract_code_between_brackets(response.text)
                print(f"{Fore.CYAN}Code obtenu : {code_obtenu}")
                print(f"{Fore.YELLOW}Le flag a été trouvé.{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Échec de l'affichage du code obtenu.{Style.RESET_ALL}")

        except requests.RequestException as e:
            print(f"{Fore.RED}Erreur lors de la requête HTTP : {e}{Style.RESET_ALL}")

        except (ValueError, base64.binascii.Error) as e:
            print(f"{Fore.RED}Erreur lors du traitement des données : {e}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Erreur inattendue : {e}{Style.RESET_ALL}")

        finally:
            # Pause pour respecter les limites de temps et éviter de surcharger le serveur
            time_elapsed = time.time() - start_time
            if time_elapsed < 1.5:  # Ajustez ce délai si nécessaire
                time.sleep(1.5 - time_elapsed)

            # Pause avant la prochaine itération (ajustez la durée selon vos besoins)
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Script interrompu par l'utilisateur.{Style.RESET_ALL}")
        sys.exit(0)
