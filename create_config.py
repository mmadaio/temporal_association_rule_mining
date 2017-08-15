__author__ = 'mmadaio'


import csv

import os
import shutil
import xml.etree.ElementTree as ET



def change_config():
    config = "Config_files"
    source = "original"
    source_folder = config + "/" + source
    print source_folder

    num_files = 15 ## Change this to the number of files generated for each Relationship (e.g. 6 (total) choose 4 (train) is 15)

    models = ["test"] #test["T","T_S_NV", "NV","S","T_NV","S_NV","T_S"]

    folder = next(os.walk(config))[2]


    ## Make a set of copies of the Config xml

    for j in range(len(models)):
        directory = "Config_files/" + models[j]

        if not os.path.exists(directory):
            print directory
            os.makedirs(directory)

        for file in os.listdir(source_folder):
            if not file.startswith(".DS"):
                #print file
                f = config + "/" + models[j] + "/" + file
                file = source_folder + "/" + file
                #print f

                for i in range(0,num_files):
                    new_name = f.replace(".xml", "{0}.xml".format(i))

                #    print new_name
                    shutil.copy(file, new_name)


        ## Change the filenames within each of the copies

        for file in os.listdir(directory):
            if not file.startswith(".DS"):
                file = directory + "/" + file
                print file
                type = file.split("_")[3]
                print type

                groups = ["friends","strangers"]

                for g in range(len(groups)):
                    print groups[g][0]
                    if type[0] == groups[g][0]:
                        print type[0]
                        ending = type.strip(".xml")

                        doc = ET.parse(file)
                        root = doc.getroot()
                        print root

                        ## Change name for .xml rules file
                        for atype in root.findall('option'):
                            name = atype.get('value')
                            print atype
                            if name.endswith(".xml"):

                                name1 = name.replace("{0}.xml".format(groups[g]), "{0}.xml".format(ending))
                                atype.attrib["value"] = name1
                                print name1


                        ## Change name for .sevt file
                        for atype in root.findall('data'):
                            name = atype.get('path')
                            if name.endswith(".sevt"):
                                name1 = name.replace("train_set.sevt", "train_set_{0}.sevt".format(ending))
                                atype.attrib["path"] = name1
                                print name
                        tree = ET.ElementTree(root)
                        tree.write(file)




change_config()