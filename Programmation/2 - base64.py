import requests  # Pour faire des requ�tes HTTP
from bs4 import BeautifulSoup  # Pour parser le HTML
import base64  # Pour d�coder les cha�nes en base64
import re  # Pour les expressions r�guli�res
import time  # Pour les pauses et la mesure du temps
import os  # Pour les op�rations sur les fichiers et dossiers
import sys  # Pour g�rer les interruptions du script
from colorama import Fore, Style, init  # Pour la coloration du texte dans la console

# Initialisation de colorama
init(autoreset=True)

# URL de la page � scraper ATTENTION JETON A CHANGER EN FONCTION DE LA SESSION (le jeton fait 12 caract�res)
url = 'https://cyber-learning.fr/cyber-challenge/programmation/b64/sujet.php?jeton=JETON'

# V�rification du jeton
if 'jeton=JETON' in url:
    print(f"{Fore.RED}{Style.BRIGHT}Pense � remplacer ton jeton mon grand ;){Style.RESET_ALL}")
    sys.exit(1)

# Dossier de t�l�chargement pour les fichiers
download_folder = 'downloads'
os.makedirs(download_folder, exist_ok=True)  # Cr�er le dossier s'il n'existe pas

# Cr�er une session pour conserver les cookies et autres informations de session
session = requests.Session()

def extract_code_between_brackets(text):
    """
    Utilise une expression r�guli�re pour extraire le texte entre crochets []
    """
    match = re.search(r'\[(.*?)\]', text)
    return match.group(1) if match else 'Code non trouv�'

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("===================================")
    print("  Challenge Base 64 - D�codage")
    print("  Programmation - 20 points")
    print("")
    print("  Pr�sent� par br0nson")
    print("  LinkedIn : t.ly/fra3R ")
    print("===================================")
    print("")

    print(f"{Fore.GREEN}D�marrage du script de scraping...{Style.RESET_ALL}")
    while True:
        start_time = time.time()  # Enregistrer l'heure de d�but pour mesurer le temps �coul�

        try:
            # R�cup�rer le contenu de la page
            response = session.get(url)
            response.raise_for_status()  # V�rifie si la requ�te a r�ussi
            soup = BeautifulSoup(response.text, 'html.parser')

            # Rechercher la cha�ne de caract�res en base64 dans le texte brut de la page
            base64_pattern = re.compile(r'D�codez : RkxBRyA9([A-Za-z0-9+/=]+)')
            match = base64_pattern.search(response.text)

            if not match:
                raise ValueError("La cha�ne de caract�res en base64 n'a pas �t� trouv�e.")

            base64_string = match.group(1)

            # D�coder la cha�ne de caract�res en base64
            decoded_bytes = base64.b64decode(base64_string)
            decoded_string = decoded_bytes.decode('utf-8')

            # Pr�parer les donn�es pour le formulaire
            form_data = {'resultat': decoded_string}

            # Soumettre le formulaire
            response = session.post(url, data=form_data)
            response.raise_for_status()  # V�rifie si la requ�te a r�ussi

            # V�rifier si le message "BRAVO" est pr�sent dans la r�ponse
            if "BRAVO" in response.text:
                print(f"{Fore.GREEN}Formulaire soumis avec succ�s.{Style.RESET_ALL}")
                # Extraire le texte entre crochets []
                code_obtenu = extract_code_between_brackets(response.text)
                print(f"{Fore.CYAN}Code obtenu : {code_obtenu}")
                print(f"{Fore.YELLOW}Le flag a �t� trouv�.{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}�chec de l'affichage du code obtenu.{Style.RESET_ALL}")

        except requests.RequestException as e:
            print(f"{Fore.RED}Erreur lors de la requ�te HTTP : {e}{Style.RESET_ALL}")

        except (ValueError, base64.binascii.Error) as e:
            print(f"{Fore.RED}Erreur lors du traitement des donn�es : {e}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Erreur inattendue : {e}{Style.RESET_ALL}")

        finally:
            # Pause pour respecter les limites de temps et �viter de surcharger le serveur
            time_elapsed = time.time() - start_time
            if time_elapsed < 1.5:  # Ajustez ce d�lai si n�cessaire
                time.sleep(1.5 - time_elapsed)

            # Pause avant la prochaine it�ration (ajustez la dur�e selon vos besoins)
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Script interrompu par l'utilisateur.{Style.RESET_ALL}")
        sys.exit(0)
