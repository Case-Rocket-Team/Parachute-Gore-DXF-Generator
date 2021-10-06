# Parachute-Gore-DXF-Generator

This program was designed to generate the shape of a gore that we might use to sew a parachute, then generate a DXF file (with included hem allowance) that we could use to laser cut a template for the actual gores.

To use the program, run `main.py`. Adjust the options in the GUI window, and once the settings are to your liking, press the `Plot gore` button to preview the gore, and press the `Get DXF` button to save a DXF file.

Most settings can be changed in the GUI, and editing the config file will only affect the default values for these settings. The settings that can only be changed in the config file are starred below.

The available settings are as follows:

- `DIAMETER`: The outer diameter of the parachute. For a circular model, this is just the diameter of the base of the parachute, but for the polygonal model, this represents the diameter of the circle circumscribing the base of the parachute.
- `INNER_DIAMETER`: The inner diameter of the parachute. The meaning of this option changes depending on what type of chute is being generated. For elliptical chutes, this parameter specifies the diameter of a hole in the top of the chute (setting this value to 0 removes the hole). For toroidal chutes, this option describes the inner diameter of the torus.
- `PROFILE`: The profile of the chute. The options for chute profiles are:
    - `0`: Elliptical
    - `1`: Toroidal
- `NUM_GORES`: The number of gores the finished parachute should have. This affects the shape of the gore.
- `MODEL_TYPE`: The method the program should use to model the shape of the gore. Each results in a different type of distortion in the shape of the final parachute, but the distortion can be reduced by increasing the number of gores. The options for method are:
    - `0`: Polygonal. This models the horizontal cross section of the parachute as a polygon. This means the gores will be correctly modeled as a flat surface that is bent to match the chute profile, leading to an accurate chute profile but an undersized circumference.
    - `1`: Circular. This models the horizontal cross section of the parachute as a circle. This leads to a parachute with a more accurate circumference, but can cause the profile to be distorted.
- `ALLOWANCE`: This sets the magnitude of the hem allowance. The allowance is calculated by offsetting the points that make up the gore profile depending on the relative angles of the lines that meet at that point. Effectively, this means that each line on the outside of the gore profile is projected outwards (perpendicular to each line) by the allowance value.
- \*`RATIO`: ~~When someone gets owned on Twitter~~ The ratio of the minor axis of the chute to the major axis of the chute.
    - For elliptical chutes, this is a ratio of the chute height to the chute radius.
    - For toroidal chutes, this the ratio of the height of the chute to the difference between the chute's outer and inner radii.
- \*`UNITS`: The units for the output DXF file to use. For a full list of options, check the [relevant page](https://ezdxf.readthedocs.io/en/stable/concepts/units.html) of the ezdxf documentation. The most relevant options for parachute design are:
    - `1`: Inches (also `ezdxf.units.IN`)
    - `5`: Centimeters (also `ezdxf.units.CM`)
- \*`FOLDER`: The output folder to place the DXF file in. If unspecified, the file will be created in the current folder. Folder delimiters must match the operating system (`\\` on Windows due to character escaping and `/` on Unix).
- `OUTPUT`: The name of the created file. This setting is currently unused, but a filename option is in the works.