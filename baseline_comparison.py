__author__ = 'mmadaio'
import os
import pandas as pd
import codecs
import csv
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import recall_score
from itertools import cycle
from sklearn.preprocessing import label_binarize


main = "input/values/"
path = ['T_S_NV','T','NV','S_NV', "T_NV", 'T_S',"S"]


relationship = []
fold = []
paths = []

maes = []
mses = []

auc_high = []
auc_low = []
auc_neutral = []
avg_auc = []


def baseline_conf(file):
    print f[12]
    paths.append(p)

    if f[12] == "F":
        this_relationship = "F"
        this_fold = (f[20:].strip(".csv"))
    elif f[12] == "S":
        this_relationship = "S"
        this_fold = (f[22:].strip(".csv"))
    relationship.append(this_relationship)
    fold.append(this_fold)



    df = pd.read_csv(file, header=0, delimiter=",")
    df1 = df.ix[:,1:] # remove initial column
    X = df1.iloc[:, 1::2] # remove reference columns
   # print X
    #print df.label
    X = pd.concat([X,pd.DataFrame(columns=['Low','Neutral','o_High'])])
    print X
    low = X.ix[:,3:6]
    neut = X.ix[:,6:7]
    high = X.ix[:,7:10]

    for i in range(len(X)):
        largest_low = low.values[i].max()
        X.Low.values[i] = largest_low

        largest_neut = neut.values[i].max()
        X.Neutral.values[i] = largest_neut

        largest_high = high.values[i].max()
        X.o_High.values[i] = largest_high


    print X


    #predicted = pd.DataFrame({n: X.T[col].nlargest(1).index.tolist()
     #             for n, col in enumerate(X.T)}).T

    df.loc[df.label > 4, 'label'] = "high"
    df.loc[df.label < 4, 'label'] = "low"
    df.loc[df.label == 4, 'label'] = "neutral"

    predicted = X.ix[:,0:3]

    print predicted

    y =  label_binarize(df.label,classes=["low","neutral","high"])
    #p =  label_binarize(df.label,classes=["low","neutral","high"])

    print "SCORE:"
    print average_precision_score(y, predicted, average='micro', sample_weight=None)



    colors = cycle(['navy', 'turquoise', 'darkorange'])
    lw = 2

    n_classes = 3
    precision = dict()
    recall = dict()
    average_precision = dict()
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    acc = dict()

    Y_test = y
    y_score = predicted


    print y_score
    i = 0
    while i in range(0,n_classes):
        print "starting with class:"
        print i

        precision[i], recall[i], _ = precision_recall_curve(Y_test[:, i],
                                                            y_score.ix[:, i])
        average_precision[i] = average_precision_score(Y_test[:, i], y_score.ix[:, i])

        print "average precision:"
        print average_precision[i]

        if i == 0:
            auc_low.append(average_precision[i])
        elif i == 1:
            auc_neutral.append(average_precision[i])
        elif i == 2:
            auc_high.append(average_precision[i])

        i += 1
        print "AUC low, neutral, high"
        print auc_low, auc_neutral, auc_high




    # Compute micro-average ROC curve and ROC area
   # precision["micro"], recall["micro"], _ = precision_recall_curve(Y_test.ravel(),
    #    y_score.ravel())
    average_precision["micro"] = average_precision_score(Y_test, y_score,
                                                         average="micro")
    avg_auc.append(average_precision["micro"])
    print "AUC:"
    print avg_auc






for p in path:
    data_path = main + p + "/"
    for f in os.listdir(data_path):
        if not f.startswith(".DS"):
            print f
            file = data_path + f
            baseline_conf(file)
          #  baseline_independent(file)

output = zip(paths, relationship,fold,avg_auc,auc_low,auc_neutral,auc_high)

with codecs.open("Baseline_AUC.csv", 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow(["Model","Relationship","Fold","Average PR AUC","PR AUC Rapport Low", "PR AUC Rapport Neutral", "PR AUC Rapport High"])
    for row in output:
         a.writerow(row)
