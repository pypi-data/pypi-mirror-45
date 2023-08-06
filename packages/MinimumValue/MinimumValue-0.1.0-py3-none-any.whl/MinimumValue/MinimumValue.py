'''Finds a value of x that minimizes a polynomial function.
This module uses gradient descent which is an optimization algorithm.
In machine learning, we use gradient descent to update the parameters of our model.
The module has one class called Gradient Descent. 
The attributes of the class are listed below:

 Attributes
----------
function: Function which we want to minimize.
symbl: Variable of the function
drev : The derivative of the function.
stp : Size of steps in gradient descent
minX : A value of x that minimizes the polynomial functions
'''

import sympy as sy
import numpy as np

class Gradient_Descent(object):
    '''Parent Class For Finding the minimum value of x.'''

    def __init__(self,function,symbl):
        self.function = function
        self.symbl = symbl
        self.drev = None
        self.stp = None
        self.minX = None
        self.x = None
        self.arrange = None

    def parse(self):
        '''parse the function and symbol
   
            Parameters
        ----------
            function: string
                A Function which we want to minimize.
            symbl: string
                Defining a variable
        '''

    def drv(self):
        '''Finding a derivative of the function by calling the "diff" function

        ----------
            x = string
                Variable's symbol
            Returns
        -------
            drev : string
                The derivative of the function.
        '''
        self.x = sy.Symbol(self.symbl)
        expr = sy.sympify(self.function)
        self.drev = expr.diff(self.x)
        return self

    def optimal_step(self):
        '''Finding the best step size for gradient descent
            Returns
        -------
            stp : integer
                The derivative of the function.
        '''
        self.stp = 0.2
        return self

    def optimal_range(self):
        '''Setting a range for checking distances'''
        self.arrange = np.arange(26)
        return self


    def MinimumX(self):
        ''' 1. Initializes the weights.
            2. Computes Gradient 
            3. While criteria don't meet updates weights
            4. Returns the final weights once reached the stopping criteria.
   
            Parameters
        ----------
            drev : string
                The derivative of the function.

            stp : float
                Step proportion 

            Returns
        -------
            minX : float
                A value of x that minimizes the polynomial function
        '''
        w = 11  
        self.x = sy.Symbol(self.symbl)
        for s in (self.arrange):
            w = w - (self.stp*(self.drev.subs(self.x,w)))
            self.minX = w
        return self
    