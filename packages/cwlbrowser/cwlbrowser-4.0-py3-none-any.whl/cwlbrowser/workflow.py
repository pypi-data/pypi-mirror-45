UNKNOWN = "not known"
#Workflow class used to store information of the workflow being processed on
class Workflow:
	def __init__(self, name, workflow, link="local"):
		self.name = name;
		self.inputs = [] if not "inputs"  in workflow else self.createInputOutputArray(workflow["inputs"])
		self.outputs = [] if not "outputs" in workflow else self.createInputOutputArray(workflow["outputs"])
		self.steps = [] if not "steps" in workflow else self.createStepArray(workflow["steps"])
		self.link = link
		self.parent = []

	def createStepArray(self, steps) :
		import cwlbrowser.step as s
		temp = []
		#print (steps)
		if (isinstance(steps, dict)) :
			for key, value in steps.items() :
				stepObj = s.Step(value, name=key)
				temp.append(stepObj)
		elif(isinstance(steps, list)) :
			for step in steps :
				stepObj = s.Step(step)
				temp.append(stepObj)
		else :
			temp = []
		return temp

	def loadStep(self, run) :
		import cwlbrowser.browser as c
		import cwlbrowser.util as util
		if run not in self.getStepsByRun():
			raise Exception('{} is not a step in {}'.format(run, self.name))
		else :
			stepLink = util.constructLink(self.link, run)
			step = c.loadWithLink(stepLink)
			step.setParent(self)
			return step



	def createInputOutputArray(self, elements) :
		import cwlbrowser.util as util
		return util.createInputOutputArray(elements, False)

	def setParent(self, parent) :
		self.parent = parent


	def getInputsByName(self) :
		return self.getElementsByAttribute(self.inputs, "name")

	def getInputsByType(self) :
		return self.getElementsByAttribute(self.inputs, "type")

	def getOutputsByName(self) :
		return self.getElementsByAttribute(self.outputs, "name")

	def getOutputsByType(self) :
		return self.getElementsByAttribute(self.outputs, "type")

	def getStepsByName(self) :
		return self.getElementsByAttribute(self.steps, "name")

	def getStepsByRun(self) :
		return self.getElementsByAttribute(self.steps, "run")

	def getElementsByAttribute(self, list_, attribute) :
		temp = []
		if list_ != [] :
			for item in list_ :
				if attribute == "name":
					temp.append(item.name)
				elif attribute == "type" :
					temp.append(item.type)
				else  :
					temp.append(item.run)
		else :
			temp = []
		return temp



