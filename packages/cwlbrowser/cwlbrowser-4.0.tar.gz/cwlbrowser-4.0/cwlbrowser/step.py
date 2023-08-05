#Step object used to store information of steps in the workflow
import cwlbrowser.util as util
import cwlbrowser.input_output as io
UNKNOWN = "not known"


class Step:
	def __init__(self, stepData, name="step"):
		self.name = name
		self.inputs = []
		self.outputs = []
		self.run = []
		if(isinstance(stepData, dict)) :
			if "id" in stepData :
				self.name = stepData["id"]
			if "in" in stepData :
				self.inputs = self.createInputOutputArray(stepData["in"])
			if "out" in stepData :
				self.outputs  = self.createInputOutputArray(stepData["out"])
			if "run" in stepData :
				self.run = stepData["run"]

	def createInputOutputArray(self, elements) :
		return util.createInputOutputArray(elements, True)

		
	def getInputsByName(self) :
		temp = []
		for input_ in self.inputs :
			temp.append(input_.name)
		return temp

	def getInputsByType(self) :
		temp = []
		for input_ in self.inputs :
			temp.append(input_.type)
		return temp

	def getOutputsByName(self) :
		temp = []
		for output in self.outputs :
			temp.append(output.name)
		return temp


	def getOutputsByType(self) :
		temp = []
		for output in self.outputs :
			temp.append(output.type)
		return temp

	def __str__(self):
		return "Step: {0} | Run: {1}".format(self.name, self.run)