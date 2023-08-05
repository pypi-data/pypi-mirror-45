#Main central python module used to carry out browsing of workflows on Jupyter notebook
import requests
import base64
import yaml
import os
import cwltool
import subprocess
import cwlbrowser.workflow as wf
import cwlbrowser.util as util
import cwlbrowser.similaritychecker as s
from IPython.display import SVG, display, HTML
import time
import itertools
import os


out_workflow = {}
steps = []
STEPS_WEIGHTING = 70
IO_WEIGHTING = 15
workflowlink = []


#retrieves .cwl file from provided github link
def retrieveFileThruLink(link, path):
	req = requests.get(link)
	if req.status_code != 200:
	    print(req.status_code)
	    if req.status_code == 404:
	    	print ("cwl file not found. Maybe due to incorrect url")
	    	print("\n")
	else:
		req = req.json()  	    
		content = base64.b64decode(req['content'])
		content = content.decode("utf-8")
		try:
			out_workflow = yaml.safe_load(content)
			#print (out_workflow)
			return wf.Workflow(path, out_workflow, workflowlink)
		except (yaml.YAMLError) as yamlError:
			print ("Error in loading the cwl file")
			print (yamlError)

#main load method.
#path to local file or github link to file can be passed as an argument
def load(workflow, link=True):
	if(link == False):
		global out_workflow
		if os.path.exists(workflow):
			file = open(workflow, 'rb')
			try:
				out_workflow = yaml.safe_load(file)
				return wf.Workflow(workflow, out_workflow)
			except (yaml.YAMLError):
				print ("Error in loading the cwl file")
		else:
			print("File not located")
			return -1;
	else:
		return loadWithLink(workflow)

#pre processes link so that it is in correct format to pass to 
#retrieveFileThruLink method
def loadWithLink(link) :
	global workflowlink
	workflowlink = link
	lhs, rhs = link.split("/blob/", 1)
	branch, path = rhs.split("/", 1)
	ownerrepo = lhs.replace('https://github.com', "")
	finallink = "https://api.github.com/repos" + ownerrepo + "/contents/" + path
	return retrieveFileThruLink(finallink, path)

#print the specified attribute you want 
#pass the attribute as a string to the method
#E.G. printWorfklow("inputs")
def printWorkflowAttr(attribute) :
	if attribute in out_workflow.keys() :
		print(attribute + ":")
		for item in out_workflow[attribute] :
			print (item)
		print ("\n")
	else :
		print("No such attribute as: " + attribute + " found in workflow")


#displays visual representation of workflow using CWL Viewer API
def displayGraph(workflow, type="link"):
	if (type  == "link") :
		BASE_URL = 'https://view.commonwl.org'

		HEADERS = {
		    'user-agent': 'my-app/0.0.1',
			'accept': 'application/json'
		}

		addResponse = requests.post(BASE_URL + '/workflows', 
								data={'url': workflow.link},		
								headers=HEADERS)
		if (addResponse.status_code == 200) :
			postExistingWorkflowGraph(workflow.link)
		elif (addResponse.status_code == requests.codes.accepted):
			qLocation = addResponse.headers['location']

			# Get the queue item until success
			qResponse = requests.get(BASE_URL + qLocation,
									headers=HEADERS,
									allow_redirects=False)
			maxAttempts = 5
			while qResponse.status_code == requests.codes.ok and qResponse.json()['cwltoolStatus'] == 'RUNNING' and maxAttempts > 0:
				time.sleep(5)
				qResponse = requests.get(BASE_URL + qLocation,
										headers=HEADERS,
										allow_redirects=False)
				maxAttempts -= 1
			if 'location' in qResponse.headers:
			# Success, get the workflow
				workflowResponse = requests.get(BASE_URL + qResponse.headers['location'], headers=HEADERS)
				if (workflowResponse.status_code == requests.codes.ok):
					workflowJson = workflowResponse.json()
					# Do what you want with the workflow JSON
					# Include details in documentation files etc
					display(SVG(BASE_URL + workflowJson['visualisationSvg']))
				else:
					print('Could not get returned workflow')
			elif (qResponse.json()['cwltoolStatus'] == 'ERROR'):
				# Cwltool failed to run here
				print(qResponse.json()['message'])
			elif (maxAttempts == 0):
				print('Timeout: Cwltool did not finish')
			else :
				print('Something is not right')

		else:
			print (addResponse.status_code)
			print('Error adding workflow')
	elif (type== "file"):
		name, suffix = workflow.split(".cwl") 
		p = subprocess.run(["cwltool", "--print-dot", workflow], capture_output=True)
		if(p.returncode != 0) :
			print ("Something went wrong")
			print(bytes.decode(p.stderr))
		else :
			graphFile = name + ".svg"
			display(SVG(graphFile))
	else :
		print("Invalid type")

	"""
	"""

