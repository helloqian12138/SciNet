import os, sys, stat
import sys
import optparse
import logging as logger
import configparser
import pickle
import platform
from time import time
from subprocess import call
from os import system, rename

# Framework imports
from serverless.Serverless import *
from serverless.datacenter.AzureDatacenter import *
from serverless.workload.AIBenchWorkload import *

# Provisioner imports
from provisioner.Provisioner import Provisioner
from provisioner.Random_Provisioner import RandomProvisioner
from provisioner.CoSim_Provisioner import CoSimProvisioner
from provisioner.SciNet_Provisioner import SciNetProvisioner
from provisioner.ACOARIMA_Provisioner import ACOARIMAProvisioner
from provisioner.ACOLSTM_Provisioner import ACOLSTMProvisioner
from provisioner.DecisionNN_Provisioner import DecisionNNProvisioner
from provisioner.SemiDirect_Provisioner import SemiDirectProvisioner
from provisioner.GRAF_Provisioner import GRAFProvisioner
from provisioner.UAHS_Provisioner import UAHSProvisioner
from provisioner.CAHS_Provisioner import CAHSProvisioner
from provisioner.Narya_Provisioner import NaryaProvisioner
from provisioner.HASCO_Provisioner import HASCOProvisioner
from provisioner.RecSim_Provisioner import RecSimProvisioner
from provisioner.CES_Provisioner import CESProvisioner

# Decider imports
from decider.Random import RandomDecider
from decider.Layer_Only import LayerOnlyDecider
from decider.Semantic_Only import SemanticOnlyDecider
from decider.Compression_Only import CompressionOnlyDecider
from decider.CoSim_Decider import CoSimDecider
from decider.SciNet_Decider import SciNetDecider
from decider.ACOARIMA_Decider import ACOARIMADecider
from decider.ACOLSTM_Decider import ACOLSTMDecider
from decider.DecisionNN_Decider import DecisionNNDecider
from decider.SemiDirect_Decider import SemiDirectDecider
from decider.GRAF_Decider import GRAFDecider
from decider.Gillis_Decider import GillisDecider
from decider.SplitPlace_Decider import SplitPlaceDecider
from decider.HASCO_Decider import HASCODecider
from decider.RecSim_Decider import RecSimDecider
from decider.CES_Decider import CESDecider

# Scheduler imports
from scheduler.Random import RandomScheduler
from scheduler.CoSim_Scheduler import CoSimScheduler
from scheduler.SciNet_Scheduler import SciNetScheduler
from scheduler.ACOARIMA_Scheduler import ACOARIMAScheduler
from scheduler.ACOLSTM_Scheduler import ACOLSTMScheduler
from scheduler.DecisionNN_Scheduler import DecisionNNScheduler
from scheduler.SemiDirect_Scheduler import SemiDirectScheduler
from scheduler.GRAF_Scheduler import GRAFScheduler
from scheduler.GOBI_Scheduler import GOBIScheduler
from scheduler.GOSH_Scheduler import GOSHScheduler
from scheduler.HASCO_Scheduler import HASCOScheduler
from scheduler.RecSim_Scheduler import RecSimScheduler
from scheduler.CES_Scheduler import CESScheduler

# Auxiliary imports
from stats.Stats import *
from utils.Utils import *
from pdb import set_trace as bp

usage = "usage: python main.py -e <environment> -t <type> -m <model>"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-e", "--environment", action="store", dest="env", default="Azure", 
					choices=['Azure', 'VLAN'],
					help="Environment is Azure or VLAN.")
parser.add_option("-t", "--type", action="store", dest="type", default="2", 
					choices=['0', '1', '2', '3'],
					help="Type is 0 (Create and destroy), 1 (Create), 2 (No op), 3 (Destroy)")
parser.add_option("-m", "--model", action="store", dest="model", default="Random", 
					choices=['Random', 'CoSim', 'ACOARIMA', 'ACOLSTM', 'DecisionNN', 'SemiDirect',\
						'GRAF', 'UAHS', 'CAHS', 'Narya', 'HASCO', 'RecSim', 'CES', 'SciNet'])
opts, args = parser.parse_args()

