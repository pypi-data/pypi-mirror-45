#Similarity checker object
#Consists of three similarity objects that compare a certain
#attribute of two workflows (inputs, outputs, steps)

STEPS_WEIGHTING = 70
IO_WEIGHTING = 15

class SimilarityChecker :
	def __init__(self) :
		import cwlbrowser.basic_similaritychecker as b
		self.overallMatch = 0
		self.workflow1 = []
		self.workflow2 = []
		self.inputSimilarityChecker = b.BasicSimilarityChecker()
		self.stepSimilarityChecker = b.BasicSimilarityChecker()
		self.outputSimilarityChecker = b.BasicSimilarityChecker()

	def similarityCheck(self, workflow1, workflow2) :
		self.workflow1 = workflow1
		self.workflow2 = workflow2
		self.inputSimilarityChecker.compare(workflow1, workflow2, "inputs")
		self.stepSimilarityChecker.compare(workflow1, workflow2, "steps")
		self.outputSimilarityChecker.compare(workflow1, workflow2, "outputs")
		self.overallMatch = round((self.inputSimilarityChecker.overallMatch 
							+ self.outputSimilarityChecker.overallMatch 
							+ self.stepSimilarityChecker.overallMatch), 3)

	def getOverallMatch(self) :
		return self.overallMatch
