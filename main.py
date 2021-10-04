from config import *
from functions import *

def main():
    chute_profile = []
    if PROFILE == 0:
        chute_profile = ellipticalPointList(DIAMETER, RATIO, INNER_DIAMETER)
    else:
        chute_profile = toroidalPointList(DIAMETER, INNER_DIAMETER, RATIO)
    point_list = offset(goreProfile(chute_profile, NUM_GORES, METHOD_TYPE), ALLOWANCE)
    getDXF(point_list, FOLDER, OUTPUT, UNITS)

main()
