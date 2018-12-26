# temporal_association_rule_mining
Some scripts used to mine temporal association rules from event sequence data. Used in an educational data mining paper ([Madaio et al., 2017](http://educationaldatamining.org/EDM2017/proc_files/papers/paper_118.pdf)) to understand how students' collaborative learning behaviors are associated with the state of their relationship, or "rapport".


<h1>Environment Setup</h1>

1.	Install Honey, EventViewer, and Titarl on Windows computer
http://framework.mathieu.guillame-bert.com/

2.	Install Visual Studio 
https://www.visualstudio.com/

3.	Download Opencv
http://opencv.org/

4.	Follow instructions to set the OpenCV environment variable here (http://docs.opencv.org/2.4/doc/tutorials/introduction/windows_install/windows_install.html#windowssetpathandenviromentvariable)		
	- Run Command Prompt as Administrator
	- setx -m OPENCV_DIR D:\OpenCV\build\x64\vc12 (change filepath)
	- Add the dlls_1.1 files to opencv\build\x64\vc12\bin

5.	In Path Editor, Add a new path to opencv\build\bin and one to opencv\build\x64\vc12\bin
a.	Restart computer

6.	Edit environment variable to honey folder / bin




<h1>Data Preparation</h1>

1.	Create master file for events for each session to run TAR on
	- Convert the timestamps to ss:ms (e.g. 101.5)
	- Create columns for each annotation, for each person (SD_Tutor, SD_Tutee, MC_Tutor, MC_Tutee, etc)
	- Each row is the start of an event, as in annotated utterance, or nonverbal behavior
	- 1 for occurrence of annotation, 0 if not

2.	If applicable, select subset of columns to use (e.g. Tutoring-only or Social-only)





<h1>TITARL Setup</h1>

1.	Create .evt file of events (annotated behaviors and rapport ratings every 30 seconds) from master files.
	- Using “create_evt.py”

2.	Create an .sevt file for each combination of train set and test set, to use for cross-validation of the predictions.
	- Using “create_sevt.py”
	- With 6 total dyads of friends and 6 for strangers, we tried 4 dyads for train and 2 for test (15 friends and 15 strangers) and 5 train and 1 test (6 friends and 6 strangers)

3.	Create config file for each set.
	- Using “create_config.py”

4.	Create “learn_rules.bat” file, using each .sevt and config file
	- Using “write_rules.py”



<h1>Running TITARL</h1>

1.	In each model folder, make sure you have:
	- Config files (.xml)
	- .sevt files
	- .evt files
	- learn_rules.bat

2.	Run Titarl “learn_rules.bat”
	- Finds rules for each train set, create simple rules, prune, merge, refine, etc
		- Output will be “value_rules-[Relationship]#.xml”
	- Runs 7 random forest classifiers on using the rules generated from each train set to predict rapport in the test set
		- Output will be a “predictions.evt” file for each model.

3.	Create “write_predictions.tit” 
	- Using “write_predictions.py”

4.	Run “write_predictions.tit” on each predictions.evt file to generate “fuse_output_[Relationship]_#.txt”




<h1>Use output predictions</h1>

1.	Process those predictions
	- Using “Processing_predictions.java”
	- Make sure Java Environment Path is set up
	- Run javac Processing_predictions.java to get the Processing_predictions.class
	- Run java Processing_predictions.java
		- This will create an output file: “fuse_output_[Relationship]_#.csv"

2.	You could use that fuse_output_[Relationship]_#.csv as input into regression or classification model
	- Remove the “time” column
	- Remove the “reference” and value of the scalar.Rapport.
	- Compare evaluation measure (MSE, kappa, AUC, etc) between each of the rulesets generated from tutoring and social behavior against the models with rules generated from social only, or tutoring only, nonverbal only, etc.

3.	For our EDM 2017 paper, we also evaluated our approach against two baselines:
	- One using the 100+ annotated columns within each time slice as independent features in a regression / classification model
	- And another using the direct output of the random forest from TITARL (fuse_output_[Relationship]_#.csv) and taking the majority vote of the final rapport value as the output. (`baseline_comparison.py`)

4.	Alternatively, you could extract the rule details themselves to interpret the temporal sequences most associated with your outcome value (we did both the scalar value of rapport for each slice, and also the delta of that slice and the subsequent slice).
	- Using “rule_extraction.py” to get:
		- A summary of the total number of rules for each of the outcome values (e.g. “Rapport_3”)
		- The full rule sets for each model, with the rapport values, temporal sequence (e.g. “Tutee_Answer, Tutor_Praise, Tutee_Norm_Violation”), their confidence, support, number of uses, etc.
