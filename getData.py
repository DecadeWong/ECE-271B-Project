import json
import csv
import os
import youtube_dl
import pafy
from pydub import AudioSegment

def createFolder(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return

def supported(url):
	ies = youtube_dl.extractor.gen_extractors()
	for ie in ies:
		if ie.suitable(url) and ie.IE_NAME != 'generic':
			# Site has dedicated extractor
			return True
	return False

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


def main():

	#This is in seconds the maximum video length we want to download..
	#Cropping happens after download so decreasing this will speed up download
	#but decrease datasize
	maxVideoLength = 600

	#Create all the folders!!!
	createFolder("data/test")
	createFolder("data/test/featureCNN")
	createFolder("data/test/rawAudio")
	createFolder("data/train")
	createFolder("data/train/featureCNN")
	createFolder("data/train/rawAudio")


	ourClasses     = [];
	youtubeClasses = [];

	#Open class csv file
	with open('classes.csv') as class_csvFile:
		classReader = csv.reader(class_csvFile)

		firstRow = True
		#Each row in the file is one of our classes
		for row in classReader:

			#skip first row!
			if(firstRow):
				firstRow = False
				continue


			tempYoutubeClass = []

			firstC = True
			#Go through classes in the row
			for c in row:

				#First element is our class name
				if(firstC):
					#Make folder for train rawAudio
					createFolder("data/train/rawAudio/" + c)

					#Make folder for train featureCNN
					createFolder("data/train/featureCNN/" + c)

					#Make folder for test rawAudio
					createFolder("data/test/rawAudio/" + c)

					#Make folder for test featureCNN
					createFolder("data/test/featureCNN/" + c)

					ourClasses.append(c)

					firstC = False
					continue

				#These c classes are the ones we will find on youtube/CNN now!!!
				if c:
					tempYoutubeClass.append(c)

			youtubeClasses.append(tempYoutubeClass)



	#Now time to get id from the youtubeClasses
	youtubeClassesID =[]

	with open("data/ontology.json") as ontology_data:
		ontology_json = json.load(ontology_data)

		for classList in youtubeClasses:
			#Use this list to check!!!
			check = list(classList)
			tempYoutubeClassesID = [];

			#Go through the json files looking for the youtube classes
			for yClass in ontology_json:

				if yClass["name"] in classList:
					tempYoutubeClassesID.append(yClass["id"])
					check.remove(yClass["name"])

			if len(check):
				print("Could not find elements {}".format(check))

			youtubeClassesID.append(tempYoutubeClassesID)


	for i in range(0, len(ourClasses)):
		print("Under {}".format(ourClasses[i]))
		print(youtubeClasses[i])
		print(youtubeClassesID[i])


	#Now going to download the raw audio training!!!!!
	with open("data/balanced_train_segments.csv") as train_file:
		trainReader = csv.reader(train_file)

		rowCount = 0
		for row in trainReader:
			rowCount = rowCount + 1

			#Skip the first 3 rows, do not contain what we want!!
			if rowCount < 4 :
				continue

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
						path_audio = "data/train/rawAudio/" + ourClasses[i] + "/" + vidID + ".mp3"
						if os.path.isfile(path_audio):
							continue

						#Download Youtube Video!!
						print("Downloading " + ourClasses[i] + "( " + c + " ): " + link)

						#use pafy to check duration!!!
						video = pafy.new(link)
						if( video.length > maxVideoLength):
							break

						ydl_opts = {
						'format': 'bestaudio/best',
						'outtmpl': 'data/train/rawAudio/' + ourClasses[i] + '/%(id)s.%(ext)s',
						'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						'preferredcodec': 'mp3',
						}],
						'logger': MyLogger(),
						}
						

						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download([link])
						
						#Crop the audio
						song = AudioSegment.from_mp3(path_audio)
						extract = song[1000*startSec: 1000*endSec]
						extract.export( path_audio , format="mp3")	



	#Now going to download the raw audio test!!!!!
	with open("data/eval_segments.csv") as train_file:
		trainReader = csv.reader(train_file)

		rowCount = 0
		for row in trainReader:
			rowCount = rowCount + 1

			#Skip the first 3 rows, do not contain what we want!!
			if rowCount < 4 :
				continue

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
						path_audio = "data/test/rawAudio/" + ourClasses[i] + "/" + vidID + ".mp3"
						if os.path.isfile(path_audio):
							continue

						#Download Youtube Video!!
						print("Downloading " + ourClasses[i] + "( " + c + " ): " + link)

						#use pafy to check duration!!!
						video = pafy.new(link)
						if( video.length > maxVideoLength):
							break

						ydl_opts = {
						'format': 'bestaudio/best',
						'outtmpl': 'data/test/rawAudio/' + ourClasses[i] + '/%(id)s.%(ext)s',
						'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						'preferredcodec': 'mp3',
						}],
						'logger': MyLogger(),
						}
						

						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download([link])
						
						#Crop the audio
						song = AudioSegment.from_mp3(path_audio)
						extract = song[1000*startSec: 1000*endSec]
						extract.export( path_audio , format="mp3")				



if __name__== "__main__":
  main()