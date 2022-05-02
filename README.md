# Parachute-Gore-DXF-Generator

This program was designed to generate the shape of a gore that we might use to sew a parachute, then generate a DXF file (with included hem allowance) that we could use to laser cut a template for the actual gores.

To use the program, run `main.py`. Adjust the options in the GUI window, and once the settings are to your liking, press the `Plot gore` button to preview the gore, and press the `Get DXF` button to save a DXF file.

Editing `config.py` will only affect the default values for the parachute gore settings. With the exception of `RATIO`, every setting listed below can be adjusted in the GUI.

The available settings are as follows:

- Chute Profile (`PROFILE`): The profile of the chute. The options for chute profiles are:
    - Elliptical
    - Toroidal
- Diameter (`DIAMETER`): The outer diameter of the parachute. For a circular model, this is just the diameter of the base of the parachute, but for the polygonal model, this represents the diameter of the circle circumscribing the base of the parachute.
- Inner Diamater (`INNER_DIAMETER`): The inner diameter of the parachute. The meaning of this option changes depending on what type of chute is being generated. For elliptical chutes, this parameter specifies the diameter of a hole in the top of the chute (setting this value to 0 removes the hole). For toroidal chutes, this option describes the inner diameter of the torus.
- Number of Gores (`NUM_GORES`): The number of gores the finished parachute should have. This affects the shape of the gore.
- Allowance (`ALLOWANCE`): This sets the magnitude of the hem allowance. The allowance is created by offsetting the points that make up the gore profile depending on the relative angles of the lines that meet at that point. Effectively, this means that each line on the outside of the gore profile is projected outwards (perpendicular to each line) by the allowance value.
- Model Type (`MODEL_TYPE`): The method the program should use to model the shape of the gore. Each results in a different type of distortion in the shape of the final parachute, but the distortion can be reduced by increasing the number of gores. The options for method are:
    - Polygonal. This models the horizontal cross section of the parachute as a polygon. This means the gores will be correctly modeled as a flat surface that is bent to match the chute profile, leading to an accurate chute profile but an undersized circumference.
    - Circular. This models the horizontal cross section of the parachute as a circle. This leads to a parachute with a more accurate circumference, but can cause the profile to be distorted.
- `RATIO`: ~~When someone gets owned on Twitter~~ The ratio of the minor axis of the chute to the major axis of the chute.
    - For elliptical chutes, this is a ratio of the chute height to the chute radius.
    - For toroidal chutes, this the ratio of the height of the chute to the difference between the chute's outer and inner radii.
- Units (`UNITS`): The units for the output DXF file to use. For a full list of options, check the [relevant page](https://ezdxf.readthedocs.io/en/stable/concepts/units.html) of the ezdxf documentation. The default GUI options are:
    - Inches (`1` or `ezdxf.units.IN`)
    - Centimeters (`5` or `ezdxf.units.CM`)
- Output Folder (`FOLDER`): The output folder to place the DXF file in. If unspecified, the file will be created in the current (program) folder. Folder delimiters must match the operating system (`\` on Windows and `/` on Unix). In `config.py`, Windows delimiters must be written as `\\` because python uses `\` as an escape character.
- File Name: The name of the output file. This can be whatever you like, but keep in mind that the program will overwrite existing files of the same name without asking first. If unspecified, the default filename will be used. The default filename is structured `DDII-GPM`, where `DD` is the diameter of the chute, `II` is the inner diameter of the chute, `G` is the number of gores, `P` is the chute profile ("E" for elliptical and "T" for toroidal), and `M` is the chute model ("C" for circular and "P" for polygonal).

##### Parachute Gore DXF Generator
##### Copyright © 2022 Eabha Abramson