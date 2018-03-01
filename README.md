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