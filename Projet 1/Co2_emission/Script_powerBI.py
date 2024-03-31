# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(make, uid)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:
import matplotlib.pyplot as plt

# Trier les fréquences de fabricants de véhicules électriques par ordre décroissant
make_counts = dataset['make'].value_counts().sort_values(ascending=False)

# Extraire les 10 marques les plus courantes et leurs fréquences
top_10_makes = make_counts[:10]

# Créer un dictionnaire associant chaque make à une couleur personnalisée
make_colors = {
    'BMW': '#34C6BB',   
    'AUDI': '#FF5733',   
    'FORD': '#7CBF7E',      
    'CITROEN': '#FFD700',     
    'KIA': '#FF69B4',   
    'FIAT': '#5C92E6',   
    'DACIA': '#1600BB',     
    'HYUNDAI': '#008000',   
    'LAND ROVER': '#FFFF00',   
    'JEEP': '#8B4513',
    'MERCEDES-BENZ': '#E57373',   
    'AUDI': '#FF5733',   
    'VOLKSWAGEN': '#A1887F',      
    'BMW': '#34C6BB',     
    'VOLVO': '#7986CB',   
    'RENAULT': '#FFB74D',   
    'TESLA': '#64B5F6',     
    'PORSCHE': '#9575CD',   
    'PEUGEOT': '#FF8A65',   
    'KIA': '#4DD0E1',
    'MAZDA': '#E6A0C4',
    'SEAT':  '#C8C8C8',
    'SKODA': '#55EE13'
}

# Tracer le graphique pour les 10 premières marques avec les couleurs personnalisées
fig, ax = plt.subplots(figsize=(20, 5))
colors = [make_colors.get(make, '#000000') for make in top_10_makes.index]
top_10_makes.plot(kind='bar', color=colors, ax=ax)

# Changer le fond de la figure en transparent
fig.patch.set_facecolor('none')
ax.patch.set_facecolor('none')

# Changer la couleur du titre, des étiquettes x et y, et des axes en blanc
plt.title('10 premiers fabricants de véhicules Thermiques en Europe', fontsize=25, color='white')
plt.xlabel('Fabricants', fontsize=25, color='white')
plt.ylabel('Fréquence', fontsize=25, color='white')

# Changer la couleur des étiquettes de l'axe x en blanc
ax.set_xticklabels(ax.get_xticklabels(), color='white')
ax.set_yticklabels(ax.get_yticklabels(), color='white')

# Changer la couleur des étiquettes de l'axe y en blanc
ax.yaxis.label.set_color('white')

# Changer la couleur des axes en blanc
ax.spines[['bottom', 'left', 'top', 'right']].set_color('white')

plt.xticks(rotation=45, fontsize=14, color='white')  # Réglez la taille de la police des étiquettes x à 14 et la couleur en blanc
plt.tight_layout()

# Ajouter des labels au-dessus des barres
for i, v in enumerate(top_10_makes):
    ax.text(i, v + 5, str(v), color='white', fontsize=14, ha='center', va='bottom')

plt.show()


