import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import copy
from matplotlib import animation
from Fireflies.functions import *
from Fireflies.turn import *
from app.models import FireflyPopulation, FireflyAgent


def go(nturns, num_worms, influence_factor, max_jitter, start, end, function, population):
    #params = FireflyPopulation.objects.create(nturns = nturns, num_worms = num_worms,influence_factor=influence_factor, max_jitter=max_jitter, start=start,end=end, function=function)
    if(function == 'Растригина'):
        fitness_function = rastrigin
    elif(function == 'Экли'):
        fitness_function = ekli
    elif(function == 'Де Джонга'):
        fitness_function = de_djonga
    elif(function == 'Розенброка'):
        fitness_function = rozenbrok

    fi = influence_factor/100
    dims = [start, end]
    lower_bound = 70
    influence_factor = 4
    flag = True

    plt.rcdefaults()

    x = np.arange(dims[0], dims[1] + 0.1, 0.1)
    y = np.arange(dims[0], dims[1] + 0.1, 0.1)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = fitness_function([xx, yy])

    figura, ax = plt.subplots()
    plt.axes(xlim=(dims[0], dims[1]), ylim=(dims[0], dims[1]))
    plt.pcolormesh(x, y, z, shading='gouraud', cmap=cm.gray)
    plt.imshow(z, interpolation='bilinear', origin='lower', cmap=cm.gray, extent=(dims[0], dims[1], dims[0], dims[1] ))
    plt.colorbar()

    pop = starting_points(num_worms, dims)

    flyworms = [pop]
    colors = []
    colors.append(fitness_function([flyworms[0][:,0], flyworms[0][:,1]]))

    

    for i in range(nturns-1):
        score = get_score(flyworms[i], lower_bound, influence_factor, fitness_function)
        im = influence_matrix(pop, score, num_worms, fitness_function)
        pop = copy.deepcopy(next_turn(pop, score, im, num_worms, max_jitter, dims, lower_bound, influence_factor, fitness_function, fi))
        flyworms += [pop]
        colors.append(fitness_function([flyworms[i+1][:,0],flyworms[i+1][:,1]]))

    def Save(flyworms, colors):
        for i in range(nturns):
            for j in range(num_worms):
                FireflyAgent.objects.create(x = flyworms[i][j, 0], y = flyworms[i][j, 1], z = colors[i][j], population_id = population, agent_id = j)
    Save(flyworms, colors)

    def an(i):
        plt.clf()
        plt.axes(xlim=(dims[0], dims[1]), ylim=(dims[0], dims[1]))
        plt.pcolormesh(x, y, z, shading='gouraud', cmap=cm.gray)
        plt.colorbar()
        plt.imshow(z, interpolation='bilinear', origin='lower', cmap=cm.gray, extent=(dims[0], dims[1], dims[0], dims[1] ))
        plt.scatter(flyworms[i][:,0], flyworms[i][:,1], c=colors[i]).set_offsets(list(zip(flyworms[i][:,0], flyworms[i][:,1])))
        plt.title('iteration: {}'.format(i), loc='right')
        
    ani = animation.FuncAnimation(figura, an, fargs=(), frames=nturns, interval=20 ,repeat=False) 
    if flag:
        #ani.save('animation.gif', writer='imagemagick', fps=12)
        ani.save('app/templates/Fireflies/animation.html', writer=animation.HTMLWriter(embed_frames=True))
    #print(10)
    #print(colors[nturns-1])
    nmax = np.argmin(colors[nturns-1])
    #print(nmax)
    #print(flyworms[nturns-1][nmax, 0])
    #print(flyworms[nturns-1][nmax, 1])
    #print(colors[nturns-1][nmax])
    print([flyworms[nturns-1][nmax, 0], flyworms[nturns-1][nmax, 1], colors[nturns-1][nmax]])
    return np.round([flyworms[nturns-1][nmax, 0], flyworms[nturns-1][nmax, 1], colors[nturns-1][nmax]], 4)
    #plt.show()
