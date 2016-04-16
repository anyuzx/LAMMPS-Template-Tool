## Description

This tool can write Lammps input files based on a template and a parameter file.

## Usage

The repository contains one template file example and one parameter file example. Let's look at `parameter.txt`

```
# this is a comment line

# specify the file name
FILENAME=Chr5_145870001_157870001_G2.5_SC_{{index_1}}_short.in

index_1=np.arange(1,31)
index_2=np.arange(1,31)
index_3=np.arange(1,31)

# create the random seed
langevin_seed=np.random.randint(1,10000000,size=30)
```

All keyword or parameter should be specified by using `=` sign. Keyword `FILENAME` is used to specify the file name for Lammps input file. The value of `FILENAME` can also have parameters in it. The value of all parameters must have the same length. `numpy` or `python` can be used to specify the value of the parameter. It will be evaluated correctly. Use the following command to run the tool

```python
python ltt.py template.in parameter.txt
```
