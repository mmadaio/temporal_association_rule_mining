__author__ = 'mmadaio'




def write_learn_rules():

    ## If you have multiple behavioral models to run, define the model names
    models = ["test"] #['NV',"S","T_NV","S_NV","T_S", "T", "T_S_NV"]


    ## Creates a batch file to use to run

    filename = "learn_rules.bat"
    print filename
    text = []

    for j in range(len(models)):
        print models[j]

        text.append("cd {0} \n \n".format(models[j]))

        ## For all of your n combinations of files, for both groups (Friend and Stranger):

        for i in range(0,6):
            text.append("titarl --learn learn_rules_friends{0}.xml \n \n".format(i))  ## The actual Titarl learn_rules command for each XML config file
            text.append("titarl --learn learn_rules_strangers{0}.xml \n \n".format(i))  ## The actual Titarl learn_rules command for each XML config file

        for i in range(0,6):
            text.append("mkdir Friends_{0} \n \n".format(i))  ## Create new directory for this group
            text.append("mkdir Strangers_{0} \n \n".format(i))
            text.append("titarl --computeFusionStats value_rules-friends{0}.xml --database friends_train_set_{0}.sevt --output Friends_{0}/tmpFusioRecord --request_symbols %%rule_heads%% --request_horizon 0 --request_length 30 --sparsematrix 0 --binary 1 --raw scalar\\.Rapport \n \n".format(i))  ## Runs the Titarl rule fusion command
            text.append("titarl --computeFusionStats value_rules-strangers{0}.xml --database strangers_train_set_{0}.sevt --output Strangers_{0}/tmpFusioRecord --request_symbols %%rule_heads%% --request_horizon 0 --request_length 30 --sparsematrix 0 --binary 1 --raw scalar\\.Rapport \n \n".format(i))   ## Runs the Titarl rule fusion command
            text.append("titarl --applyFusionStats value_rules-friends{0}.xml --database friends_test_set_{0}.sevt --output Friends_{0}/predictions --model randomForest --fusionRecord Friends_{0}/tmpFusioRecord --threshold 10 --sparsematrix 0 \n \n".format(i))       ## Runs the Titarl random forest for rapport prediction
            text.append("titarl --applyFusionStats value_rules-strangers{0}.xml --database strangers_test_set_{0}.sevt --output Strangers_{0}/predictions --model randomForest --fusionRecord Strangers_{0}/tmpFusioRecord --threshold 10 --sparsematrix 0 \n \n".format(i))   ## Runs the Titarl random forest for rapport prediction

        text.append("cd .. \n \n")

    output = "".join(text)
    print output
    batch_output = open(filename, "w")

    batch_output.write(output)
    batch_output.close()




write_learn_rules()
