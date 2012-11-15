import uuid
import os.path, sys
path_to_this_file = os.path.abspath(__file__)
parent_directory_to_this_file = os.path.dirname(path_to_this_file)
shared_root = os.path.dirname(parent_directory_to_this_file)
path_to_DRD_module = os.path.join(shared_root, 'dr_dispatch', 'src')

if path_to_DRD_module not in sys.path:
    sys.path.insert(0,path_to_DRD_module)
import DRD

def generateID():
     return "ID_" + str(uuid.uuid1().int)

def run_dr_dispatch(
    reference_dr_filename,
    lmp_filename,
    energy_load_data_filename,
    algorithm):

    user_id = generateID()
    output_dir = os.path.abspath('user_results')

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
    ba_input["CPP_Event"]= 4
    ba_input["DLC_Event"] = 5
    ba_input["LCR_Event"] = 6
    ba_input["NumberEvents"] = 10
    #ba_input["Number_CPP_Events"] = 5

    # This is how additional information will be added. Add this section:
    #ba_input["BA"] = {}
    #
    # For each BA to overwrite, add a dictionary with it.
    #ba_input["BA"]["AESO"] = {}
    #ba_input["BA"]["AESO"]["Number_CPP_Events"] = "10"

    DRD.writeConfigFile("configuration_file.ini", prog_input, ba_input)
    megawatts_dispatch_fn, prices_dispatch_fn = DRD.dispatchDR("configuration_file.ini") 

    print megawatts_dispatch_fn
    print prices_dispatch_fn
    return megawatts_dispatch_fn, prices_dispatch_fn

def allowed_files(allowed_extensions, *filenames):
    ''' Takes an arbitrary number of filenames and returns true if all of their
    file extensions are in the set of allowed_extensions, e.g. .csv, .txt, but 
    not .xls or .png. If any one of the files has a forbidden file extension,
    the function returns False. Otherwise it returns True.'''

    binaries = []
    for filename in filenames:
        # next line returns true false
        true_false = '.' in filename and filename.rsplit('.',1)[1] in allowed_extensions 
        binaries.append(true_false) # will have e.g. [True, True, False, True]
    sum = 0
    for binary in binaries:
        if binary == False:
            sum += 1
        else:
            sum += 0
    if sum > 0:
        return False
    else:
        return True

if __name__ == "__main__":
    run_dr_dispatch(
        "/home/andrew/dr_dispatch/data/WECC_Common Case Reference DR.csv",
        "/home/andrew/dr_dispatch/data/WECC_Common Case LMPs_20120130.csv",
        "/home/andrew/dr_dispatch/data/WECC_Hourly Energy Load.csv",
        "Inflexible"
        )
