__author__ = 'mmadaio'

import os
import csv
import xml.etree.ElementTree as ET
import codecs


main = "input/delta/"
path = ['T_S_NV'] #'NV', 'T_S_NV','T_NV','S_NV', 'T_S','S','T']
paths = []
relationship = []

fold = []
conditions = []
total_rules = []
len_rapport1 = []
len_rapport2 = []
len_rapport3 = []
len_rapport4 = []
len_rapport5 = []
len_rapport6 = []
len_rapport7 = []

def process_subtree(c, conditions):
    name = c.get('symbol') if c.tag == 'condition' else None
    negation = c.get('negation') if c.tag == 'condition' else None
    if negation:
        if negation == "1":
            name = name + "_negative"
    if name:
      conditions.append(name)

    for c1 in c:
      process_subtree(c1, conditions)


def rule_summary(file):
    print f[12]
    paths.append(p)
    relationship.append(f[12])

    if f[12] == "f":
        fold.append(f[19:].strip(".xml"))
    elif f[12] == "s":
        fold.append(f[21:].strip(".xml"))

    rapport_values = []
    rapport1 = []
    rapport2 = []
    rapport3 = []
    rapport4 = []
    rapport5 = []
    rapport6 = []
    rapport7 = []
    doc = ET.parse(file)
    root = doc.getroot()

    numRules = root.get('numberOfRules')
    print "Total number of rules in this fold:"
    print numRules + "\n"
    total_rules.append(numRules)
    for atype in root.findall('rule'):
        rapport_value = atype.get('head')
        rapport_value = rapport_value[14:]
        rapport_values.append(rapport_value)
    print rapport_values
    for r in rapport_values:
        if r == "1":
            rapport1.append(r)
        elif r == "2":
            rapport2.append(r)
        elif r == "3":
            rapport3.append(r)
        elif r == "4":
            rapport4.append(r)
        elif r == "5":
            rapport5.append(r)
        elif r == "6":
            rapport6.append(r)
        elif r == "7":
            rapport7.append(r)
    len_rapport1.append(len(rapport1))
    len_rapport2.append(len(rapport2))
    len_rapport3.append(len(rapport3))
    len_rapport4.append(len(rapport4))
    len_rapport5.append(len(rapport5))
    len_rapport6.append(len(rapport6))
    len_rapport7.append(len(rapport7))


    print paths, relationship, fold
    print total_rules
    print len_rapport1
    print len_rapport7





def extract_rules(file):


    rule_num = []
    rapport_val = []
    conf = []
    supp = []
    numUses = []
    numEvents = []
    numPredicts = []
    numCond = []
    conditions_ = []
    paths_ = []
    relationship_ = []
    fold_ = []
    print f[12]

    count = 0
    doc = ET.parse(file)
    root = doc.getroot()

    numRules = root.get('numberOfRules')
    print "Total number of rules in this fold:"
    print numRules + "\n"

    for atype in root.findall('rule'):
        paths_.append(p)
        relationship_.append(f[12])

        if f[12] == "f":
            fold_.append(f[19:].strip(".xml"))
        elif f[12] == "s":
            fold_.append(f[21:].strip(".xml"))
        count += 1
        rapport_value = atype.get('head')
        confidence = atype.get('confidence')
        support = atype.get('support')
        number_of_use =  atype.get('number_of_use')
        number_of_events_to_predict = atype.get('number_of_events_to_predict')
        number_of_events_predicted = atype.get('number_of_events_predicted')

        print "Rule {0}:".format(count)
        rule_num.append(count)
        rapport_value = rapport_value[14:]
        print rapport_value + "\n"
        rapport_val.append(rapport_value)
        print "Confidence: " + confidence + "\nSupport: " + support + "\nUses of this rule: " + number_of_use + "\nNumber of events with this rapport value: " + number_of_events_to_predict + "\nNumber of rapport value events successfully predicted: " + number_of_events_predicted + "\n"
        conf.append(confidence)
        supp.append(support)
        numUses.append(number_of_use)
        numEvents.append(number_of_events_to_predict)
        numPredicts.append(number_of_events_predicted)
        conditions = []
        conditions_.append(conditions)
        process_subtree(atype, conditions)
        num_conditions = len(conditions)
        print "Rule body:"
        print conditions
        print "Number of conditions:"
        print num_conditions
        numCond.append(num_conditions)

        print "Total number of rapport slices:"


        print "------------------------------------------------------------------------------------------------\n\n\n"



    output1 = zip(paths_, relationship_,fold_,rule_num, rapport_val,conf, supp, numUses, numEvents, numPredicts, numCond, conditions_)

    with codecs.open("output/delta/{0}/{1}_extracted_rule_details.csv".format(p, f), 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow(["Model","Relationship","Fold","Rule ID","Rapport Value","Confidence", "Support","Number of Uses", "Num Events to Predict", "Num Events Predicted", "Number of Conditions","Conditions"])
            for row in output1:
                 a.writerow(row)









for p in path:
    print p
    data_path = main + p + "/"
    for f in os.listdir(data_path):
        if  not f.startswith(".DS"):
            print f + "\n"
            file = data_path + f
           # rule_summary(file)
            extract_rules(file)



output = zip(paths, relationship,fold,total_rules, len_rapport1, len_rapport2, len_rapport3, len_rapport4,len_rapport5,len_rapport6,len_rapport7)

with codecs.open("rule_summary.csv", 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(["Model","Relationship","Fold","TotalNum Rules","Rapport 1", "Rapport 2", "Rapport 3", "Rapport 4", "Rapport 5", "Rapport 6", "Rapport 7"])
        for row in output:
             a.writerow(row)

