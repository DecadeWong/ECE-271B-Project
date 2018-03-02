# ECE-271B-Project
A Git for our ECE 271B project doing Instrument Classification



To get youtube data:
	1) Get the dependencies
		get youtube-dl: sudo -H pip install --upgrade youtube-dl 
		get pydub: sudo pip install pydub
	2) Delete the old data folders data/test and data/train
	3) Use the classes.csv file to modify the classes we would like to have
	4) Run the getData.py script 
	5) The data is downloaded in data/test and data/train
    
To run audioFeatureLearning:
    1) Get the dependencies
         get skilearn
         get pyAudioAnalysis (not needed if downloaded Featureset from google drive)
    2) To generate test and training features, have train_rawAudio and test_rawAudio in data folder and have pyAudioAnalysis
    3) Or you can just download the already generated features from google drive and put them in data folder
    4) Should be good to run!