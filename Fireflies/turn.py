import numpy as np
from scipy.spatial import distance as dist
import copy

# This returns a matrix with the distances between each worm calculated if the
# worm in the row is influenced by the worm in the column, else 0
def influence_matrix(pop, score, num_worms, func):#расстояния мужду светлячками
    graph = np.array([np.zeros(num_worms)] * num_worms)
    
    for i in range(num_worms):
        for j in range(num_worms):
            if i == j:
                graph[i][j] = 0
            elif dist.euclidean((pop[i][0],pop[i][1]), (pop[j][0],pop[j][1])) <= score[j]:
                graph[i][j] = dist.euclidean((pop[i][0],pop[i][1]), (pop[j][0],pop[j][1]))
            else:
                graph[i][j] = dist.euclidean((pop[i][0],pop[i][1]), (pop[j][0],pop[j][1]))
                #graph[i][j] = 0
    return graph
    
def next_turn(pop, score, im, num_worms, max_jitter, dims, lower_bound, influence_factor, fitness_function, fi):
    n_turn = copy.deepcopy(pop)
    
    # X and Y movement is determined by the ratio of distance between worms and
    # the radius of the influencing worm
    # This ensures that closer worms will have more influence than further worms
    # with the same pull, and at the same time worms with large influences will
    # have more pull than other worms of the same distance
    for i in range(num_worms):
        x_move = 0
        y_move = 0
        jitter_x = 0
        jitter_y = 0
        percent_move = 0
        xy_t = True
        for j in range(num_worms):
            if(i!=j):
                if(score[i] > score[j]): #and dist.euclidean((n_turn[i][0],n_turn[i][1]), (n_turn[j][0],n_turn[j][1])) < 5):
                    x_move = 0
                    y_move = 0
                    percent_move = np.math.exp(-np.power(im[i][j], 2) * (1 - fi)) * 1 #кофф передвижения(fitness_function(n_turn[j]) - fitness_function(n_turn[i]))
                    #percent_move = 1 - im[i][j] / score[j]
                    xy_t = True
                    x_move += (pop[j][0] - pop[i][0]) * percent_move / (10)
                    y_move += (pop[j][1] - pop[i][1]) * percent_move / (10)

                    n_turn[i][0] = keep_in_bounds(x_move + n_turn[i][0], dims)
                    n_turn[i][1] = keep_in_bounds(y_move + n_turn[i][1], dims)
                    score[i] = get_score_one(n_turn[i], lower_bound, influence_factor, fitness_function)
        if xy_t:
            a = max_jitter * np.random.rand()
            b = max_jitter * np.random.rand()
            mass = [fitness_function([n_turn[i][0], n_turn[i][1]]), fitness_function([n_turn[i][0] + a, n_turn[i][1] + b]), fitness_function([n_turn[i][0] + a, n_turn[i][1] - b]), fitness_function([n_turn[i][0] - a, n_turn[i][1] + b]), fitness_function([n_turn[i][0] - a, n_turn[i][1] - b])]
            min_num = np.argmin(mass)
            #print(mass)
            #print(min_num)
            jitter_x = max_jitter * np.random.rand() * np.random.randint(-1,2)
            jitter_y = max_jitter * np.random.rand() * np.random.randint(-1,2)
            if min_num == 1:
                n_turn[i][0] += a
                n_turn[i][1] += b
            elif min_num == 2:
                n_turn[i][0] += a
                n_turn[i][1] -= b
            elif min_num == 3:
                n_turn[i][0] -= a
                n_turn[i][1] += b
            elif min_num == 4:
                n_turn[i][0] -= a
                n_turn[i][1] -= b
        
        n_turn[i][0] = keep_in_bounds(n_turn[i][0], dims)
        n_turn[i][1] = keep_in_bounds(n_turn[i][1], dims)
        
    return n_turn
        
def keep_in_bounds(x,dims):
    if x < dims[0]:
        return dims[0]
    elif x > dims[1]:
        return dims[1]
    else:
        return x

        
def get_score(pop, lower_bound, influence_factor, func):
    temp = [ func(tup) for tup in pop ]
    normal = [ x + lower_bound for x in temp ]
    return [ x / influence_factor for x in normal ]

def get_score_one(pop, lower_bound, influence_factor, func):
    temp = func(pop)
    normal =  temp + lower_bound
    return normal / influence_factor