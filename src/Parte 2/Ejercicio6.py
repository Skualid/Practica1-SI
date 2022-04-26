import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import json
import graphviz

with open('JSON Ejercicios IA-20220426/users_IA_clases.json', 'r') as f:
    data_train = json.load(f)

with open('JSON Ejercicios IA-20220426/users_IA_predecir.json', 'r') as f:
    data_test = json.load(f)

matriz_train = [None] * len(data_train['usuarios'])
for i in range(len(data_train['usuarios'])):
    matriz_train[i] = [None] * 2


list_train = [None] * len(data_train['usuarios'])

i = 0
for usuario in range(len(data_train['usuarios'])):

    matriz_train[i][0] = data_train['usuarios'][usuario]['emails_phishing_recibidos']
    matriz_train[i][1] = data_train['usuarios'][usuario]['emails_phishing_clicados']

    list_train[i] =[data_train['usuarios'][usuario]['vulnerable']]

    i += 1

print(list_train)
print(matriz_train)

# Use only one feature
data_train_Y = list_train
data_train_X = matriz_train
#print(data_train_Y)

# Split the data into training/testing sets
data_X_train = data_train_X[:-20]
data_X_test = data_train_X[-20:]

# Split the targets into training/testing sets
data_y_train = data_train_Y[:-20]
data_y_test = data_train_Y[-20:]

def RegresionLinear():
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(data_X_train, data_y_train)

    # Make predictions using the testing set
    data_y_pred = regr.predict(data_X_test)

    #data_pred = regr.predict(data_X_test)

    # The coefficients
    print("Coefficients: \n", regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(data_y_test, data_y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(data_y_test, data_y_pred))

    # Plot outputs
    res = []
    for i in data_X_test:
        if i[1] == 0:
            i[1] = 1
        res.append([float(i[0]/i[1])])

    print(res)
    plt.scatter(res, data_y_test, color="black")
    plt.plot(res, data_y_pred, color="blue", linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()


def decisionTree():
    from sklearn.datasets import load_iris
    from sklearn import tree

    regr = tree.DecisionTreeClassifier()
    # Train the model using the training sets
    regr.fit(data_X_train, data_y_train)

    tree.plot_tree(regr, filled=True, fontsize=10, rounded = True, precision=2, proportion=False)
    plt.show()

def forest():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import tree

    regr = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
    # Train the model using the training sets
    regr.fit(data_X_train, data_y_train)

    print(str(data_X_train[0]) + " " + str(data_y_train[0]))
    print(regr.predict([data_X_train[0]]))

    for i in range(len(regr.estimators_)):
        print(i)
        estimator = regr.estimators_[i]
        tree.plot_tree(estimator, filled=True, fontsize=10, rounded = True, precision=2, proportion=False)
        plt.show()

forest()
#decisionTree()
#RegresionLinear()