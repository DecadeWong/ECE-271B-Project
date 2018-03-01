from pydub import AudioSegment
from functions import getClasses



def main():
	ourClasses, _, _, _ = getClasses('classes.csv', "data/ontology.json", 'data/class_labels_indices.csv')

	for c in ourClasses:
		listOfFiles = os.listdir('data/train/rawAudio/' + c)

		for file in listOfFiles:
			song = AudioSegment.from_mp3(file)

	
if __name__== "__main__":
  main()
