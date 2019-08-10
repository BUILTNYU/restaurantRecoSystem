Notice:
1. please keep of positive word array in "preprocessing/pca_model_training.ipynb","preprocessing/data_stimulation.ipynb/" consistent


Database Setup:
	1. create a database called `UrbanConnector` in MySQL
	2. import file "/database/database_setup.sql" to create two tables
	3. change the database setting in the following files to your own database:
		A. main/app.py line11-17
		B. main/main.py line 171-180 if you want to run this individual file and test the program with terminal
		C. main/helperFunction.py line 6-13

Preprocessing:
	1. get_restaurant_data.py: get around 5w restaurant records from Yelp API to train PCA model and for offline evaluation
		output: /data/restaurants_information/...(12 files)
		
	2. pca_model_training.ipynb: convert text data(restaurant info) to feature matrix and train PCA model to reduce the dimension to 
		output: /pca_model.sav (but now it's moved to /main folder)
		
	3. offline_evaluation_data_simulation.ipynb: generated synthetic data (food preference) to test the algorithm, but much of the part is similar to pca_model_training program
		output: /simulated_arm_contexts.pyc (but now it's moved to /data folder)
		
Main:
	1.yelDataCollection.py: used to make request to Yelp API and retrieve candidate restaurants information.
	(multithreading to increase the speed)
	run it directlly will give you some restaurants that satisfy your setting

	2.featureExtraction.py: convert the text data to feature matrix.

	3.linUCB.py: main recommendation algorithm using contextual bandit algorithm
	you can run it directly to see the result of an offline evaluation

	4.main.py: main functions to implement the recommendation algorithm, like get and save matrices, make recommendations and update the result.

	5.app.py: web framework

	
Two main services:
'/getRecommendation:<user_profile>+<user_id>+<time>+<longitude>+<latitude>+<radius>+<price>'
def getRecommendation(user_profile,user_id,time,longitude,latitude,radius,price):


'/feedback:<user_profile>+<user_id>+<time>+<restaurant_id>+<recommendation_time>+<reward>'
def feedback(user_profile,user_id,time,restaurant_id,recommendation_time,reward):



To install the dependencies, run: pip install -r requirements.txt.

To start the web services, run under main folder `python app.py`