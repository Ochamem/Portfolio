import json
import requests_oauthlib
import oauthlib.oauth1 as oauth1
import pandas as pandas
from concurrent.futures import ThreadPoolExecutor
from errors.sellsy_exceptions import SellsyAuthenticateError, SellsyError
from dotenv import load_dotenv
import csv
from datetime import datetime, timedelta


# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

DEFAULT_URL = 'https://apifeed.sellsy.com/0/'

# Setting the maximum number of columns displayed to 200
pd.set_option('display.max_columns', 200)

class Client:
    def __init__(self, consumer_token, consumer_secret, user_token, user_secret, url=DEFAULT_URL):
        self.url = url
        self.session = requests_oauthlib.OAuth1Session(
            consumer_token,
            consumer_secret,
            user_token,
            user_secret,
            signature_method=oauth1.SIGNATURE_PLAINTEXT,
            signature_type=oauth1.SIGNATURE_TYPE_BODY
        )

    def api(self, method='Infos.getInfos', params={}):
        headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
        payload = {'method': method, 'params': params}

        response = self.session.post(self.url, data={
            'request': 1,
            'io_mode': 'json',
            'do_in': json.dumps(payload)
        }, headers=headers)

        # Handle OAuth error (401 status code returned)
        if response.status_code == 401:
            raise SellsyAuthenticateError(response.text)

        # Error handler
        response_json = response.json()
        if response_json['status'] == 'error':
            error_code, error_message = response_json['error']['code'], response_json['error']['message']
            raise SellsyError(error_code, error_message)

        return response_json['response']

    def get_billing_list(self, params):
        # Utilisez la méthode api pour obtenir la liste de facturation
        return self.api(method=params['method'], params=params['params'])


if __name__ == '__main__':
    import os

    # Récupérer les clés d'identification depuis les variables d'environnement
    consumer_token = os.environ.get('SELLSEY_CONSUMER_TOKEN')
    consumer_secret = os.environ.get('SELLSEY_CONSUMER_SECRET')
    user_token = os.environ.get('SELLSEY_USER_TOKEN')
    user_secret = os.environ.get('SELLSEY_USER_SECRET')

    print(f"Consumer Token: {consumer_token}")
    print(f"Consumer Secret: {consumer_secret}")
    print(f"User Token: {user_token}")
    print(f"User Secret: {user_secret}")

    client = Client(
        consumer_token,
        consumer_secret,
        user_token,
        user_secret)

    # Assurez-vous que les clés récupérées ne sont pas None
    if None in (consumer_token, consumer_secret, user_token, user_secret):
        print("Erreur: Certaines clés d'identification sont manquantes.")
    else:

        # Utiliser la méthode get_purchase_list pour obtenir la liste de facturation
        today = datetime.now()
        twelve_months_ago = today - timedelta(days=365)
        timestamp_start = int(twelve_months_ago.timestamp())
        timestamp_end = int(today.timestamp())

        # Convertir les timestamps en objets datetime
        start_date = datetime.fromtimestamp(timestamp_start)
        end_date = datetime.fromtimestamp(timestamp_end)

        # Afficher les dates au format désiré (par exemple, 'YYYY-MM-DD HH:MM:SS')
        format_date = '%Y-%m-%d %H:%M:%S'
        start_date_str = start_date.strftime(format_date)
        end_date_str = end_date.strftime(format_date)

        print(f"Période de {start_date_str} à {end_date_str}")
        # Utiliser la méthode Document.getList pour obtenir la liste de facturation
        search_params = {
            'method': "Purchase.getOne",
            'params': {
                "id": "4588913"
            }
        }
        '''search_params = {
            'method': 'Document.getList',
            'params': {
                'doctype': 'invoice',
                'includeLinkedDocs': 'Y',  
                'includeTags': 'Y',  
                'includePayments': 'Y',
                'search': {
                    'periodecreated_start': timestamp_start,
                    'periodecreated_end': timestamp_end
                },
                'pagination': {
                    'nbperpage': 5000  # Nombre de résultats par page
                },
                'order': {
                    'direction': 'DESC',
                    'order': 'doc_displayedDate'
                },
                'currency': 'EUR'
            }
        }
'''

        try:
            billing = client.get_billing_list(search_params)
            print("Liste de facturation récupérée avec succès:")
            print(billing)
        except ValueError as e:
            print(f"Erreur lors de la récupération de la liste de facturation: {str(e)}")

    # Chemin où vous souhaitez enregistrer le fichier CSV
    chemin_fichier = r'C:\Users\Administrateur\Desktop\sellsy\billing.csv'

    # Récupérer toutes les clés pour les noms de colonnes
    keys = set()
    for item in billing['result'].values():
        keys.update(item.keys())

    # Ouvrir le fichier CSV en mode écriture
    with open(chemin_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=keys)

        # Écrire l'en-tête du fichier CSV
        writer.writeheader()

        # Écrire les données dans le fichier CSV
        for item in billing['result'].values():
            writer.writerow(item)

    print("Données enregistrées dans le fichier CSV avec succès.")

