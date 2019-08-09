import pandas as pd
import numpy as np
import pickle
from sklearn.decomposition import PCA
import gc

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

directory = "../"
r_1_b_file = directory+"data/restaurants_information/restaurants_nyc_1_bestmatch.pyc"
r_2_b_file = directory+"data/restaurants_information/restaurants_nyc_2_bestmatch.pyc"
r_3_b_file = directory+"data/restaurants_information/restaurants_nyc_3_bestmatch.pyc"
r_4_b_file = directory+"data/restaurants_information/restaurants_nyc_4_bestmatch.pyc"
r_1_r_file = directory+"data/restaurants_information/restaurants_nyc_1_rating.pyc"
r_2_r_file = directory+"data/restaurants_information/restaurants_nyc_2_rating.pyc"
r_3_r_file = directory+"data/restaurants_information/restaurants_nyc_3_rating.pyc"
r_4_r_file = directory+"data/restaurants_information/restaurants_nyc_4_rating.pyc"
r_1_rw_file = directory+"data/restaurants_information/restaurants_nyc_1_reviewcount.pyc"
r_2_rw_file = directory+"data/restaurants_information/restaurants_nyc_2_reviewcount.pyc"
r_3_rw_file = directory+"data/restaurants_information/restaurants_nyc_3_reviewcount.pyc"
r_4_rw_file = directory+"data/restaurants_information/restaurants_nyc_4_reviewcount.pyc"

r_1_b = pickle.load(open(r_1_b_file,"rb"))
r_2_b = pickle.load(open(r_2_b_file,"rb"))
r_3_b = pickle.load(open(r_3_b_file,"rb"))
r_4_b = pickle.load(open(r_4_b_file,"rb"))
r_1_r = pickle.load(open(r_1_r_file,"rb"))
r_2_r = pickle.load(open(r_2_r_file,"rb"))
r_3_r = pickle.load(open(r_3_r_file,"rb"))
r_4_r = pickle.load(open(r_4_r_file,"rb"))
r_1_rw = pickle.load(open(r_1_rw_file,"rb"))
r_2_rw = pickle.load(open(r_2_rw_file,"rb"))
r_3_rw = pickle.load(open(r_3_rw_file,"rb"))
r_4_rw = pickle.load(open(r_4_rw_file,"rb"))


#concatenate all lists

restaurants_list = r_1_b+r_2_b+r_3_b+r_4_b+r_1_r+r_2_r+r_3_r+r_4_r+r_1_rw+r_2_rw+r_3_rw+r_4_rw
#remove duplicates
restaurants_unique = []
for each in restaurants_list:
  if each not in restaurants_unique:
    restaurants_unique.append(each)
print("restaurants_list length:",len(restaurants_list))
print("restaurants_unique length:",len(restaurants_unique))


restaurants = pd.DataFrame.from_records(restaurants_unique)
print(restaurants.columns)
print(restaurants[["alias","distance","categories"]].head())

PRICE2NUM = {"$":1,"$$":2,"$$$":3,"$$$$":4,'£££':3,'££££':4}
#filter out columns with NaN
restaurants= restaurants.dropna(subset=['price'])
# print("count:",restaurants.count())
#print(restaurants.price.unique())
#['$' '$$' '$$$' '£££' '$$$$' '££££']
restaurants.price = restaurants.price.apply(lambda x: PRICE2NUM[x])

# convert list of dicts to list of alias in the dic
restaurants.categories = restaurants.categories.apply(lambda x:list(map(lambda cate:cate["alias"],x)))

preference = ["hotpot",'cantonese',"szechuan",'bbq','korean','noodles','salad']
# if the food is related to these preferences, 70% the user will like it
# if the food fall out of these preferences, 30% the user will like it

#randomly get some restaurants
restaurants_pool = restaurants.sample(frac = 0.3)

# whether the user will like it 
import random 

def likeOrNot(restaurant_categories,preference):
  intersection = set(restaurant_categories)&set(preference)
  if len(intersection)==0:#30% like this restaurants
    if random.random()<0.3:
      return 1
    else:
      return 0
  else:#70% like this restaurants
    if random.random()<0.7:
      return 1
    else:
      return 0    
 

restaurants_pool["like"] = restaurants_pool.categories.apply(lambda x: likeOrNot(x,preference) )


#decide if this destination qualify our criteria
def qualify(array, positive_words):
  for each in array:
    if each in positive_words:
      return 1
  return 0

restaurants_pool["qualified"] = restaurants_pool.categories.apply(lambda x: qualify(x,positive) )

  #drop all unqualified destinations
restaurants_pool = restaurants_pool[restaurants_pool.qualified == 1]
print(restaurants_pool.count())

def addColumns(table, current_categories,positive):
  for each in positive:
    if each not in current_categories:
      table[each] = 0
      

onehot_categories = restaurants_pool.categories.str.join('|').str.get_dummies()
# add columns that didn't appear
current_categories = onehot_categories.columns.values.tolist()
addColumns(onehot_categories,current_categories,positive)

# make sure that the order of categories will always be the same in different dataset 
onehot_categories = onehot_categories[positive]

filename = directory+"/main/pca_model.sav"
pca_loaded_model = pickle.load(open(filename, 'rb'))
decomposed_categories = pca_loaded_model.transform(onehot_categories)
decomposed_scores = pca_loaded_model.score(onehot_categories)
print("score",decomposed_scores)
print(decomposed_categories[:2,:])

restaurants_pool.reset_index(drop=True, inplace=True)
arm_contexts_simulated = pd.concat([restaurants_pool[["like","id","distance","rating","review_count","price"]], pd.DataFrame(decomposed_categories)] ,axis=1)


file = directory+"/data/simulated_arm_contexts.pyc"
pickle.dump(arm_contexts_simulated,open(file,"wb"))

