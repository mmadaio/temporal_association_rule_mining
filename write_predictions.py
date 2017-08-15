__author__ = 'mmadaio'






## Creates a Honey file (.tit) to convert the predictions.evt event file into a .txt file

def write_predictions_tit():
    text = []
    for i in range(0,6):  ## Change value for however many files you have
        text.append("@data input:Friends_{0}\\predictions.evt output:Friends_{0}".format(i)+"\\fuse_output_Friends_{0}.txt \n \n".format(i))  ## Specifies file path for input and file name for output file
        text.append("$RESULT = echo #.*  \n \n")
        text.append("saveBufferedCsv $RESULT file:%output \n \n".format(i))

        text.append("@data input:Strangers_{0}\\predictions.evt output:Strangers_{0}".format(i)+"\\fuse_output_Strangers_{0}.txt \n \n".format(i))  ## Specifies file path for input and file name for output file
        text.append("$RESULT = echo #.*  \n \n")
        text.append("saveBufferedCsv $RESULT file:%output \n \n".format(i))

    filename = "write_predictions1.tit"
    output = "".join(text)
    print output
    batch_output = open(filename, "w")

    batch_output.write(output)
    batch_output.close()




write_predictions_tit()
