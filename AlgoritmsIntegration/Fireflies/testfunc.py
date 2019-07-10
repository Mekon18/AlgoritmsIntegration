from math import *
import numpy as np

def function(xy_tuple):
    x = xy_tuple[0]
    y = xy_tuple[1]
    #return np.sin(x**3+ (y-5)**3) + np.cos((y-5)**2) *10 + np.cos(x*2) * 12 * (y-5)
    return np.sin(x + y) * 3


def ekli(x):#+
    return -20*np.exp(-0.2*np.sqrt(0.5*np.sum(i**2 for i in x))) - \
           np.exp(0.5*np.sum(np.cos(i) for i in x)) + 20 + exp(1)

def de_djonga(x):
    return np.sum(np.power(i, 2) for i in x)


def rastrigin(x):
    return 20 + np.sum((np.power(i, 2) - 10*np.cos(2*np.pi *i)) for i in x)

def rozenbrok(x):
    return 100 * (x[1] - x[0]**2)**2 + (x[0] - 1)**2




def bukin_function(x):#+
    return 100*np.sqrt(np.abs(x[1]-0.01*x[0]**2)) + 0.01*np.abs(x[0] + 10)


def cross_in_tray_function(x):#+
    return np.round(-0.0001*(np.abs(np.sin(x[0])*np.sin(x[1])*np.exp(np.abs(100 - \
                            np.sqrt(np.sum(i**2 for i in x))/pi))) + 1)**0.1, 7)


def sphere_function(x):
    return sum([i**2 for i in x])


def bohachevsky_function(x):
    return x[0]**2 + 2*x[1]**2 - 0.3*cos(3*pi*x[0]) - 0.4*cos(4*pi*x[1]) + 0.7


def sum_squares_function(x):
    return sum([(i+1)*x[i]**2 for i in range(len(x))])


def sum_of_different_powers_function(x):
    return sum([abs(x[i])**(i+2) for i in range(len(x))])


def booth_function(x):
    return (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2


def matyas_function(x):
    return 0.26*sphere_function(x) - 0.48*x[0]*x[1]


def mccormick_function(x):
    return np.sin(x[0] + x[1]) + (x[0] - x[1])**2 - 1.5*x[0] + 2.5*x[1] + 1


def dixon_price_function(x):
    return (x[0] - 1)**2 + np.sum([(i+1)*(2*x[i]**2 - x[i-1])**2
                                for i in range(1, len(x))])


def six_hump_camel_function(x):
    return (4 - 2.1*x[0]**2 + x[0]**4/3)*x[0]**2 + x[0]*x[1]\
           + (-4 + 4*x[1]**2)*x[1]**2


def three_hump_camel_function(x):
    return 2*x[0]**2 - 1.05*x[0]**4 + x[0]**6/6 + x[0]*x[1] + x[1]**2


def easom_function(x):
    return -cos(x[0])*cos(x[1])*exp(-(x[0] - pi)**2 - (x[1] - pi)**2)


def michalewicz_function(x):
    return -sum([sin(x[i])*sin((i+1)*x[i]**2/pi)**20 for i in range(len(x))])


def beale_function(x):
    return (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + \
           (2.625 - x[0] + x[0]*x[1]**3)**2


def drop_wave_function(x):
    return -(1 + cos(12*sqrt(sphere_function(x))))/(0.5*sphere_function(x) + 2)

