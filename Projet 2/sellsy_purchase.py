import json
import requests_oauthlib
import oauthlib.oauth1 as oauth1
from errors.sellsy_exceptions import SellsyAuthenticateError, SellsyError
from dotenv import load_dotenv
import csv
from datetime import datetime, timedelta
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

DEFAULT_URL = 'https://apifeed.sellsy.com/0/'


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

    def get_purchase_list(self, params):
        # Utilisez la méthode api pour obtenir la liste d'achats
        return self.api(method=params['method'], params=params['params'])
    
    # Function to fetch purchase details
    def fetch(self, purshase_id):
        payload = {
            'method': 'Purchase.getOne',
            'params': {
                'id': f'{purshase_id}'
            }
        }

        response = self.session.post(
            DEFAULT_URL,
            data={
                'request': 1,
                'io_mode': 'json',
                'do_in': json.dumps(payload)
            },
            headers={'content-type': 'application/json', 'cache-control': 'no-cache'}
        )

        while not response.ok:
            print(f"Retrying for purchase ID: {purshase_id}")
            print(response)
            print(response.text)
           
            response = client.session.post(
                DEFAULT_URL,
                data={
                    'request': 1,
                    'io_mode': 'json',
                    'do_in': json.dumps(payload)
                },
                headers={'content-type': 'application/json', 'cache-control': 'no-cache'}
            )
            time.sleep(5)

        return response.json()["response"]["map"]


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

        # Utiliser la méthode get_purchase_list pour obtenir la liste d'achats
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

        # Lire le fichier CSV contenant les identifiants
        df_ids = pd.read_csv(r'C:\Users\Administrateur\Desktop\sellsy\df_id.csv')

        # Créer une liste des valeurs 'id'
        purshase_ids = df_ids['id'].tolist()
        # Convertir les identifiants en entiers
        purshase_ids = [int(id) for id in purshase_ids]
        # Afficher la liste des identifiants
        print(purshase_ids)


        try:
            all_purchases = []  # Initialisation d'une liste pour stocker les détails des achats récupérés
            for purchase_id in purshase_ids:
                search_params = {
                    'method': 'Purchase.getOne',
                    'params': {
                        'id': purchase_id
                    }
                }
                # Utiliser la méthode get_purchase_list pour obtenir la liste d'achats
                purchases = client.get_purchase_list(search_params)
                print("Liste d'achats récupérée avec succès:")
                print("API Response:")
                print(purchases) 

                purchase_details = client.fetch(purchase_id)
                all_purchases.append(purchase_details)

                print(f"Détails de l'achat {purchase_id} récupérés avec succès.")

            # On crée un DataFrame à partir des détails récupérés
            purchases_df = pd.DataFrame(all_purchases)
            print(purchases_df.head())
            print(f"Total d'achats pour l'ID {purchase_id} : {len(purchases_df)}")

            #CSV

            chemin_fichier_csv = rf'C:\Users\Administrateur\Desktop\sellsy\resultat_{purchase_id}.csv'
            purchases_df.to_csv(chemin_fichier_csv, index=False)
            print(f"Le DataFrame pour l'achat {purchase_id} a été enregistré avec succès dans {chemin_fichier_csv}")

            # Obtenez les identifiants d'achat
            purchase_ids = [purchase_id for purchase_id in purchases_df["id"]]

            # Utilisation de ThreadPoolExecutor pour récupérer les données d'achat
            with ThreadPoolExecutor(max_workers=4) as executor:
                purchases_data = list(tqdm(executor.map( client.fetch, purchase_ids), total=len(purchase_ids)))

            # Traitements supplémentaires avant la sauvegarde en CSV
            rows_df = pd.DataFrame.from_dict(purchases_data)
            rows_df = pd.DataFrame(rows_df["rows"].apply(lambda x: list(v for v in x.values() if isinstance(v, dict))).explode("rows").tolist())

            # Traitements finaux 
            # Fusion des DataFrames purchases_df et rows_df
            result = purchases_df.merge(rows_df, right_on="purdomapid", left_on="purdocmapid", how="left")
            # Sélection des colonnes pertinentes dans le DataFrame résultant
            result = result[["ident", "displayedDate", "type", "step", "thirdname", "linkedid_y", "name", "qt", "formatted_taxAmount", "formatted_taxrate", "formatted_unitAmount", "formatted_totalAmount_y", "formatted_created", "notes_y"]]
            # Fusion avec le DataFrame items_df
            #result = result.merge(items_df, left_on="linkedid_y", right_on="id", how= "left")
            # Suppression des colonnes 'linkedid_y' et 'id' du DataFrame résultant
            result.drop(columns= ['linkedid_y', 'id'], inplace= True)
            # Sélection des colonnes finales
            #result = result[["ident", "displayedDate", "type", "step", "thridname", "tradename", "name", "qt", "formatted_taxAmount", "formatted_taxrate", "formatted_unitAmount", "formatted_totalAmount_y", "formatted_created", "notes_y", "accountingPurchaseCodeVal"]]
            # Renommer les colonnes pour une meilleure lisibilité
            #result.columns = ["Document", "Date du document", "Type", "Statut", "Fournisseur", "Produit/Service", "Référence produit/service", "Quentité", "Montant TVA", "Taux TVA", "P.U HT", "Total HT", " Date de création", "Description", "Code comptable"]
            # Convertir la colonne 'Date du document' en datetime
            result["Date du document"] = pd.to_datetime(result["Date du document"])
            result["Date du document"] = pd.to_datetime(result["Date du document"], dayfirst=True)
            # Conversion des colonnes numériques de format string en float
            float_columns = ["Quantité", "Montant TVA", "Taux TVA", "P.U HT", "Total HT"]

            for col in float_columns:
                result[col] = result[col].str.replace(' ', '').str.replace(",", ".").astype(float)
        
            #éliminer les balises HTML ou d'autres caractères spéciaux
            result["Description"] = result ["Description"].str.replace('<.*?>', ' ', regex=True).replace('#', '', regex=True) 

        
            chemin_fichier_csv = rf'C:\Users\Administrateur\Desktop\sellsy\resultat_final.csv'
            result.to_csv(chemin_fichier_csv, index=False)
            print(f"Le DataFrame final a été enregistré avec succès dans {chemin_fichier_csv}")


        except Exception as e:
            print(f"Erreur lors de la récupération des achats : {e}")
        except SellsyError as e:
            print(f"Sellsy API Error: {e}")
        except SellsyAuthenticateError as e:
            print(f"Sellsy Authentication Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    





