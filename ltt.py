import re
import sys
import numpy as np
import argparse
import PyRanOrg
import glob
import os

# ----------------------------------------------------
# multiple replacement function


def multiple_replace(dict, text, index=0):
    # Create a regular expression from the dictionary keys
    # find string inside double curly braces. ...{{parameter}}...
    pattern = re.compile("|".join(k for k in ['{{('+re.escape(item)+')}}'
                         for item in dict.keys()]))

    # For each match, look-up corresponding value in dictionary
    if isinstance(dict.values()[0], list) or \
       isinstance(dict.values()[0], np.ndarray):
        return pattern.sub(lambda m: str(dict[m.group(0)[2:-2]][index]), text)
    else:
        return pattern.sub(lambda m: str(dict[m.group(0)[2:-2]]), text)
# ---------------------------------------------------

def ltt(template_file, parameter_file):
    # -----------------------------------------------------
    # first compile the pattern in parameter
    # parameter must be specified in such manner:
    #     FILENAME=lammps_input_file_test_{{FILENAME_parameter}}
    #     FILENAME_parameter=['1','2','3','4','5']
    #     parameter_1=[1,2,3,4,5]
    #     parameter_2=np.arange(1,6)
    #     parameter_3=[5,5,5,5,5]
    #     parameter_4=np.linspace(0,5,5)
    # Note: all the parameter list must has the same length

    inputfilename = {}
    parameter_dic = {}
    pattern_dic = {}
    with open(parameter_file, 'r') as f:
        for i, line in enumerate(f):
            # ignore the empty line
            if line.strip():
                # ignore line with '#' starting. comment line
                if line[0] != '#' or line[0:2] == '#!' or line[0:7] == '#SBATCH':
                    try:
                        # split at the first occurence of '='
                        split_str = line.split('=', 1)
                        # put the parameter name and value in a dictionary
                        if split_str[0] == 'FILENAME':
                            inputfilename[split_str[0]] = split_str[1]
                            continue
                        parameter_dic[split_str[0]] = eval(split_str[1])

                        try:
                            parameter_length
                        except NameError:
                            parameter_length = len(parameter_dic[split_str[0]])

                        # all the parameters must have the same length
                        if len(parameter_dic[split_str[0]]) != parameter_length:
                            raise ValueError("Error in parameter: '{}'. Length of parameter list must be the same".format(split_str[0]))

                        # put the parameter name and regex pattern in a dictionary
                        pattern_dic[split_str[0]] = re.compile('{{'+split_str[0]+'}}')
                    except AttributeError:
                        raise AttributeError('Line number {}. Unknown command in parameter file...'.format(i+1))
    # -----------------------------------------------------

    # -----------------------------------------------------
    # read template and store it
    template_f = open(template_file, 'r')
    template_lines = template_f.readlines()
    # -----------------------------------------------------


    # Write out the input files based on template and parameter files
    parameter_file_lst = []
    for index in np.arange(parameter_length):
        write_filename = multiple_replace(parameter_dic,
                                          inputfilename['FILENAME'],
                                          index)
        # remove the newline character
        write_filename = write_filename.rstrip('\n')
        with open(write_filename, 'w') as fout:
            for line in template_lines:
                # change the line if there is pattern
                # match or return the original line
                new_line = multiple_replace(parameter_dic,
                                            line,
                                            index)
                fout.write(new_line)

        parameter_file_lst.append(write_filename)
    return parameter_file_lst

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("template", help='specify template file path')
    parser.add_argument("parameter", help='specify parameter file path')
    args = parser.parse_args()

    ltt(args.template, args.parameter)
