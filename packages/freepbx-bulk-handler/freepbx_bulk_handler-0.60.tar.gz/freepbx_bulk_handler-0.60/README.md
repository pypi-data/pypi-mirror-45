# FreePBX Bulk Handler
This python package is designed to assist administrators of FreePBX systems when
they need to use the Bulk Handler module.

Currently only the Extension Class has been created but I think/hope that I've
set this project up to support other Python Classes for the other features of
the FreePBX Bulk Handler module.

# How to use this repository
An example script has been provided to show you the gist of how to use the freepbx_bulk_handler
package.
* Copy the ```extensions_to_create.csv-example``` to ```extensions_to_create.csv```.
* Run the ```EXAMPLE_SCRIPT.py``` to create the output csv file (named ```extensions_to_import.csv```
by default).

# How to use the freepbx_bulk_handler package
The freepbx_bulk_handler package is available via pypi.  Issue the command ```pip3 install freepbx_bulk_handler``` to 
install this package into your Python environment.

# Notes
The freepbx_bulk_handler package only supports the Extension feature of the FreePBX Bulk Handler module.  I hope to add
the other features later.

I've set some "sane defaults" for some of the fields in the freepbx_bulk_handler Extension class.  Any of these defaults
are easily overwritten by your own values.  That said, I do no sanity checking to see whether your values are viable.

Once a Python object has been created from the freepbx_bulk_handler Extension class it can no longer be modified.  So,
pre-define all your desired variables and pass them into the class at instantiation.

# Developers
I'd love any/all help in improving/expanding this package.  Feel free to issue Pull Requests and/or open a discussion
using the GitLab bug tracker for this project.