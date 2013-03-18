"""
This module takes care of generating config files needed to run the
dr_dispatch tool (DRD). Config files are the only way to run DRD.
Config file section headings and the associated key names are specified
by DRD, and should not be changed. The four dictionaries below illustrate
these names. The dispatchtool web application should take care to 
generate these input dictionaries exactly as they appear here.
"""

import ConfigParser
import os

path_to_this_file = os.path.abspath(__file__)
present_directory = os.path.dirname(path_to_this_file)

input_ = {
    "Strict": 3, 
    "DR_Availability_File_Name": '/home/andy/dr_dispatch/examples/Debug_DR_Levels.csv',
    "Prices_File_Name": "/home/andy/dr_dispatch/examples/lmp_data.csv",
    "Demand_File_Name": "/home/andy/dr_dispatch/examples/WECC_Hourly Energy Load.csv"}

output = {
    "Directory": os.path.join(present_directory, 'user_results'), # Addy, can it just 'return' two files instead of writing them somewhere?
    "Name": "FLEXIBLE_NONINTERRUPT", # Filename prefix.
    "Make_Graphs": True}

dispatch_configuration = {
    #"Dispatch_Name": "Original", 
    # Addy is this needed? Seems like it's either 'dispatch_name' OR the two triggers.
    # If so, what are the names? Or should we just remove this option?
    "Dispatch_Type": "PeakBlock",
    "Dispatch_Type": "Flexible",
    "Dispatch_Type": "PeriodBlock",
    "Dispatch_Trigger": "ExpectedPriceSavings",
    "Dispatch_Trigger": "ExpectedDemandSavings",
    "Dispatch_Trigger": "Demand",
    "Dispatch_Trigger": "Price"
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

def writeConfigFile(
                      input_,
                      output,
                      dispatch_configuration,
                      dr_programs):

    """ Write a config file to be read by DRD module. Takes a file name
    and four dictionaries. Dictionaries must have keys named as in the
    examples above, because that's what DRD expects. """

    config = ConfigParser.RawConfigParser()
    config.optionxform = str # Addy what does this do?

    # Section Headers (just the four main sections)
    config.add_section("Input")
    config.add_section("Output")
    config.add_section("Dispatch Configuration")
    config.add_section("DR Programs") # For general settings.
    # BA-specific settings (overrides) go labeled sections below.

    # Section key:value pairs
    defined_keys = [
        'P_Event_Length',
        'L_Event_Length',
        'I_Event_Length',
        'R_Event_Length',
        'P_Number_Events',
        'L_Number_Events',
        'I_Number_Events',
        'R_Number_Events']
    for key, value in input_.iteritems():
        config.set("Input", key, value)
    for key, value in output.iteritems():
        config.set("Output", key, value)
    for key, value in dispatch_configuration.iteritems():
        config.set("Dispatch Configuration", key, value)
    for key, value in dr_programs.iteritems():
        if key in defined_keys:
            config.set("DR Programs", key, value)

    # If present in the user-submitted dictionary dr_programs,
    # add sections for individual BA program overrides.
    for key, value in dr_programs.iteritems():
        if key not in defined_keys:
            config.add_section("DR Programs/"+key)
            for ba_key, ba_value in dr_programs[key].iteritems():
                config.set("DR Programs/"+key, ba_key, ba_value)

    config_file_path = os.path.join(present_directory, 'configuration_file.conf')
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

if __name__ == "__main__":
    writeConfigFile(input_, output, dispatch_configuration, dr_programs)
