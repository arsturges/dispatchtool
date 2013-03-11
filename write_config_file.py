def writeConfigFile(config_file_name, program_input, dr_dispatch):
    assert(isinstance(program_input, dict))
    assert(isinstance(dr_dispatch, dict))

    import ConfigParser

    # class MyConfig(ConfigParser.RawConfigParser):
    #     def optionxform(self, optionstr):
    #         return str(optionstr)

    config = ConfigParser.RawConfigParser()
    config.optionxform = str

    # These are the actual headers.
    prog_input = "Program Input"

    refdr_fn = "ReferenceDR_FileName"
    lmp_fn = "LMP_FileName"
    energyload_fn = "EnergyLoadData_FileName"
    out_dir = "OutputDirectory"
    out_name = "OutputName"
    algorithm = "DispatchAlgorithm"

    dr_dispatch_sec = "DR Dispatch"

    config.add_section(prog_input)

    try:
        config.set(prog_input, refdr_fn, program_input[refdr_fn])
        config.set(prog_input, lmp_fn, program_input[lmp_fn])
        config.set(prog_input, energyload_fn, program_input[energyload_fn])
        config.set(prog_input, out_dir, program_input[out_dir])
        config.set(prog_input, out_name, program_input[out_name])
        config.set(prog_input, algorithm, program_input[algorithm])
    except KeyError, xcpt:
        raise xcpt

    config.add_section(dr_dispatch_sec)
    
    __writeDispatchToSection(config, dr_dispatch_sec, dr_dispatch)


    if "BA" in dr_dispatch:
        for ba in dr_dispatch["BA"].keys():
            sec_name = "/".join([dr_dispatch_sec, ba])
            config.add_section(sec_name)
            __writeDispatchToSection(config, sec_name, dr_dispatch["BA"][ba])

    with open(config_file_name, 'w') as config_file:
        config.write(config_file)
    return 


def __writeDispatchToSection(config, section, dictionary):
    cpp_event = "CPP_Event"
    dlc_event = "DLC_Event"
    lcr_event = "LCR_Event"
    num_event = "NumberEvents"
    num_cpp_event = "Number_CPP_Events"
    num_lcr_event = "Number_LCR_Events"
    num_dlc_event = "Number_DLC_Events"

    if cpp_event in dictionary.keys():
        config.set(section, cpp_event, dictionary[cpp_event])

    if dlc_event in dictionary.keys():
        config.set(section, dlc_event, dictionary[dlc_event])

    if lcr_event in dictionary.keys():
        config.set(section, lcr_event, dictionary[lcr_event])

    if num_event in dictionary.keys():
        config.set(section, num_event, dictionary[num_event])

    if num_cpp_event in dictionary.keys():
        config.set(section, num_cpp_event, dictionary[num_cpp_event])

    if num_lcr_event in dictionary.keys():
        config.set(section, num_lcr_event, dictionary[num_lcr_event])
                            
    if num_dlc_event in dictionary.keys():
        config.set(section, num_dlc_event, dictionary[num_dlc_event])

        return 
