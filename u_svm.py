from sklearn import svm
from sklearn.model_selection import cross_val_score
import joblib
import csv
import random

gesture_number = 2

filename = 'parameters.joblib'

D = []

X_train, X_test, Y_train, Y_test = [], [], [] ,[]
# X : data  Y : label


for i in range(gesture_number):
    f_name = 'final_dataset_%d.csv' %(i+4)
    f = open(f_name, 'r')
    rdr = csv.reader(f)

    for line in rdr:
        if (len(line) != 0):
            D.append((line, i)) # save data as a (input, label) tuple

    f.close()

random.shuffle(D)
# devide data set to training set & test set
for i in range(len(D)):
    if (i % 5 == 0):
        X_test.append(D[i][0])
        Y_test.append(D[i][1])
    else:
        X_train.append(D[i][0])
        Y_train.append(D[i][1])

X = X_train + X_test
Y = Y_train + Y_test

clf1 = svm.SVC(kernel = 'linear')

scores = cross_val_score(clf1, X, Y, cv = 5)

print(scores)
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

clf = svm.SVC(kernel = 'linear').fit(X, Y)

#save the classifier parameter as a joblib file
joblib.dump(clf, filename)


