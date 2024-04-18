# P4 Templates
[![Coverage Status](https://coveralls.io/repos/github/rmaffesoli/p4_templates/badge.svg?branch=main)](https://coveralls.io/github/rmaffesoli/p4_templates?branch=main)

![Support](https://img.shields.io/badge/Support-Community-yellow.svg)

## Overview

P4 Templates are a Python library to aid in the quick creation of p4 environments for studios that have quick turn around projects and need to deploy a standard setup often.

## Installation

Currently, the running the main kernel via source doesn't require any additional libraries beyond Python3
The UI currently requires PyQt6.

## Requirements
##### CLI:
p4python                  2023.2.2581979\
##### GUI:
PyQt6                     6.6.1
##### EXE BUILD Requirements:
altgraph                  0.17.4\
packaging                 24.0\
pefile                    2023.2.7\
pyinstaller               6.5.0\
pyinstaller-hooks-contrib 2024.3\
pywin32-ctypes            0.2.2\
setuptools                69.2.0
##### Testing requirements:
colorama                  0.4.6\
coverage                  7.4.4\
iniconfig                 2.0.0\
pluggy                    1.4.0\
pytest                    8.1.1\
pytest-cov                5.0.0\
pytest-mock               3.14.0


## Server Configuration File

* Server configuration is taken from the `config.json` that can either be positioned next to the exe file or passed in as a command line argument when calling the tool.
```bash
{
    "server":{
        "port": "ssl:helix_core_server:1666",
        "user": "username",
        "password": null,
        "charset": "none"
    },
    "template_dir": ""
}

```

## Template Directory
* The `template` directory can either live next to the exe file, be defined within the exe file, or passed in as a command line argument.

## Templates
* If you're looking to define new templates by hand, the template structure can be viewed in the example templates. Alternatively you can use the template Editor UI to author new templates with the proper formatting in place.

## CLI Usage

* To process a specific json template pass in the file path with the -t flag.
You can find example templates in the `p4templates/templates` directory. Copy one if these templates, edit to fit your needs, and then process it to add the requested components to your p4d server. To Note: You will need the p4 Permissions level required to complete these actions for the script to succeed.

```bash
python ./kernel/process_template.py -t /path/to/template/file.json
```

* If you have a specific template predefined you can use the -n --name option that corresponds to either the name field as defined in the template file, or the filename itself.

```bash
python ./kernel/process_template.py -n template_name
```

* If you are using parameter tags in your template you can use the -p,--parameter flag to input these values for processing.
The syntax is as follows with a ':' acting a string delimiter between the key and value.
Any number of parameters may be passed in separated by a space.
For instance if your template uses the parameters 'project' and 'dept' you would use the following syntax to pass the substitutions into the cli utility.
Within your json file the syntax for parameters is to use curly braces to identify parameter values.
For example a template json string of:
`{"streams": [{"depot": "{dept}_depot", "name": "{project}_{dept}_main"}]}` would result in the creation of mainline stream named `demo_3D_main` within the `3D_depot` depot.

```bash
python ./kernel/process_template -n default_unreal_template -p project:demo dept:3D
```

* the -d,--dryrun flag can be used to preview the the template output with the parameter substitutions applied. The output will be printed to the command line instead of being processed by the server.

```bash
python ./kernel/process_template -n default_unreal_template -p project:demo dept:3D -d
```

## File Population

The template system utilizes Helix Core's branch mappings and the p4 populate command to duplicate files and folders from one depot position on the server into the new template project. For this to operate correctly I recommend you establish a separate template project depot on your p4d server and then use those boilerplate setups as your duplication source.

For example, in the following snippet we see the branch mapping section from a p4 setup template showing how the view section is defined for file propagation including file renaming.

```
  "branches": [
    {
      "name": "{project}_populate",
      "options": [
        "unlocked"
      ],
      "view": {
        "//populate_demo/main/old_project/...": "//{project}_depot/{project}_main/new_project/...",
        "//populate_demo/main/old_project/old_project.py": "//{project}_depot/{project}_main/new_project/new_project.py"
      }
    }
  ],
```

## GUI Usage

* To load the editor GUI use the launch the exe. By default the exe will look for a config file and template directory next to the executable itself, however these values can be passed in as command line arguments as well. The template directory can also be defined in the config file itself.

```bash
E:\repos\p4templates\bin>E:\repos\p4templates\bin\p4_template.exe -h
usage: p4_template.exe [-h] [-c CONFIG] [-t TEMPLATE_DIR]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
  -t TEMPLATE_DIR, --template_dir TEMPLATE_DIR
```


```bash
python ./p4_template_tool.py
```
* Upon loading the UI you will be presented with the template loader execution window. Any variable parameter will be lifted and shown in the field below the template selection drop down. Once all parameters have a valid value then you will be able to process the template. If you would like to edit a current template the `Edit` button will open the Edit Template window with the data for the currently selected template. This can then be either saved as the same file name or as a new name to create a copy. If you would like to create a new template, the `New` button will open the Edit Template window without any predefined values.

* A video walkthrough of UI operation can be found [here](https://share.descript.com/view/qB7vWvmbhRO).

## EXE Build
* If you have the pyinstaller requirements installed. `build_windows.bat` will create a self contained executable in the bin directory.

## Testing

* run_tests.bat should take care of things so long as you have the testing requirements installed. Currently basic unit tests are in place. If you update the code at all be sure to update the tests accordingly. Test results will be available via command line and coverage reports can be viewed via the `html-cov/index.html` file that will be generated by coverage.
* This script will attempt to upload test results to coveralls, however don't be concerned if this portion fails as it does require a private repo_token that will not be included in this github repository.

## TODO Wishlist
- [ ] Documentation
  - More than a readme and video walkthrough is likely needed.
- [ ] Validation
  - I would prefer if this tool could validate the entries per tab, and particularly on the type map to stop and erroneous edits.
- [ ] Cleaner CLI
  - entry point other than kernel\process_template.py?
  - A separate entry point should be stabilized beyond reaching into the kernel directly.
