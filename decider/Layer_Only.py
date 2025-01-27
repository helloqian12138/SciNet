from .Decider import *

class LayerOnlyDecider(Decider):
	def __init__(self):
		super().__init__()

	def decision(self, workflowlist):
		results = []
		for CreationID, interval, SLA, application in workflowlist:
			choice = self.choices[0]
			tasklist = self.createTasks(CreationID, interval, SLA, application, choice)
			results += tasklist
		return results