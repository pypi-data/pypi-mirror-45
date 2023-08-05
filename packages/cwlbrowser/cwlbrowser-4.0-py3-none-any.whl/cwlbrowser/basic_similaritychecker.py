#Basic similarity checker
#Carries out bottom level comparison of two workflows depending on a certain attribute
# IE inputs outputs steps
IO_WEIGHTING = 15
STEP_WEIGHTING = 70
class BasicSimilarityChecker:
	def __init__(self) :
		self.overallMatch = 0
		self.attribute = []
		self.workflow1= []
		self.workflow2 = []
		self.fullListWorkflow1 = []
		self.fullListWorkflow2 = []
		self.differencesWorkflow1 = {}
		self.differencesWorkflow2 = {}
		self.matchingItems = []

	#sets up two lists to carry out comparisons between the corresponding workflows
	def compare(self, workflow1, workflow2, attribute) :
		self.attribute = attribute
		self.workflow1 = workflow1
		self.workflow2 = workflow2
		if (attribute == "inputs") :
			self.fullListWorkflow1 = workflow1.getInputsByName()
			self.fullListWorkflow2 = workflow2.getInputsByName()
		elif (attribute == "outputs") :
			self.fullListWorkflow1 = workflow1.getOutputsByName()
			self.fullListWorkflow2 = workflow2.getOutputsByName()
		else :
			self.fullListWorkflow1 = workflow1.getStepsByName()
			self.fullListWorkflow2 = workflow2.getStepsByName()
		self.similarityCheck(self.fullListWorkflow1, self.fullListWorkflow2)
		
	#Evaluates metrics and carries out the actual comparison
	def similarityCheck(self, workflow1Attributes, workflow2Attributes):
		if self.attribute == "steps" :
			weighting = STEP_WEIGHTING
		else :
			weighting = IO_WEIGHTING
		self.differencesWorkflow1 = set(workflow1Attributes).difference(workflow2Attributes)
		self.differencesWorkflow2 = set(workflow2Attributes).difference(workflow1Attributes)
		if len(workflow1Attributes) >= len(workflow2Attributes) :
			matchingItems = set(workflow2Attributes).intersection(workflow1Attributes)
			denominator = len(workflow1Attributes)
		else :
			matchingItems = set(workflow1Attributes).intersection(workflow2Attributes)
			denominator = len(workflow2Attributes)
		if denominator <= 0 :
			denominator = 1
		self.matchingItems = matchingItems
		self.overallMatch = len(matchingItems) / denominator * weighting

		
	def getOverallMatch(self) :
		return self.overallMatch

	def getDifferingItems(self) :
		differingItems = []
		for i in self.differencesWorkflow1 :
			differingItems.append(i)
		for i in self.differencesWorkflow2 :
			differingItems.append(i)
		return differingItems