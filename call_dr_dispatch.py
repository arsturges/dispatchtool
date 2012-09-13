import uuid
import os.path, sys
path = os.path.abspath(os.path.pardir) #path of parent directory
path += '/dr_dispatch/src' #path from parent directory to DRD
if path not in sys.path:
	sys.path.insert(0,path)
import DRD

def generateID():
   return "ID_" + str(uuid.uuid1().int)

user_id = generateID()

# Change this to your writable directory
output_dir = "/home/andrew/dispatchtool/tmp"


#
# Making the prog input directory 
#
prog_input = {}

# These three inputs are provided by the user, although the LMP
# filename (the prices) may or may not be provided by the user.
prog_input["ReferenceDR_FileName"] = "../dr_dispatch/data/WECC_Common Case Reference DR.csv"
prog_input["LMP_FileName"] = "../dr_dispatch/data/WECC_Common Case LMPs_20120130.csv"
prog_input["EnergyLoadData_FileName"] = "../dr_dispatch/data/WECC_Hourly Energy Load.csv"
prog_input["OutputDirectory"] = output_dir 
prog_input["OutputName"] = user_id
prog_input["DispatchAlgorithm"] = "Inflexible"

ba_input = {}

ba_input["CPP_Event"]= 2
ba_input["DLC_Event"] = 0
ba_input["LCR_Event"] = 0
ba_input["NumberEvents"] = 10
ba_input["Number_CPP_Events"] = 5


# This is how (ultimately) additional information will be added.

# Add this section
#ba_input["BA"] = {}
#
# For each BA to overwrite, add a dictionary with it.
#ba_input["BA"]["AESO"] = {}
#ba_input["BA"]["AESO"]["Number_CPP_Events"] = "10"


DRD.writeConfigFile("example.ini", prog_input, ba_input)
megawatts_dispatch_fn, price_dispatch_fn = DRD.dispatchDR("example.ini") 

print megawatts_dispatch_fn
print price_dispatch_fn
