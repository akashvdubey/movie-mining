# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 13:09:06 2017

@author: Steff
"""

import ClassifierTemplate as ct
import pandas as pd

data = pd.read_csv("../../data/processed/train_set.csv", index_col=0)

# DataFrame containing label (!)
df = pd.DataFrame(data)

label_column = "productivity_binned_binary"

# Build Classifier object with DataFrame and column name of truth values
c = ct.Classifier(df,label_column)

### drop single columns not needed for Classification
c.dropColumns([
        "original_title"
        #,"adult"
        #,"belongs_to_collection"
        #,"budget"
        #,"runtime"
        #,"year"
        ,"quarter"
        ,"productivity_binned_multi"
        #,"productivity_binned_binary"
])

### scale something if needed
#c.scale([
#        "budget"
#])

### drop columns by prefix if needed
#c.dropColumnByPrefix("actor")
#c.dropColumnByPrefix("director")
#c.dropColumnByPrefix("company")
#c.dropColumnByPrefix("country")
#c.dropColumnByPrefix("genre")
#c.dropColumnByPrefix("quarter_")

# lets print all non-zero columns of a movie to doublecheck
df = c.data.loc[19898]
df = df.iloc[df.nonzero()[0]]
print(df)
print(c.data.columns)

# get information about the data
c.balanceInfo()

# get parameters for GridSearch
scorer = c.f1(average="macro") # use F1 score with micro averaging
estimator = c.neuralnet() # get kNN estimator
cv = c.fold(
        k=2
        ,random_state=42
) # KStratifiedFold with random_state = 42
# parameters to iterate in GridSearch
parameters = {
    "solver":[
            #"lbfgs" # an optimizer in the family of quasi-Newton methods.
            #"sgd" # refers to stochastic gradient descent.
            "adam" # refers to a stochastic gradient-based optimizer proposed by Kingma, Diederik, and Jimmy Ba
     ]
    ,"hidden_layer_sizes":[ # tuple, length = n_layers - 2, default (100,). The ith element represents the number of neurons in the ith hidden layer.
            (100,)
            #,(50,)
    ]
    ,"activation":[
            #"identity" # no-op activation, useful to implement linear bottleneck, returns f(x) = x
            #"logistic" # the logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x))
            #,"tanh" # the hyperbolic tan function, returns f(x) = tanh(x)
            "relu" # the rectified linear unit function, returns f(x) = max(0, x)
    ]
    ,"alpha":[ # L2 penalty (regularization term) parameter. float, optional, default 0.0001
            0.0001
    ]
    ,"max_iter":[ # int, optional, default 200. Maximum number of iterations. The solver iterates until convergence (determined by ‘tol’) or this number of iterations. For stochastic solvers (‘sgd’, ‘adam’), note that this determines the number of epochs (how many times each data point will be used), not the number of gradient steps.
            200
            #,1000
    ]
    ,"random_state":[42]
    # parameter can be used to tweak parallel computation / n = # of jobs
    #,"n_jobs":[1]
}

features = [
            "adult",
            "belongs_to_collection",
            "budget",
            "runtime",
            "year",
            "actor_",
            "director_",
            "company_",
            "country_",
            "genre_",
            "quarter_"
]

# compute FeatureSelect
gs = c.featureselect_greedy(
        features
        ,parameters
        ,scorer
        ,estimator
        ,cv
        ,label_column
)

#print(gs)