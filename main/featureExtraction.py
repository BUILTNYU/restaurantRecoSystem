import pandas as pd
import numpy as np
import pickle
from sklearn.decomposition import PCA
import gc
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

__directory_path__ = ""
__model_path__ = __directory_path__  + "pca_model.sav"

positive = ['acaibowls', 'afghani', 'african','arabian', 'arcades', 'argentine',
    'armenian',  'asianfusion', 'australian', 'austrian', 'bagels', 'bakeries',
    'bangladeshi',  'barcrawl', 'bars', 'bartenders', 'basque', 'bbq', 'belgian',  
    'brasseries', 'brazilian', 'breakfast_brunch', 'breweries', 'brewingsupplies',
    'bridal', 'british', 'bubbletea', 'buffets', 'burgers', 'burmese', 'butcher',
    'cabaret', 'cafes', 'cafeteria', 'cajun', 'cambodian', 'cantonese', 'caribbean', 
    'catering',  'cheese', 'cheesesteaks', 'chicken_wings', 'chickenshop', 'chinese', 
    'chocolate',  'colombian', 'comfortfood', 'creperies', 'cuban', 'culturalcenter',  
    'czech', 'delis', 'desserts', 'dimsum', 'diners', 'dinnertheater', 'distilleries','diyfood', 
    'dominican', 'donuts',  'egyptian', 'empanadas', 'eritrean', 'ethiopian', 'falafel', 'farmersmarket', 
    'filipino', 'fishnchips',  'fondue', 'food', 'food_court', 'fooddeliveryservices', 'foodstands', 
    'foodtrucks', 'french', 'gamemeat', 'gastropubs', 'gelato', 'georgian', 'german',  
    'gluten_free', 'gourmet', 'greek', 'hainan', 'haitian', 'halal', 'hawaiian', 'hennaartists',
    'herbsandspices', 'himalayan', 'hkcafe', 'honduran', 'hookah_bars', 'hotdog', 'hotdogs',  'hotpot', 'iberian',  'importedfood', 
    'indonesian', 'indpak', 'internetcafe', 'intlgrocery', 'irish', 'irish_pubs', 'italian', 'izakaya', 'japacurry', 'japanese', 
    'jazzandblues', 'karaoke', 'kebab',  'kitchensupplies', 'korean', 'kosher',  'laotian', 'latin', 'lebanese', 
    'localflavor', 'macarons', 'mags', 'malaysian',  'meats', 'mediterranean', 'mexican', 'mideastern', 'modern_european', 
    'mongolian', 'moroccan',  'newamerican', 'newmexican',   'noodles', 'pakistani', 'panasian', 
    'pastashops', 'persian', 'personalchefs', 'peruvian', 'petadoption', 'petstore', 'piadina', 
    'pianobars', 'pizza', 'playgrounds', 'poke', 'polish', 'poolhalls', 'popuprestaurants', 'portuguese', 'poutineries', 'pretzels', 
    'pubs', 'puertorican', 'ramen', 'raw_food', 'restaurants', 'russian', 'salad', 'salvadoran', 'sandwiches', 
    'sardinian', 'scandinavian', 'scottish', 'seafood', 'seafoodmarkets', 'senegalese', 'servicestations', 'shanghainese', 
    'shavedice', 'sicilian', 'singaporean', 'slovakian', 'smokehouse','somali', 'soulfood', 'soup', 
    'southafrican', 'southern', 'spanish', 'srilankan', 'steak',   'sushi', 'syrian', 'szechuan', 'tacos', 'sichuan','hotpot', 
    'taiwanese', 'tapas', 'tapasmallplates',  'tea', 'teppanyaki', 'tex-mex', 'thai','themedcafes', 'tikibars', 'tobaccoshops', 
    'tradamerican', 'trinidadian', 'turkish', 'tuscan', 'uzbek', 
    'vegan', 'vegetarian', 'venezuelan',  'vietnamese', 'waffles', 'wine_bars', 'wraps']

#decide if this destination qualify our criteria
def qualify(array, positive_words):
  for each in array:
    if each in positive_words:
      return 1
  return 0

#make sure that all different data pool will have the same number of categories
def addColumns(table, current_categories,positive):
  for each in positive:
    if each not in current_categories:
      table[each] = 0
      

def featureExtraction(data):
    restaurants = pd.DataFrame.from_records(data)
    # PRICE2NUM = {"$":1,"$$":2,"$$$":3,"$$$$":4,"£":1,"££":2,'£££':3,'££££':4}
   
    #make sure that all the values in the price columns are valid
    #filter out columns with NaN
    restaurants= restaurants.dropna(subset=['price'])
    # restaurants = restaurants[restaurants["price"] in PRICE2NUM.keys()]
    #use length directly, avoide error caused by other unseen price labels
    restaurants.price = restaurants.price.apply(lambda x: len(x))

    # convert list of dicts to list of alias in the dic
    restaurants.categories = restaurants.categories.apply(lambda x:list(map(lambda cate:cate["alias"],x)))

    restaurants["qualified"] = restaurants.categories.apply(lambda x: qualify(x,positive) )

    #drop all unqualified destinations
    restaurants = restaurants[restaurants.qualified == 1]

    onehot_categories = restaurants.categories.str.join('|').str.get_dummies()
    # add columns that didn't appear
    current_categories = onehot_categories.columns.values.tolist()
    addColumns(onehot_categories,current_categories,positive)

    # make sure that the order of categories will always be the same in different dataset 
    onehot_categories = onehot_categories[positive]

    
    pca_loaded_model = pickle.load(open(__model_path__, 'rb'))
    decomposed_categories = pca_loaded_model.transform(onehot_categories)

    #make sure that there is no duplicates, though it won't happen
    restaurants.reset_index(drop=True, inplace=True)
    context_pool = pd.concat([restaurants[["id","distance","rating","review_count","price"]], pd.DataFrame(decomposed_categories)] ,axis=1)
    context_pool = context_pool.values.tolist()

    return context_pool

