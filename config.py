# Parachute Gore DXF Generator
# Copyright © 2022 Eabha Abramson
# config.py - Contains default values for the GUI. RATIO is the only value which cannot be adjusted in the GUI.

from math import pow

# For GUI internal use
chute_profile = ["E", "T"]
chute_type = ["P", "C"]
chute_units = ["","in","","","","cm"]

# Chute major diameter in document units
DIAMETER = 18

# Chute minor diamater in document units. For elliptical chutes, this is the diameter of the hole in the top of the chute (set to 0 for no hole). For toroidal chutes, this is the minor diameter of the chute.
INNER_DIAMETER = 0

# Chute profile (0 = elliptical, 1 = toroidal)
PROFILE = 0

# Number of gores. Must be at least 4
NUM_GORES = 6

# Gore model type (0 = polygonal, 1 = circular). This describes whether a horizontal cross section of the finished chute should appear to be a polygon or a circle, for modeling purposes
MODEL_TYPE = 1

# Allowance for hemming in document units
ALLOWANCE = 0.5

# Ratio of chute height to chute radius. 0 makes a flat chute profile, while 1 results in a circular chute profile. Any other values result in elliptical chutes.
RATIO = pow(2,-0.5)

# Units of the exported DXF file (1 = inches, 5 = cm. Check the ezdxf docs at https://ezdxf.readthedocs.io/en/stable/concepts/units.html for more unit options)
UNITS = 1

# Default index of units box, for use in GUI-only version
UNITS_INDEX = 0

# File output location
FOLDER = ""
