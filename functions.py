import os
import json
import csv
import numpy as np


def createFolder(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return


def getClasses(pathOurClassesCSV, pathYoutubeOntologyJSON, pathYoutubeClassLabels ):
	ourClasses     = [];
	youtubeClasses = [];

	#Open class csv file
	with open(pathOurClassesCSV) as class_csvFile:
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

					ourClasses.append(c)

					firstC = False
					continue

				#These c classes are the ones we will find on youtube/CNN now!!!
				if c:
					tempYoutubeClass.append(c)

			youtubeClasses.append(tempYoutubeClass)



	#Now time to get id from the youtubeClasses
	youtubeClassesID =[]

	with open(pathYoutubeOntologyJSON) as ontology_data:
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


	#Get the labels for tfrecord
	labelsTF = []
	for classList in youtubeClasses:
		tempLabels_tf = []

		with open(pathYoutubeClassLabels) as labels_tf_csvFile:
			labels_tf_csv = csv.reader(labels_tf_csvFile)


			for row in labels_tf_csv:
				if row[2] in classList:
					tempLabels_tf.append(row[0])

		labelsTF.append(tempLabels_tf)



	return ourClasses, youtubeClasses, youtubeClassesID, labelsTF


