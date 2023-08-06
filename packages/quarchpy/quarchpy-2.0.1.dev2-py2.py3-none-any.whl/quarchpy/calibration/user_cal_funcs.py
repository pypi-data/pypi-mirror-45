'''
General functions to help the user perform a calibration
'''

import quarchpy

'''
Function to print useful sections of standard calibration text to the user
'''
def displayCalInstruction (instructionName):

    # Print the header for HD module calobration
    if (instructionName.lower() == "open_hd"):
        print ("")
        print ("********************************************************")
        print ("Quarch Technology Calibration System")
        print ("(C) 2019, All rights reserved")
        print ("")
        print ("V" + quarchpy.calibration.calCodeVersion)
        print ("")
        print ("********************************************************")
        print ("")
        print ("Calibration process for QTL1999 HD Power Modules")
        print ("")
        print ("********************************************************")
        print ("")
        print ("")

    # Print and return the selection for calibration action
    elif (instructionName.lower() == "select_action"):
        print ("")
        print ("Please select the action(s) to perform")
        print ("")
        print ("1 - Full calibration cycle")
        print ("2 - Verify existing calibration")
        print ("")
        selection = input ("Enter Selection: ")
        if (selection == "1"):
            return "calibrate|verify"
        if (selection == "2"):
            return "verify"
        else:
            sys.exit ("Invalid selection:" + selection)
    else:
        raise ValueError ("Unknown instruction for display: " + instructionName)