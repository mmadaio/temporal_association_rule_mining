__author__ = 'mmadaio'

import itertools
import os, errno

def write_sevt():

    ## If applicable, indicate which of your data are friends or strangers, and how many dyads and sessions for each

    groups = ["friends", "strangers"]
    friends = [2,3,4,10,13,16]
    strangers = [1,7,8,9,14,15]
    num_dyads = 6  # total number of dyads in each group
    num_sessions = 5   # number of sessions for each dyad



    ## Indicate the total the number of each in the train set and test set
    sets = ["train", "test"]
    train_num = 5  # number to choose for train set
    test_num = 1   # number to choose for test set


    ## For Friends and Stranger groups:
    for g in range(len(groups)):
        if g == 0:
            group = friends
        else:
            group = strangers


        ## Generate the combinations of dyad indices in the train and test set

        train_list = list(itertools.combinations(group,train_num))
        test_list = list(itertools.combinations(group,test_num))[::-1]


        ## For each of the train and test sets:
        for t in range(len(sets)):
            print groups[g]
            print sets[t]

            if sets[t] == "train":
                this_list = train_list
                this_set_length = train_num
            elif sets[t] == "test":
                this_list = test_list
                this_set_length = test_num


            ## Write the name of each file (e.g. Dyad1_Session2 --> d1s2.evt)
            for m in range(0,num_dyads):

                output = "basepath relative \n \nminoffset 86400\n"
                template = "sequence %s \ndataset d%ss%s.evt \nflush\n\n"

                s = 1
                k = 1
                l = 1

                total_num = num_sessions * this_set_length

                print total_num
                for i in range(1,total_num+1):

                    if s > num_sessions:
                        s = 1
                    if l == num_dyads:
                        k += 1
                        l = 1

                    d = this_list[m][k-1]
                   # print d

                    output += template % (i, d, s)
                    s+= 1
                    l +=1
                #    print output
               # print output



                ## Opens a csv file to write the output to.

                try:
                    os.makedirs("sevt")
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                filename = "sevt/{0}_{1}_set_{2}.sevt".format(str(groups[g]), sets[t], m)
                print filename
                sevt = open(filename, "w")
                sevt.write(output)
                sevt.close()



write_sevt()