#displays graph of workflow if it has already been uploaded to website
def postExistingWorkflowGraph(link) :
	BASE_URL = 'https://view.commonwl.org'

	HEADERS = {
		'accept': 'application/json'
	}
	shortenedLink = link.replace("https://", "")
	finishedlink = BASE_URL + "/workflows/" + shortenedLink
	req = requests.get(finishedlink, headers=HEADERS)
	if req.status_code != 200:
		print(req.status_code)
	else:
		req = req.json()     
		display(SVG(BASE_URL + req['visualisationSvg']))

#displays tabular representation of workflow
#specific attributes can be displayed on their own
def displayTables(workflow, attr='All') :
	caption = ""
	if attr == 'All':
		caption = "\n {} INPUTS:".format(workflow.name)
		tabulateWorkflow(workflow.inputs, caption)
		caption = "\n {} OUTPUTS:".format(workflow.name)
		tabulateWorkflow(workflow.outputs, caption)
		caption = "\n {} STEPS:".format(workflow.name)
		tabulateWorkflow(workflow.steps, caption, step=True)

	elif attr == 'inputs' or attr == 'input' :
		caption = "\n {} INPUTS:".format(workflow.name)
		tabulateWorkflow(workflow.inputs, caption)

	elif attr == 'outputs' or attr == 'output':
		caption = "\n {} OUTPUTS:".format(workflow.name)
		tabulateWorkflow(workflow.outputs, caption)

	elif attr == 'steps' or attr =='step' :
		caption = "\n {} STEPS:".format(workflow.name)
		tabulateWorkflow(workflow.steps, caption, step=True)

	else:
		print("Invalid attribute specified: Please use 'outputs', 'inputs', 'steps' or 'All")


#Displays results of similarity checker
def displayStats(similarityChecker) :
	tabulateSimChecker(similarityChecker.inputSimilarityChecker)
	tabulateSimChecker(similarityChecker.outputSimilarityChecker)
	tabulateSimChecker(similarityChecker.stepSimilarityChecker)
	print("Overall match: {}".format(similarityChecker.overallMatch))

def tabulateSimChecker(similarityChecker) :
	caption = '<caption style="font-weight:bold; font-size: 20px">{} and {} {}</caption>'.format(similarityChecker.workflow1.name, 
														similarityChecker.workflow2.name, similarityChecker.attribute)
	data = ""
	tableBody = setColours(similarityChecker.fullListWorkflow1, similarityChecker.fullListWorkflow2,
							similarityChecker.differencesWorkflow1, 
							similarityChecker.differencesWorkflow2, similarityChecker.attribute)
	data = data + tableBody
	display(HTML('<table style="width:100%">{}<tr><th>{}</th><th>{}</th></tr>{}</table>'.format(caption, similarityChecker.workflow1.name, similarityChecker.workflow2.name, data)))


#sets colours of cells in table to distinguish differing and similar elements of the two workflows being compared
def setColours(worklow1Attributes, workflow2Attributes, workflow1Diff, workflow2Diff, attr) :
	tableBody = ""
	styleI = ""
	styleJ = ""
	uncolored = 'style="border: 1px solid black"' 
	green = 'style="border: 1px solid black; background-color:limegreen"'
	diff = 'style="border: 1px solid black; background-color:{}"'.format("yellow" if not attr == 'steps' else "red")
	for i, j in itertools.zip_longest(worklow1Attributes, workflow2Attributes) :
		styleI = green if not (i in workflow1Diff) else diff
		styleJ = green if not (j in workflow2Diff) else diff
		(i, styleI) = (i, styleI)  if not(i == None) else ("", uncolored)
		(j, styleJ) = (j, styleJ) if not(j == None) else ("", uncolored)
		tableBody = tableBody + ('<tr><td {}>{}</td><td {}>{}</td></tr>'.format(styleI, i, styleJ, j))
	return tableBody


#Helper method used to display tabular view of workflow via HTML
def tabulateWorkflow(list_, inputCaption, step=False) :
	caption = '<caption style="font-weight:bold; font-size: 20px">{}</caption>'.format(inputCaption)
	page = "<html>" 
	style = 'style= "border: 1px solid black"'
	data = ""
	if step == False :
		attr = "Type"
		for i in list_ :
			data = data + ("<tr {}><td {}>{}</td><td {}>{}</td></tr>".format(style, style, i.name, style, i.type))
	else :
		attr = "Run"
		for i in list_ :
			data = data + ("<tr {}><td {}>{}</td><td {}>{}</td></tr>".format(style, style, i.name, style,i.run))
	page = page + '<body><table style="width:100%;border: 1px solid black">{}<tr><th {}>Name</th><th {}>{}</th></tr>{}</table></body>'.format(caption, style, style, attr, data)
	page = page + "</html>"
	display(HTML(page))











	
