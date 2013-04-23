import uuid
import logging
import os.path, sys
import csv
from datetime import date, timedelta
path_to_this_file = os.path.abspath(__file__)
parent_directory_to_this_file = os.path.dirname(path_to_this_file)
shared_root = os.path.dirname(parent_directory_to_this_file)
path_to_DRD_module = os.path.join(shared_root, 'dr_dispatch', 'src')

log_file_path = os.path.join(parent_directory_to_this_file, 'dispatchtool.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
if path_to_DRD_module not in sys.path:
    sys.path.insert(0,path_to_DRD_module)

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

def parse_template_form_data(form_data):
    bas = []
    dr_programs = []
    for key in form_data.keys():
        if key[:2] == 'ba':
            if len(form_data[key]) > 0:
                bas.append(str(form_data[key]))
        if key[:10] == 'dr_program':
            if len(form_data[key]) > 0:
                dr_programs.append(str(form_data[key]))
    return bas, dr_programs

def create_templates(form_data):
    bas, dr_programs = parse_template_form_data(form_data)
    user_id = generateID()
    output_dir = os.path.join(parent_directory_to_this_file, 'csv_templates')
    dr_levels_filename = user_id + "dr_levels_template.csv"
    dr_levels_filepath = os.path.join(output_dir, dr_levels_filename)
    with open(dr_levels_filepath, 'wb') as f:
        writer = csv.writer(f)
        header = ['DSM','BA','Jan','Feb','Mar','Apr','May','Jun','Jul',
            'Aug','Sep','Oct','Nov','Dec']
        writer.writerow(header)
        for dr_program in dr_programs:
            for ba in bas:
                row = [dr_program, ba]
                writer.writerow(row)

    lmp_filename = user_id + "lmp_template.csv"
    lmp_filepath = os.path.join(output_dir, lmp_filename)
    with open(lmp_filepath, 'wb') as f:
        writer = csv.writer(f)
        header = ['Date', 'Hour of Day']
        for ba in bas:
            header.append(ba)
        writer.writerow(header)
        for day_of_year in range(365):
            date_object = date(2022,1,1) + timedelta(day_of_year)
            for hour_of_day in range(1,25):
                writer.writerow([
                    date_object.strftime('%m/%d/%Y'),
                    hour_of_day])


    energy_load_filename = user_id + "energy_load_template.csv"
    energy_load_filepath = os.path.join(output_dir, energy_load_filename)
    with open(energy_load_filepath, 'wb') as f:
        writer = csv.writer(f)
        header = ['Date', 'Hour of Day', 'Hour of Year']
        for ba in bas:
            header.append(ba)
        writer.writerow(header)
        hour_of_year = 1
        for day_of_year in range(365):
            date_object = date(2022,1,1) + timedelta(day_of_year)
            for hour_of_day in range(1,25):
                writer.writerow([
                    date_object.strftime('%m/%d/%Y'),
                    hour_of_day,
                    hour_of_year])
                hour_of_year += 1

    return dr_levels_filename, lmp_filename, energy_load_filename

if __name__ == "__main__":
    run_dr_dispatch(
        "/home/andrew/dr_dispatch/examples/Debug_DR_Levels.csv",
        "/home/andrew/dr_dispatch/examples/lmp_data.csv",
        "/home/andrew/dr_dispatch/examples/WECC_Hourly Energy Load.csv"
        )
