# Parachute Gore DXF Generator
# Copyright © 2022 Eabha Abramson
# config.py - Contains default values for the GUI. RATIO is the only value which cannot be adjusted in the GUI.

from math import pow

# For GUI internal use
chute_profile: list[str] = ["E", "T"]
chute_model: list[str] = ["P", "C"]
chute_units: list[str] = ["","in","","","","cm"]

# Chute diameter in document units
DIAMETER: int = 20

# Spill hole diameter in document units
SPILL_HOLE_DIAMETER: int = 4

# Height distance from the top of the chute to the spill hole, normalized by the height of the chute (should be between 0 and 1, inclusive)
PULLDOWN_RATIO: float = 0.2

# Chute profile (0 = ellipsoidal, 1 = toroidal)
PROFILE: int = 0

# Number of gores. Must be at least 4
NUM_GORES: int = 6

# Gore model (0 = polygonal, 1 = circular). This describes whether a horizontal cross section of the finished chute should appear to be a polygon or a circle, for modeling purposes
MODEL: int = 1

# Allowance for hemming in document units
ALLOWANCE: float = 0.5

# Ratio of chute height to chute radius. 0 makes a flat chute profile, while 1 results in a circular chute profile. Any other values result in ellipsoidal chutes.
RATIO: float = 0.707

# Units of the exported DXF file (1 = inches, 5 = cm. Check the ezdxf docs at https://ezdxf.readthedocs.io/en/stable/concepts/units.html for more unit options). Unused in the GUI version
UNITS: int = 1

# Default index of units box, for use in GUI version
UNITS_INDEX: int = 0

# File output location
FOLDER: str = ""
