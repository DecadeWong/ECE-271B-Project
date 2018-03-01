import json
import csv
import os
import youtube_dl
# import pafy
from pydub import AudioSegment

from functions import createFolder
from functions import getClasses


def supported(url):
	ies = youtube_dl.extractor.gen_extractors()
	for ie in ies:
		if ie.suitable(url) and ie.IE_NAME != 'generic':
			# Site has dedicated extractor
			return True
	return False


def downloadYoutubeCSV(csvFilePath, tempFile, outFolder, ourClasses, youtubeClassesID, startRow=4, endRow=0):

	if os.path.exists(tempFile):
		os.remove(tempFile)

	tempName, file_extension = os.path.splitext(tempFile)

	#Now going to download the raw audio training!!!!!
	with open(csvFilePath) as file:
		reader = csv.reader(file)


		rowCount = 0
		for row in reader:
			rowCount = rowCount + 1

			#Skip the first 3 rows, do not contain what we want!!
			if rowCount < 4  or rowCount < startRow:
				continue

			if rowCount > endRow and endRow != 0 :
				break

			vidID    = row[0]
			startSec = float(row[1])
			endSec   = float(row[2])
			labelsID = row[3:]

			link = 'https://www.youtube.com/watch?v=' + vidID 
			if not supported(link):
				continue


			#See if this video is for us!!!
			for i in range(0, len(ourClasses)):
				for c in youtubeClassesID[i]:
					if c in labelsID:
						path_audio = outFolder + ourClasses[i] + "/" + vidID + ".mp3"
						
						if os.path.exists(path_audio):
							continue

						#Download Youtube Video!!
						print("Downloading " + ourClasses[i] + "( " + c + " ): " + link)

						ydl_opts = {
						'format': 'bestaudio/best',
						'outtmpl': tempName + '.%(ext)s',
						'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						'preferredcodec': 'mp3',
						}],
						'logger': MyLogger(),
						'ignoreerrors': True
						}
						

						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download([link])
						
						#Crop the audio
						if os.path.exists(tempFile):
							song = AudioSegment.from_mp3(tempFile)
							extract = song[1000*startSec: 1000*endSec]
							extract.export( path_audio , format="mp3")	
							os.remove(tempFile)


class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


def main():

	ourClasses, youtubeClasses, youtubeClassesID, labelsTF = getClasses('classes.csv', "data/ontology.json", 'data/class_labels_indices.csv')

	# ourClasses = [ourClasses[3]]
	# youtubeClasses = [youtubeClasses[3]]
	# youtubeClassesID = [youtubeClassesID[3]]
	# labelsTF = [labelsTF[3]]

	#Print to check
	for i in range(0, len(ourClasses)):
		print("Under {}".format(ourClasses[i]))
		print(youtubeClasses[i])
		print(youtubeClassesID[i])
		print(labelsTF[i])


	#Create all the folders!!!
	createFolder("data/test_rawAudio")
	createFolder("data/train_rawAudio")

	for c in ourClasses:
		createFolder("data/test_rawAudio/" + c)
		createFolder("data/train_rawAudio/" + c)

	
	#Download the raw train set
	print("====Downloading Train Data====")
	downloadYoutubeCSV("data/unbalanced_train_segments.csv", "data/temp_train4.mp3", "data/train_rawAudio/", ourClasses, youtubeClassesID, startRow=500000)

	return

	#Download the raw test set
	print("====Downloading Test  Data====")
	downloadYoutubeCSV("data/eval_segments.csv", "data/temp_test.mp3", "data/test_rawAudio/", ourClasses, youtubeClassesID)


	
if __name__== "__main__":
  main()
