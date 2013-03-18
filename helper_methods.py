import uuid
import logging
import os.path, sys
path_to_this_file = os.path.abspath(__file__)
parent_directory_to_this_file = os.path.dirname(path_to_this_file)
shared_root = os.path.dirname(parent_directory_to_this_file)
path_to_DRD_module = os.path.join(shared_root, 'dr_dispatch', 'src')

log_file_path = os.path.join(parent_directory_to_this_file, 'dispatchtool.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
if path_to_DRD_module not in sys.path:
    sys.path.insert(0,path_to_DRD_module)
logging.debug("sys.path: " + str(sys.path))
import DRD
import write_config_file

def generateID():
     return str(uuid.uuid1().int)[:5]

def run_dr_dispatch(
    reference_dr_filename,
    lmp_filename,
    energy_load_data_filename,
    dispatch_type,
    dispatch_trigger):

    print "Entering run_dr_dispatch" 
    user_id = generateID()
    output_dir = os.path.join(parent_directory_to_this_file, 'user_results')

    input_ = {
        "Strict": 3, 
        "DR_Availability_File_Name": reference_dr_filename,
        "Prices_File_Name": lmp_filename,
        "Demand_File_Name": energy_load_data_filename}

    output = {
        "Directory": output_dir, 
        # Addy, can it just 'return' two files instead of writing them somewhere?
        "Name": dispatch_type + "_" + dispatch_trigger + "_" + user_id + "_", 
        # filenames prefix, e.g. "PeakBlock_ExpectedDemandSavings_49582_"
        "Make_Graphs": False}

    dispatch_configuration = {
        #"Dispatch_Name": "Original", 
        # Addy should this be deleted, or is it still used?
        "Dispatch_Type": dispatch_type, # "PeakBlock"; 'Flexible'; 'PeriodBlock'
        "Dispatch_Trigger": dispatch_trigger 
        # "ExpectedPriceSavings"; ExpectedDemandSavings; Demand; Price
        }

    dr_programs = {
        "P_Event_Length": 4,
        "L_Event_Length": 4,
        "I_Event_Length": 4,
        "R_Event_Length": 4,
        "P_Number_Events": 2,
        "L_Number_Events": 2,
        "I_Number_Events": 2,
        "R_Number_Events": 2,
        "PSCO": {"I_Event_Length": 8, "I_Number_Events": 2}
        }

    configuration_file_path = os.path.join(
        parent_directory_to_this_file, 
        'configuration_file.conf')
    write_config_file.writeConfigFile(input_, output, dispatch_configuration, dr_programs)
    conf = DRD.Configuration.getConfiguration(configuration_file_path)
    DRD.bin.dispatchDR(conf) 
    return output['Name']+'dr_dispatches.csv', output['Name']+'dr_prices.csv'


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
        "/home/andrew/dr_dispatch/examples/Debug_DR_Levels.csv",
        "/home/andrew/dr_dispatch/examples/lmp_data.csv",
        "/home/andrew/dr_dispatch/examples/WECC_Hourly Energy Load.csv"
        )
