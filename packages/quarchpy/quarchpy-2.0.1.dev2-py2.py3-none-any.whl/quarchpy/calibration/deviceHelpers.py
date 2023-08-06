
'''
Sends a command to the device and verifies that the expexted response is returned
'''
def sendAndVerifyCommand (myDevice, commandString, responseExpected="OK", exception=True):
    responseStr = myDevice.sendCommand (commandString)
    if (responseStr != responseExpected):
        if (exception):
            raise ValueError ("Command response error: " + responseStr)
        else:
            return False
    else:
        return True
    
'''
Sends a measurement command to the device and decodes the response into a float and unit
component for return
'''
def returnMeasurement (myDevice, commandString):
    valueStr = None
    unitStr = None

    # Send the command
    responseStr = myDevice.sendCommand (commandString)
    # If a space is found, suggests xxx uu format
    pos = responseStr.find(" ")
    if (pos != -1):
        valStr = responseStr[pos:].strip()
        unitStr = responseStr[:pos].strip()
        try:
            floatVal = float(valStr)
        except:
            raise ValueError ("Response does not parse to a measurement value: " + responseStr)
    # Otherwise may be a simple value (xxx format)       
    else:
        # Try to parse direct to float
        try:
            floatVal = float(responseStr)
        # If that failes, assumed to be xxxuu format
        except:
            for i, c in enumerate(responseStr):
                if c.isalpha():
                    pos = i
                    break
            if (i < len(responseStr)):
                valStr = responseStr[:pos].strip()
                unitStr = responseStr[pos:].strip()
                try:
                    floatVal = float(valStr)
                except:
                    raise ValueError ("Response does not parse to a measurement value: " + responseStr)
            else:
                raise ValueError ("Response does not parse to a measurement value: " + responseStr)
    
    # Return parsed values
    return valStr, unitStr
        
    