# This script uses the Sequential model within Keras to implement 
# a simple one-hidden-layeer neural network 

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import regularizers
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from keras.constraints import maxnorm
from sklearn.model_selection import GridSearchCV
import numpy as np
import pdb

np.random.seed(10) # for reproducability

def one_hot(y, num_classes):
    onehot = np.zeros((y.shape[0], num_classes))
    onehot[np.arange(y.shape[0]), y] = 1
    return onehot

def load_data():
    # Load data X and labels y
    X = np.load('../datasets/kings_05_rapideye/train_data_single.npy')
    X = X*1.0/np.max(X) # normalize to 1
    y = np.load('../datasets/kings_05_rapideye/train_lbl_sc.npy')
    y = np_utils.to_categorical(y)

    X_dev = np.load('../datasets/kings_05_rapideye/val_data_single.npy')
    X_dev = X_dev*1.0/np.max(X_dev) # normalize to 1
    y_dev = np.load('../datasets/kings_05_rapideye/val_lbl_sc.npy')
    y_dev = np_utils.to_categorical(y_dev)

    X_test = np.load('../datasets/kings_05_rapideye/test_data_single.npy')
    X_test = X_test*1.0/np.max(X_test) # normalize to 1
    y_test = np.load('../datasets/kings_05_rapideye/test_lbl_sc.npy')
    y_test = np_utils.to_categorical(y_test)
    return X, y, X_dev, y_dev, X_test, y_test

def create_model(units, activation, loss, optimizer, metrics, reg, dropout_rate, weight_constraint):
    # Model parameters / layers should be tuned for better performance
    # Define model as a sequence of layers; Dense models are fully-connected models
    model = Sequential()
    model.add(Dense(units=units, input_dim=5, activation=activation, kernel_regularizer=regularizers.l2(reg), kernel_constraint=maxnorm(weight_constraint)))
    #model.add(Dense(units=units, input_dim=75, activation=activation, kernel_regularizer=regularizers.l2(reg), kernel_constraint=maxnorm(weight_constraint)))
    #model.add(Dense(units=units, input_dim=105, activation=activation, kernel_regularizer=regularizers.l2(reg), kernel_constraint=maxnorm(weight_constraint)))
    model.add(Dropout(dropout_rate))
    #model.add(Dense(6, activation='softmax'))
    model.add(Dense(9, activation='softmax'))
    model.compile(optimizer, loss, metrics)
    return model

def fit_model(model, X, y, epochs=30, batch_size=1000):
    # Fit the model
    return model.fit(X, y, epochs, batch_size)

def evaluate_model(model, X, y, X_dev, y_dev, X_test, y_test):
    # Evaluate the model
    scores = model.evaluate(X, y)
    print('\n%s: %.2f%%' % (model.metrics_names[1], scores[1]*100))
    
    # Tune parameters to adjust to the validation performance
    val_scores = model.evaluate(X_dev, y_dev)
    print('\n%s: %.2f%%' % (model.metrics_names[1], val_scores[1]*100))

    # DO NOT tune parameters based on test scores. This should be run once the 
    #  model is defined to give an unbiased measure of performance
    test_scores = model.evaluate(X_test, y_test)
    print('\n%s: %.2f%%' % (model.metrics_names[1], test_scores[1]*100))
    return scores, val_scores, test_scores

def predict(model, X, y, X_dev, y_dev, X_test, y_test):
    # Make predictions
    pred_y = model.predict(X)
    pred_y_dev = model.predict(X_dev)
    pred_y_test = model.predict(X_test)
    
    #print(predictions)
    return pred_y, pred_y_dev, pred_y_test

def main():
    X, y, X_dev, y_dev, X_test, y_test = load_data()
    
    for units in [200]: # controls the number of neurons in the hidden layer
        model = create_model(units=units, activation='relu', loss='categorical_crossentropy', optimizer='Adadelta', 
            metrics=['accuracy'], reg=0.00001, dropout_rate=0.1, weight_constraint=5) #, verbose=0)
        print('------------------------')
        for epoch in [50, 100]:
            for batch in [1000]:
                print('batch: %s' % (batch))
                print('epoch: %s' % (epoch))
                model.fit(X, y, batch, epoch)
                scores, val_scores, test_score = evaluate_model(model, X, y, X_dev, y_dev, X_test, y_test)
    
    #pred_y, pred_y_dev, pred_y_test = predict(model, X, y, X_dev, y_dev, X_test, y_test)

    # Summarize results
    #print('Best: %f using %s' % (grid_result.best_score_, grid_result.best_params_))
    #means = grid_result.cv_results_['mean_test_score']
    #stds = grid_result.cv_results_['std_test_score']
    #params = grid_result.cv_results_['params']
    #for mean, stdev, param in zip(means, stds, params):
    #    print('%f (%f) with %r' % (mean, stdev, param))

if __name__ == '__main__':
    main()
