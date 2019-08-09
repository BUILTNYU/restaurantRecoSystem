import numpy as np 
import matplotlib.pylab as plt
import pickle
from random import sample 
from collections import Counter 

def linUCB(A, b, history, candidate_pool, alpha, context_size):
    # A: existant matrix for all resturants 
        #either None or a k*k matrix
    # b: existant vector 
        #either None or a k*1 vector
    # history: array of (reward, restaurant_id,features)
        #must be a list, no restriction on length
    # candidate_pool: array of restaurants to be recommended 
        # array of (restaurantt_id,features)
    # alpha: confidence interval 
        # 0<alpha<1 for constant alpha: alpha*sd
    # context_size: the dimension of the context
    # click_num: number of restaurants clicks 
    # click_den: number of restaurants recommended
    # test_mode: if we are using a simulated dataset to exame the performance of this algorithm

    if A is None: #initialize a new matrix, otherwise based on old history
        A = np.identity(context_size)  # k*k identity matrix 
    if b is None: #initialize a new vector, otherwise based on old history
        b = np.atleast_2d(np.zeros(context_size)).T # k*i zero vector

    for record in history:

        reward = record[0]
        restaurant_id = record[1]
        context = np.asarray(record[2:])

        A = A + np.outer(context, context)
        b = b + reward*np.reshape(context,(context_size,1))

    if len(candidate_pool)==0:
        #here we are not making predictions, but only update the parameters
        prediction_ids = None
    else:
        coefficient = np.dot(np.linalg.inv(A), b)
        ucb = {}
        for candidate in candidate_pool:
            candidate_id = candidate[0]            
            c_context = np.asarray(candidate[1:])
            
            sd = np.sqrt( np.dot(c_context.T,np.dot(np.linalg.inv(A), c_context)) ) 

            ucb[candidate_id] = np.asscalar(  np.dot(coefficient.T,c_context) + np.dot(alpha,sd) )

        # # Choose the restaurant with largest UCB
        # # prediction_id = maximum = max(ucb, key=ucb.get)
        # prediction_id = max(ucb, key=ucb.get)

        # give back all predictions 
        # let the main.py program decides if some of them are recommended before
        # and thus, recommend the next one that haven't be recommended before
        prediction_ids = list(Counter(ucb))

    return A, b, prediction_ids

if __name__ == "__main__":
    print("Program starts...")
    # how many training data 
    # 1000 means to use the first 1000 records to train the model
    # 0 means starts from the sratch
    index = 0
    # The parameter for the degree of exploration
    alpha = 0.5

    input_file = "../data/simulated_arm_contexts.pyc"

    data = pickle.load(open(input_file,"rb"))

    data = list(map(lambda x:x[:2]+x[6:],data.values.tolist())) 
    # don't consider distance, rating, review_count, price
    # as they are not part of the factors that generate the reward
    id2context = {}

    for each in data:
        id2context[each[1]] = each[2:]


    train_set = data[:index]
    test_set = list(map(lambda x:x[1:],data[index:]))
    

    print("Total number of history records used for training:",len(train_set))
    print("Total number of records for testing",len(test_set))

    context_size = len(data[0])-1-1 # remove reward and arm

    likedRestaurants = list(filter(lambda x: x[0]==1,data)) # get liked restaurants
    likedRestaurants = list(map(lambda x:x[1],likedRestaurants)) # get their names
    likedRestaurants = set(likedRestaurants) #remove duplicates

    total_positive = list(filter(lambda x: x[0]==1,data))
    average = len(total_positive)/len(data)

    # train the model, get parameters and prediction 
    # number of candidates for each prediction
    size = 10

    #cumulative click through rate
    test_set_sampled = test_set[:1]
    # test_set_sampled = sample(test_set,50)
    A, b, predictions = linUCB(None, None, train_set, test_set_sampled, alpha, context_size)

    prediction = predictions[0]
    #only give one result, highest ucb

    click_num = 0
    click_den = 0
    x = []#iternation 
    y = []#total click/ total prediction
    z = []#standard
    # for i in range(1,200,size):
    for i in range(1,len(test_set)-size,size):
        reward = 0
        if prediction in likedRestaurants:
            # print("iter:",i/size)
            click_num += 1
            reward = 1
        click_den += 1
        # make sure it doesn't appear before, otherwise it might always recommend the one it recommended before
        test_set_sampled = test_set[i:i+size]
        # print(test_set_sampled)
        context = id2context[prediction]
        result = [reward,prediction,context]
        A, b, predictions = linUCB(A, b, [result], test_set_sampled, alpha, context_size) #it's learning 
        # A, b, prediction = linUCB(A, b, [], test_set_sampled, 0.01, context_size) # not learning 
        prediction = predictions[0]
        #only give one result, highest ucb

        x.append(i/size)
        y.append(click_num/click_den)
        z.append(average)
    plt.plot(x, y, "b",x,z,"r",label = 'cumulative click-through-rate')
    plt.show()



    # #average click through rate
    # test_set_sampled = test_set[:1]
    # # test_set_sampled = sample(test_set,50)
    # A, b, prediction = linUCB(None, None, train_set, test_set_sampled, 0.01, context_size)
    # x = []#iternation 
    # y = []#total click/ total prediction
    # z = []#standard
    # for i in range(1,len(test_set)-size,size):
    #     click_num = 0
    #     click_den = 0
    #     for j in range(i,i+size):
    #         reward = 0
    #         if prediction in likedRestaurants:
    #             click_num += 1
    #             reward = 1
    #         click_den += 1
    #         # make sure it doesn't appear before, otherwise it might always recommend the one it recommended before
    #         test_set_sampled = test_set[j:j+1]
    #         # print(test_set_sampled)
    #         context = id2context[prediction]
    #         result = [reward,prediction,context]
    #         A, b, prediction = linUCB(A, b, [result], test_set_sampled, 0.01, context_size) #it's learning 
    #     x.append(i/size)
    #     y.append(click_num/click_den)
    #     z.append(average)
    # plt.plot(x, y, "b",x,z,"r",label = 'average click-through-rate')
    # plt.show()
    
