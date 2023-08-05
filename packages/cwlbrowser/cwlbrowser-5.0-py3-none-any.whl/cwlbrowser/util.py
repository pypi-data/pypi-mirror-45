#Utility module that has general purpose methods for displaying information 
def printAttr(attribute, attributeName, subjectName):
	print(subjectName + " " + attributeName + ":")
	print("-----------------")
	for item in attribute:
		if(isinstance(item, dict)):
			print(item["id"])
		else:
			print(item)
	print("\n")


def compare(name1, name2,attributeX, attributeY, attributeName):
	count1 = 0
	count2 = 0
	difference = 0
	for input_ in attributeX:
		count1 = count1 + 1
	for input_2 in attributeY:
		count2 = count2 + 1
	if(count1 >= count2):
		difference = count1 - count2
	else:
		difference = count2 - count1
	print("-------------------------------------")
	print("--------- " + attributeName + " comparison------------")
	print("-------------------------------------")
	print(name1 + "| no. of " + attributeName+ ": " + str(count1))
	print(name2 + "| no. of " + attributeName+ ": " + str(count2))
	print("Difference: " + str(difference))
	print("-------------------------------------")
	print("\n")


def createInputOutputArray(elements, step) :
	import cwlbrowser.workflow as wf
	import cwlbrowser.input_output as io
	temp =[]
	if(isinstance(elements, dict)) :
		for key, value in elements.items() :
			obj = io.InputOutput(value, step, name=key) 
			temp.append(obj)
	elif (isinstance(elements, list)) :
		for e in elements :
			obj = io.InputOutput(e, step) 
			temp.append(obj)
	else :
		temp = []
	return temp


def constructLink(parentLink, link) :
	parentlhs, parentrhs = parentLink.rsplit('/', 1)
	if('/' in link) :
		lhs, rhs = link.split('/', 1)
		if(lhs == '..') :
			root, path = parentlhs.rsplit('/', 1)
			finalLink = root + '/' + rhs
		else :
			finalLink = ""
	else :
		finalLink = parentlhs + '/' + link
	return finalLink







	