# Global constants
NUM_SIM_STEPS = 200
HOSTS = 10
INTERVAL_TIME = 5 # seconds
NEW_TASKS = 0

def initalizeEnvironment(environment, type, prov, dec, sched):
	# Initialize simple fog datacenter
	''' Can be AzureDatacenter '''
	datacenter = eval(environment+'Datacenter(type)')
	hostlist = datacenter.generateHosts()
	
	# Initialize workload
	''' Can be AIBench '''
	workload = AIBenchWorkload(NEW_TASKS, 1.5)

	# Initialize provisioner
	provisioner = eval(prov+'Provisioner()')

	# Initialize decider
	decider = eval(dec+'Decider()')

	# Initialize scheduler
	scheduler = eval(sched+'Scheduler()')

	# Initialize Environment
	env = Serverless(scheduler, decider, provisioner, INTERVAL_TIME, hostlist, environment)

	# Execute first step
	workloadlist = workload.generateNewContainers(env.interval) # New containers info
	provisioner.provision() # Provision hosts
	newtasklist = decider.decision(workloadlist) # Decide splitting choice
	decision, schedulingTime = scheduler.placement(newtasklist) # Decide placement using task objects
	numdep = env.allocateInit(newtasklist, decision) # Schedule functions
	print("New Tasks Size:", len(newtasklist))
	print("Waiting List Size:", len(env.waitinglist))
	print("Tasks in hosts:", env.getTasksInHosts())
	print("Deployed:", numdep, "of", len(env.waitinglist + newtasklist))
	printProvisioned(env.hostlist)
	printDecisions(newtasklist)
	print("Schedule:", decision)

	# Initialize stats
	stats = Stats(env, workload, datacenter, scheduler)
	stats.saveStats(numdep, [], newtasklist, decision, schedulingTime)
	return datacenter, workload, scheduler, decider, provisioner, env, stats

def stepSimulation(workload, scheduler, decider, provisioner, env, stats):
	workloadlist = workload.generateNewContainers(env.interval) # New containers info
	provisioner.provision() # Provision hosts
	newtasklist = decider.decision(workloadlist) # Decide splitting choice
	decision, schedulingTime = scheduler.placement(env.waitinglist + newtasklist) # Decide placement using task objects
	destroyed = env.destroyCompletedTasks()
	numdep = env.simulationStep(newtasklist, decision) # Schedule containers
	print("New Tasks Size:", len(newtasklist))
	print("Waiting List Size:", len(env.waitinglist))
	print("Tasks in hosts:", env.getTasksInHosts())
	print("Deployed:", numdep, "of", len(env.waitinglist + newtasklist))
	print("Destroyed:", len(destroyed), "of", len(env.activetasklist))
	printProvisioned(env.hostlist)
	printDecisions(newtasklist)
	print("Schedule:", decision)

	stats.saveStats(numdep, destroyed, newtasklist, decision, schedulingTime)

def saveStats(stats, dirname, end=True):
	stats.generateDatasets(dirname)
	if not end: return
	stats.generateGraphs(dirname); stats.generateCompleteDatasets(dirname)
	stats.env, stats.workload, stats.datacenter, stats.scheduler = None, None, None, None
	with open(dirname + '/stats.pk', 'wb') as handle:  pickle.dump(stats, handle)

if __name__ == '__main__':
	# Initialize Environment
	datacenter, workload, scheduler, decider, provisioner, env, stats = initalizeEnvironment(opts.env, int(opts.type), *decompose(opts.model))

	# Create log directory
	dirname = "logs/" + opts.model
	if not os.path.exists("logs"): os.mkdir("logs")
	if os.path.exists(dirname): shutil.rmtree(dirname, ignore_errors=True)
	os.mkdir(dirname)

	# Execute steps
	for step in range(NUM_SIM_STEPS):
		print(color.GREEN+"Execution Interval:", step, color.ENDC)
		stepSimulation(workload, scheduler, decider, provisioner, env, stats)
		if step % 10 == 0: saveStats(stats, dirname, end = False)

	# Cleanup and save results
	datacenter.cleanup()
	saveStats(stats, dirname)

