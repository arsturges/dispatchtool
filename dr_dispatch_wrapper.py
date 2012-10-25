import uuid
import os.path, sys
path = os.path.abspath(os.path.pardir) #path of parent directory
path += '/dr_dispatch/src' #path from parent directory to DRD
if path not in sys.path:
    sys.path.insert(0,path)
import DRD

def generateID():
     #return "ID_" + str(uuid.uuid1().int)

def run_dr_dispatch(
    reference_dr_filename,
    lmp_filename,
    energy_load_data_filename,
    algorithm):
    
    user_id = generateID()
    output_dir = "/home/andrew/dispatchtool/tmp"

    # These three inputs are provided by the user, although the LMP
    # filename (the prices) may or may not be provided by the user.
    prog_input = {}
    prog_input["ReferenceDR_FileName"] = reference_dr_filename 
    prog_input["LMP_FileName"] = lmp_filename 
    prog_input["EnergyLoadData_FileName"] = energy_load_data_filename
    prog_input["OutputDirectory"] = output_dir 
    prog_input["OutputName"] = user_id
    prog_input["DispatchAlgorithm"] = algorithm

    ba_input = {}
    ba_input["CPP_Event"]= 2
    ba_input["DLC_Event"] = 0
    ba_input["LCR_Event"] = 0
    ba_input["NumberEvents"] = 10
    ba_input["Number_CPP_Events"] = 5

    # This is how additional information will be added. Add this section:
    #ba_input["BA"] = {}
    #
    # For each BA to overwrite, add a dictionary with it.
    #ba_input["BA"]["AESO"] = {}
    #ba_input["BA"]["AESO"]["Number_CPP_Events"] = "10"

    DRD.writeConfigFile("configuration_file.ini", prog_input, ba_input)
    megawatts_dispatch_fn, price_dispatch_fn = DRD.dispatchDR("configuration_file.ini") 

    print megawatts_dispatch_fn
    print price_dispatch_fn

if __name__ == "__main__":
    run_dr_dispatch(
        "user_uploads/WECC_Common Case Reference DR.csv",
        "user_uploads/WECC_Common Case LMPs_20120130.csv",
        "user_uploads/WECC_Hourly Energy Load.csv",
        "Inflexible"
        )
