""" GUIDE D"INSTALLATION DU PACKAGE GOOGLE_IMAGES_DOWNLOAD
Point d"attention : une version patchée de la version officiel du package a été utilisée car cette dernière n"est plus fonctionnelle
Methode 1 :
Simplement installer le package directement à partir de git :
"pip install git+https://github.com/Joeclinton1/google-images-download.git" (fonctionnel au 08/05/2020)
Methode 2 :
Installer le module à travers le zip "google-images-donwload-master"
"""

import unidecode
from google_images_download import google_images_download



def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern % title + ext))

# Initiate tool
response = google_images_download.googleimagesdownload()

# List of cities
_STOP_CITY = ["Paris", "Strasbourg", "Colmar", "Sacy", "Les Trois-Domaines", "Forbach-Boulay-Moselle", "Metz", "Thionville", "Lyon", "Lyon", "Torcy", "Chessy", "Nancy", "Mulhouse", "Meroux-Moval", "Les Auxons", "Dijon", "Mâcon", "Nîmes", "Montpellier", "Avignon", "Cabriès", "Marseille", "Chalon-sur-Saône", "Alixan", "Beaune", "Nice", "Antibes", "Cannes", "Saint-Raphaël", "Les Arcs-sur-Argens", "Toulon", "Remiremont", "Épinal", "Saint-Dié-des-Vosges", "Lunéville", "Saverne", "Sarrebourg", "Châlons-en-Champagne", "Vitry-le-François", "Bar-le-Duc", "Reims", "Rethel", "Charleville-Mézières", "Sedan", "Lille", "Ablaincourt-Pressoir", "Roissy-en-France", "Arras", "Redessan", "Montpellier", "Sète", "Agde", "Béziers", "Narbonne", "Perpignan", "Lille", "Montbard", "Douai", "Massy", "Saint-Pierre-des-Corps", "Poitiers", "Angoulême", "Bordeaux", "Le Mans", "Angers", "Nantes", "Rennes", "Laval", "Le Havre", "Rouen", "Mantes-la-Jolie", "Versailles", "Massy", "Saumur", "Louvigny", "Paris", "Hyères", "Colombier-Saugnieu", "Menton", "Valence", "Montélimar", "Orange", "Avignon", "Miramas", "Mâcon", "Bourg-en-Bresse", "Chambéry", "Valserhône", "Annemasse", "Thonon-les-Bains", "Évian-les-Bains", "Saint-Jean-de-Maurienne", "Modane", "Saint-Étienne", "Dole", "Besançon", "Carcassonne", "Toulouse", "Grenoble", "Aix-les-Bains", "Annecy", "Paris", "Fréthun", "Boulogne-sur-Mer", "Calais", "Dunkerque", "Lens", "Béthune", "Hazebrouck", "Étaples", "Verton", "Wasquehal", "Roubaix", "Tourcoing", "Valenciennes", "Paris", "Agen", "Montauban", "Saint-Brieuc", "Guingamp", "Morlaix", "Brest", "Lamballe-Armor", "Plouaret", "Landerneau", "Redon", "Vannes", "Auray", "Lorient", "Vitré", "Quimper", "Quimperlé", "Rosporden", "Saint-Malo", "Dol-de-Bretagne", "La Roche-sur-Yon", "Saint-Nazaire", "La Baule-Escoublac", "Le Croisic", "Pornichet", "Le Pouliguen", "Sablé-sur-Sarthe", "Les Sables-d\'Olonne", "Biganos", "Arcachon", "La Teste-de-Buch", "Libourne", "Vendôme", "Châtellerault", "Dax", "Bayonne", "Biarritz", "Saint-Jean-de-Luz", "Hendaye", "Niort", "Surgères", "La Rochelle", "Saint-Maixent-l\'École", "Chasseneuil-du-Poitou", "Tours", "Orthez", "Pau", "Lourdes", "Tarbes"]

# transform the list of cities into the right type [from a list to a string containing list of cities separated by commas)
# decode special characters
city_list = ""
for city in _STOP_CITY:
    city_list += unidecode.unidecode(city) + " tourisme, "
city_list = city_list[:-2] # remove last comma


arguments = {"keywords":city_list,"limit":1,"print_urls":True,"size":">10MP", "aspect_ratio":"wide", "type":"photo"}
paths = response.download(arguments)





