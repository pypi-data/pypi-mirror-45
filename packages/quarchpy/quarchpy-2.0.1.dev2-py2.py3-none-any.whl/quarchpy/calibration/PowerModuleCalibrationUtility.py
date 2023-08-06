'''
Quarch Power Module Calibration Functions
Written for Python 3.6 64 bit

M Dearman April 2019
'''

'''
Calibration Flow
    Connect to PPM
    Connect to Keithley
    step through a set of values and get ADC vs Reference Value
    evaluate results vs defined limits


'''

#Imports QuarchPy library, providing the functions needed to use Quarch modules
#from quarchpy import quarchDevice #, scanDevices

# Import other libraries used in the examples
from functools import reduce
#from quarchpy.calibration import *
from quarchpy.calibration.deviceHelpers import sendAndVerifyCommand,returnMeasurement
import calibrationConfig
import types
from time import sleep,time

dut = None
load = None

'''
Coefficient Class

This class holds a floating point value, and the precision at which it will be stored (in the FPGA)

    The constructor will throw an OverFlowError if the integer value overflows the specified integer width

    Value() returns the original value

    storedValue() returns the reduced precision value as would be stored in the FPGA

    hexString() returns an appropriate length hex string of the stored Value

'''

class Coefficient:
    def __init__(self, value, signed, int_width, frac_width):
        # set overflow flag if the value can't fit in the assigned integer range
        if (signed == True and abs(value) >= (2**(int_width-1))) or (signed == False and abs(value) >= (2**(int_width))):
            self.overflow = True
        else:
            self.overflow = False

        self.value = value
        self.signed = signed
        self.int_width = int_width
        self.frac_width = frac_width

    def originalValue(self):
        return self.value

    def storedValue(self):
        #shift left by required number of fractional bits, round it (to nearest integer), then shift right again
        return round(self.value*(2**self.frac_width)) / (2**self.frac_width)

    '''
    hexString(hex_chars)

    returns a hex string begining 0x with the number of hex characters specified
    '''
    def hexString(self,hex_chars):
        #shift left by required number of fractional bits, round it (to nearest integer), then and with 1's to truncate it to required length
        return "{:#0{hex_chars}x}".format(round(self.value*(2**self.frac_width)) & (2**(hex_chars*4)-1),hex_chars=(hex_chars+2))

'''
Calibration Class

This class holds a multiplier and offset coefficient as instances of the Coefficient class

    The constructor will generate multiplier and offset from a set of points in the form of a list of coordinates, using the x axis for ADC value and the y axis for reference value
    shift is an integer providing the size of the shift left that is applied to the result after multiplication and offset are applied

    Calibration(points,shift,abs_error,rel_error)

        shift is the binary left shift that takes place inside the FPGA


                LOW_12V = Calibration("uA",init_cmd,read_cmd,multiplier_cmd,offset_cmd,
                              MULTIPLIER = Coefficient(multiplier_int_width,multiplier_frac_width,multiplier_shift)
                              OFFSET = Coefficient(offset_int_width,offset_frac_width,offset_shift)

'''
class Calibration:

    def __init__(self,params):
        self.abs_error = params["abs_error"]
        self.rel_error = params["rel_error"]
        self.test_min = params["test_min"]
        self.test_max = params["test_max"]
        self.test_step = params["test_step"]
        self.units = params["units"]
        self.scaling = params["scaling"]
        self.multiplier_signed = params["multiplier_signed"]
        self.multiplier_int_width = params["multiplier_int_width"]
        self.multiplier_frac_width  = params["multiplier_frac_width"]
        self.offset_signed = params["offset_signed"]
        self.offset_int_width  = params["offset_int_width"]
        self.offset_frac_width  = params["offset_frac_width"]

    def generate(self,points):

        (thisMultiplier,thisOffset) = bestFit(points)
        # divide the offset by the hardware shift
        thisOffset /= self.scaling
        self.multiplier = Coefficient(thisMultiplier,False,self.multiplier_int_width,self.multiplier_frac_width)
        self.offset = Coefficient(-thisOffset,True,self.offset_int_width,self.offset_frac_width)            # offsets are subtracted in the hw, so we flip the sign of the offset



    '''
    getResult(adc_value)

        takes in a value and applies the current calibration to it    

    '''
    def getResult(self,adc_value):
        return round( ( (float(adc_value)/self.scaling ) * self.multiplier.storedValue() - self.offset.storedValue() ) * self.scaling )

class Verification:

    def __init__(self,params):
        self.abs_error = params["abs_error"]
        self.rel_error = params["rel_error"]
        self.test_min = params["test_min"]
        self.test_max = params["test_max"]
        self.test_step = params["test_step"]
        self.units = params["units"]

'''
Class PowerModule

    Generic Class for a quarch module with measurement channels. The function holds a list of channels, and a channel holds a list of calibrations

'''
class PowerModule:

    def __init__(self,name):
        self.name = name            # this is the name of the product that will be displayed to the user
        self.calibrations = {}      # a dictionary of calibrations supported by this module
        self.verifications = {}     # a dictionary of verifications supported by this module

class PowerModuleFactory:

    @staticmethod
    def init_cal_hd(instance,voltage):

        # get output mode
        mode = dut.sendCommand("conf:out:mode?")

        #if output mode is not 5v, set it
        while mode != "5V":
            response = dut.sendCommand("conf:out:mode 5v")
            #wait for module to change mode
            sleep(4)
            mode = dut.sendCommand("conf:out:mode?")

        # power up
        dut.sendCommand("power up")

        # disable pull down fets
        dut.sendCommand("CONFig:OUTput:12v:PULLdown OFF")
        dut.sendCommand("CONFig:OUTput:5v:PULLdown OFF")

        #set averaging to max
        dut.sendCommand("rec:ave 32k")

        # set module into calibration mode (again?)
        dut.sendCommand("write 0xf000 0xaa55")   # will not verify
        dut.sendCommand("write 0xf000 0x55aa")   # will not verify

        #check we are connected to the right channel
        if voltage.upper() == "12V":
            lower_limit = 11
            upper_limit = 13
            dut.sendCommand("sig:12v:volt 12000")
        elif voltage.upper() == "5V":
            lower_limit = 4
            upper_limit = 6
            dut.sendCommand("sig:5v:volt 5000")
        else:
            raise ValueError ("Invalid voltage specified")

        result = load.measureNoLoadVoltage()

        while (result < lower_limit or result > upper_limit):
            input("please connect the Keithley to the " + voltage + " channel, then press any key to continue")
            result = load.measureNoLoadVoltage()

    def init_cal_12v_offset(self):
 
        PowerModuleFactory.init_cal_hd(self,"12v")

        # clear the output offset register by setting it to zero
        dut.sendCommand("write 0xf011 0x0000")

    def init_verify_12v_offset(self):
 
        PowerModuleFactory.init_cal_hd(self,"12v")

        # set module to auto mode
        dut.sendCommand("write 0xf001 0x0100")

    def init_cal_12v_volt(self):

        PowerModuleFactory.init_cal_hd(self,"12v")

        # set module into calibration mode (again?)
        dut.sendCommand("write 0xf000 0xaa55")   # will not verify
        dut.sendCommand("write 0xf000 0x55aa")   # will not verify
        # clear the multiplier and offset registers by setting them to zero
        dut.sendCommand("write 0xf009 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf009 0x0000")
        dut.sendCommand("write 0xf00a 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00a 0x0000")

        #set voltage to zero and wait 1 second to settle
        dut.sendCommand("sig:12v:volt 0")
        sleep(1)

    def init_cal_12v_low(self):

        PowerModuleFactory.init_cal_hd(self,"12v")

        #set low current mode
        dut.sendCommand("write 0xf001 0x0101")
        # clear the multiplier and offset registers by setting them to zero
        dut.sendCommand("write 0xf00b 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00b 0x0000")
        dut.sendCommand("write 0xf00c 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00c 0x0000")

    def init_cal_12v_high(self):

        PowerModuleFactory.init_cal_hd(self,"12v")

        #set high current mode
        dut.sendCommand("write 0xf001 0x0102")
        # clear the multiplier and offset registers by setting them to zero
        dut.sendCommand("write 0xf00e 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00b 0x0000")
        dut.sendCommand("write 0xf00f 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00c 0x0000")

    def init_cal_12v_leakage(self):

        PowerModuleFactory.init_cal_hd(self,"12v")

        #set low current mode
        dut.sendCommand("write 0xf001 0x0101")
        # clear the multiplier register by setting it to zero
        dut.sendCommand("write 0xf00d 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00b 0x0000")
        #set load current to 5mA
        load.setReferenceCurrent(0.005)

    def hd_set_12v_volt(self,value):

        #set source voltage
        response = dut.sendCommand("sig:12v:volt " + str(value))

        # this sleep has a large impact on calibration accuracy, determined experimentally
        sleep(0.2)

        return response

    def load_meas_volt(self):

        # measaureLoadVoltage returns volts, we convert these to mV and return
        return load.measureLoadVoltage()*1000

    def hd_meas_12v_volt(self):

        response = returnMeasurement(dut,"meas:volt:12v?")

        # returnMeasurement() returns [value,units] we only need the value, which is actually ADC levels * 2^shift
        return int(response[0])

    def read_val_12v_offset(self):

        return int(dut.sendCommand("read 0x0006"),16)

    def set_coefficients_12v_offset(self):

        dut.sendCommand("write 0xf011 " + self.offset.hexString(4))

    def set_coefficients_12v_volt(self):

        dut.sendCommand("write 0xf00a " + self.multiplier.hexString(4))
        dut.sendCommand("write 0xf009 " + self.offset.hexString(4))

    def load_set_cur(self,value):

        #set load current, parameter is uA, the keithley needs amps
        response = load.setReferenceCurrent(value/1000000)
        sleep(1)
        return response

    def load_meas_cur(self):

        #get load current, the keithley returns amps, we use uA
        return load.measureLoadCurrent()*1000000

    def hd_meas_12v_cur(self):

        response = returnMeasurement(dut,"meas:cur 12v?")
        return float(response[0])*1000

    def set_coefficients_12v_low(self):
        
        dut.sendCommand("write 0xf00c " + self.multiplier.hexString(4))
        dut.sendCommand("write 0xf00b " + self.offset.hexString(4))

    def set_coefficients_12v_high(self):
        
        dut.sendCommand("write 0xf00f " + self.multiplier.hexString(4))
        dut.sendCommand("write 0xf00e " + self.offset.hexString(4))

    def meas_ref_12v_leakage(self):

        #return test current (5mA) - current measured by PPM
        return 5000-(float(returnMeasurement(dut,"meas:cur 12v?")[0])*1000)

    def read_val_12v_leakage(self):

        #return the difference between nominal voltage and the current voltage
        # we use raw DAC values as it slightly more accurate (12v nominal voltage = 0xD3F = 11.9984 V
        # return nominal voltage - current set voltage
        return 0xD3F-int(dut.sendCommand("read 0x0006"),16)

    def set_coefficients_12v_leakage(self):

        dut.sendCommand("write 0xf00d " + self.multiplier.hexString(4))

    def init_cal_5v_offset(self):
 
        PowerModuleFactory.init_cal_hd(self,"5v")

        # clear the output offset register by setting it to zero
        dut.sendCommand("write 0xf010 0x0000")

    def init_cal_5v_volt(self):

        PowerModuleFactory.init_cal_hd(self,"5v")

        # clear the multiplier and offset registers by setting them to zero
        dut.sendCommand("write 0xf002 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf009 0x0000")
        dut.sendCommand("write 0xf003 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00a 0x0000")

        #set voltage to zero and wait 1 second to settle
        dut.sendCommand("sig:5v:volt 0")
        sleep(1)

    def init_cal_5v_low(self):

        PowerModuleFactory.init_cal_hd(self,"5v")

        #set low current mode
        dut.sendCommand("write 0xf001 0x0101")
        # clear the multiplier and offset registers by setting them to zero
        dut.sendCommand("write 0xf004 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00b 0x0000")
        dut.sendCommand("write 0xf005 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00c 0x0000")

    def init_cal_5v_high(self):

        PowerModuleFactory.init_cal_hd(self,"5v")

        #set high current mode
        dut.sendCommand("write 0xf001 0x0102")
        # clear the multiplier and offset registers by setting them to zero
        dut.sendCommand("write 0xf007 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00b 0x0000")
        dut.sendCommand("write 0xf008 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00c 0x0000")

    def init_cal_5v_leakage(self):

        PowerModuleFactory.init_cal_hd(self,"5v")

        #set low current mode
        dut.sendCommand("write 0xf001 0x0101")
        # clear the multiplier register by setting it to zero
        dut.sendCommand("write 0xf006 0x0000")
        #sendAndVerifyCommand(ppm,"write 0xf00b 0x0000")
        #set load current to 5mA
        load.setReferenceCurrent(0.005)

    def hd_set_5v_volt(self,value):

        #set source voltage
        response = dut.sendCommand("sig:5v:volt " + str(value))

        # this sleep has a large impact on calibration accuracy, determined experimentally
        sleep(0.2)

        return response

    def hd_get_5v_volt(self):

        #set source voltage
        response = returnMeasurement("sig:5v:volt?")

        return int(response[0])

    def hd_meas_5v_volt(self):

        response = returnMeasurement(dut,"meas:volt:5v?")

        # returnMeasurement() returns [value,units] we only need the value, which is actually ADC levels * 2^shift
        return int(response[0])

    def read_val_5v_offset(self):

        return int(dut.sendCommand("read 0x0005"),16)

    def set_coefficients_5v_offset(self):

        dut.sendCommand("write 0xf010 " + self.offset.hexString(4))

    def set_coefficients_5v_volt(self):

        dut.sendCommand("write 0xf003 " + self.multiplier.hexString(4))
        dut.sendCommand("write 0xf002 " + self.offset.hexString(4))

    def hd_meas_5v_cur(self):

        response = returnMeasurement(dut,"meas:cur 5v?")
        return float(response[0])*1000

    def set_coefficients_5v_low(self):
        
        dut.sendCommand("write 0xf005 " + self.multiplier.hexString(4))
        dut.sendCommand("write 0xf004 " + self.offset.hexString(4))

    def set_coefficients_5v_high(self):
        
        dut.sendCommand("write 0xf008 " + self.multiplier.hexString(4))
        dut.sendCommand("write 0xf007 " + self.offset.hexString(4))

    def meas_ref_5v_leakage(self):

        #return test current (5mA) - current measured by PPM
        return 5000-(float(returnMeasurement(dut,"meas:cur 5v?")[0])*1000)

    def read_val_5v_leakage(self):

        #return the difference between nominal voltage and the current voltage
        # we use raw DAC values as it slightly more accurate (5v nominal voltage = 0xD3F = 11.9984 V
        # return nominal voltage - current set voltage
        return 0xD3F-int(dut.sendCommand("read 0x0005"),16)

    def set_coefficients_5v_leakage(self):

        dut.sendCommand("write 0xf006 " + self.multiplier.hexString(4))

    def finalise_hd(self):

        #turn off load
        load.setReferenceCurrent(0)
        load.disable()

        #turn off dut
        dut.sendCommand("power down")
        # turn dut to autoranging
        dut.sendCommand("write 0xf001 0x0100")


    def report_hd_cal(self,data):

        report = []

        if (mode=="text"):
            # check errors and generate report
            report.append('\n')
            report.append('{0:>10}'.format('Reference') + '   ' + '{0:>10}'.format('Raw Value') + '   ' + '{0:>10}'.format('Result') + '   ' + '{0:>10}'.format('Error') + '   ' + '{0:>10}'.format('Abs Error') + '   ' + '{0:>10}'.format('% Error') + '   ' + '{0:>10}'.format('Pass'))
            report.append("========================================================================================")        

            for thisLine in data:
                reference = thisLine[1]
                value = thisLine[0]
                calcValue = self.getResult(value)
                (actError,absError,relError,result) = getError(reference,calcValue,self.abs_error,self.rel_error)
                passfail = lambda x: "Pass" if x else "Fail"
                report.append('{:>10.3f}'.format(reference) + '   ' + '{:>10.1f}'.format(value) + '   ' + '{:>10.1f}'.format(calcValue) + '   ' + "{:>10.3f}".format(actError) + '   ' + "{:>10}".format(absError) + '   ' + "{:>10.2f}".format(relError) + '   ' + '{0:>10}'.format(passfail(result)))
        
            report.append("========================================================================================")  
            report.append('\n')

            report.append("Calculated Multiplier: " + str(self.multiplier.originalValue()) + ", Calculated Offset: " + str(self.offset.originalValue()))
            report.append("Stored Multiplier: " + str(self.multiplier.storedValue()) + ", Stored Offset: " + str(self.offset.storedValue()))
            report.append("Multiplier Register: " + self.multiplier.hexString(4) + ", Offset Register: " + self.offset.hexString(4))
        else:
            report.append ("TODO: NOT IMPLEMENTED YET")


        return '\n'.join(report)

    def report_hd_verify(self,data):

        report = []

        # check errors and generate report
        report.append('\n')
        report.append('{0:>10}'.format('Reference') + '   ' + '{0:>10}'.format('Result') + '   ' + '{0:>10}'.format('Error') + '   ' + '{0:>10}'.format('Abs Error') + '   ' + '{0:>10}'.format('% Error') + '   ' + '{0:>10}'.format('Pass'))
        report.append("========================================================================================")        

        for thisLine in data:
            reference = thisLine[1]
            value = thisLine[0]
            (actError,absError,relError,result) = getError(reference,value,self.abs_error,self.rel_error)
            passfail = lambda x: "Pass" if x else "Fail"
            report.append('{:>10.3f}'.format(reference) + '   ' + '{:>10.1f}'.format(value) + '   ' + "{:>10.3f}".format(actError) + '   ' + "{:>10}".format(absError) + '   ' + "{:>10.2f}".format(relError) + '   ' + '{0:>10}'.format(passfail(result)))
        
        report.append("========================================================================================")  
        report.append('\n')

        return '\n'.join(report)

    def hd_init_verify_12v(self):

        PowerModuleFactory.init_cal_hd(self,"12v")

    def hd_init_verify_12v_leakage(self):

        PowerModuleFactory.init_cal_hd(self,"12v")

        #set load current to 5mA
        load.setReferenceCurrent(0.005)

    def hd_init_verify_5v(self):

        PowerModuleFactory.init_cal_hd(self,"5v")

    def hd_init_verify_5v_leakage(self):

        PowerModuleFactory.init_cal_hd(self,"5v")

        #set load current to 5mA
        load.setReferenceCurrent(0.005)

    def hd_get_12v_volt(self):
        
        response = returnMeasurement(dut,"sig:12v:volt?")
        return int(response[0])

    # define HD PPM

    @staticmethod
    def HDPowerModule():
            
        # set the name of this module
        module = PowerModule("HD Programmable Power Module")
            
        #set global resources
        global dut
        dut = calibrationConfig.calibrationResources["quarchModule"]
        global load
        load = calibrationConfig.calibrationResources["calibrationinstrument"]

        # populate 12V channel with calibrations
        module.calibrations["12V"] = {}

        # 12V Output Offset Calibration
        thisCalibration = Calibration(
            {"abs_error":0,
             "rel_error":100,
            "test_min":10800,
            "test_max":13200,
            "test_step":1.1,
            "units":"mV",
            "scaling": 3.538305666,     # mV/bit defined by the ADC resolution, reference voltage, and potential divider on the output feedback loop
            "multiplier_signed":False,  # multiplier is not stored, don't care
            "multiplier_int_width":16,  # multiplier is not stored, don't care
            "multiplier_frac_width":16, # multiplier is not stored, don't care
            "offset_signed":True,
            "offset_int_width":12,
            "offset_frac_width":0})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_12v_offset,thisCalibration)
        thisCalibration.initVerify = types.MethodType(PowerModuleFactory.init_verify_12v_offset,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.hd_set_12v_volt,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_volt,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.read_val_12v_offset,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_12v_offset,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["12V"]["Output Offset"] = thisCalibration

        # 12V Voltage Calibration
        thisCalibration = Calibration(
            {"abs_error":1,
            "rel_error":1,
            "test_min":10,
            "test_max":14000,
            "test_step":1.1,
            "units":"mV",
            "scaling":2,                # shift of 1
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,
            "offset_int_width":10,
            "offset_frac_width":6})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_12v_volt,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.hd_set_12v_volt,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_volt,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_volt,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_12v_volt,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["12V"]["Voltage"] = thisCalibration

        #12V Low Current Calibration
        thisCalibration = Calibration(
            {"abs_error":2,
             "rel_error":2,
            "test_min":10,
            "test_max":90000,
            "test_step":1.1,
            "units":"uA",
            "scaling":16,
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,
            "offset_int_width":10,
            "offset_frac_width":6})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_12v_low,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_cur,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_12v_low,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["12V"]["Low Current"] = thisCalibration

        #12V High Current Calibration
        thisCalibration = Calibration(
            {"abs_error":2,
             "rel_error":1,
            "test_min":1000,    # 1mA
            "test_max":4000000, # 4A   
            "test_step":1.1,
            "units":"uA",
            "scaling":2048,
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,
            "offset_int_width":10,
            "offset_frac_width":6})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_12v_high,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_cur,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_12v_high,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["12V"]["High Current"] = thisCalibration

        # 12V Leakage Calibration
        thisCalibration = Calibration(
            {"abs_error":0,
             "rel_error":100,
            "test_min":10,
            "test_max":12000,
            "test_step":2,
            "units":"mV",
            "scaling": 1,     
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,       # offset is not stored, don't care
            "offset_int_width":16,      # offset is not stored, don't care
            "offset_frac_width":16})     # offset is not stored, don't care
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_12v_leakage,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.hd_set_12v_volt,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.meas_ref_12v_leakage,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.read_val_12v_leakage,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_12v_leakage,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["12V"]["Leakage"] = thisCalibration

        # populate 5V channel with calibrations
        module.calibrations["5V"] = {}

        # 5V Output Offset Calibration
        thisCalibration = Calibration(
            {"abs_error":0,
             "rel_error":100,
            "test_min":4000,
            "test_max":6000,
            "test_step":1.1,
            "units":"mV",
            "scaling": 3.538305666,     # mV/bit defined by the ADC resolution, reference voltage, and potential divider on the output feedback loop
            "multiplier_signed":False,  # multiplier is not stored, don't care
            "multiplier_int_width":16,  # multiplier is not stored, don't care
            "multiplier_frac_width":16, # multiplier is not stored, don't care
            "offset_signed":True,
            "offset_int_width":12,
            "offset_frac_width":0})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_5v_offset,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.hd_set_5v_volt,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_volt,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.read_val_5v_offset,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_5v_offset,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["5V"]["Output Offset"] = thisCalibration

        # 5V Voltage Calibration
        thisCalibration = Calibration(
            {"abs_error":1,
            "rel_error":1,
            "test_min":10,
            "test_max":6000,
            "test_step":1.1,
            "units":"mV",
            "scaling":2,                # shift of 1
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,
            "offset_int_width":10,
            "offset_frac_width":6})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_5v_volt,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.hd_set_5v_volt,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_volt,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_volt,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_5v_volt,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["5V"]["Voltage"] = thisCalibration

        #5V Low Current Calibration
        thisCalibration = Calibration(
            {"abs_error":2,
             "rel_error":2,
            "test_min":10,
            "test_max":90000,
            "test_step":1.1,
            "units":"uA",
            "scaling":16,
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,
            "offset_int_width":10,
            "offset_frac_width":6})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_5v_low,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_cur,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_5v_low,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["5V"]["Low Current"] = thisCalibration

        #5V High Current Calibration
        thisCalibration = Calibration(
            {"abs_error":2,
             "rel_error":1,
            "test_min":1000,    # 1mA
            "test_max":4000000, # 4A   
            "test_step":1.1,
            "units":"uA",
            "scaling":2048,
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,
            "offset_int_width":10,
            "offset_frac_width":6})
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_5v_high,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_cur,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_5v_high,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["5V"]["High Current"] = thisCalibration

        # 5V Leakage Calibration
        thisCalibration = Calibration(
            {"abs_error":0,
             "rel_error":100,
            "test_min":10,
            "test_max":5000,
            "test_step":2,
            "units":"mV",
            "scaling": 1,     
            "multiplier_signed":False,
            "multiplier_int_width":1,
            "multiplier_frac_width":16,
            "offset_signed":True,       # offset is not stored, don't care
            "offset_int_width":16,      # offset is not stored, don't care
            "offset_frac_width":16})     # offset is not stored, don't care
        thisCalibration.init = types.MethodType(PowerModuleFactory.init_cal_5v_leakage,thisCalibration)
        thisCalibration.setRef = types.MethodType(PowerModuleFactory.hd_set_5v_volt,thisCalibration)
        thisCalibration.readRef = types.MethodType(PowerModuleFactory.meas_ref_5v_leakage,thisCalibration)
        thisCalibration.readVal = types.MethodType(PowerModuleFactory.read_val_5v_leakage,thisCalibration)
        thisCalibration.set_coefficients = types.MethodType(PowerModuleFactory.set_coefficients_5v_leakage,thisCalibration)
        thisCalibration.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisCalibration)
        thisCalibration.report = types.MethodType(PowerModuleFactory.report_hd_cal,thisCalibration)

        module.calibrations["5V"]["Leakage"] = thisCalibration

        '''
        ************************************************************************************************************************************************************
        '''

        # populate 12V channel with verifications
        module.verifications["12V"] = {}

        # 12V Output Offset Verification
        thisVerification = Verification(
            {"abs_error":0,
             "rel_error":1,
            "test_min":10800,
            "test_max":13200,
            "test_step":1.1,
            "units":"mV"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_12v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.hd_set_12v_volt,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.hd_get_12v_volt,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.load_meas_volt,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["12V"]["Output Offset"] = thisVerification

        # 12V Voltage Verification
        thisVerification = Verification(
            {"abs_error":1,
            "rel_error":1,
            "test_min":10,
            "test_max":14000,
            "test_step":1.1,
            "units":"mV"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_12v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.hd_set_12v_volt,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_volt,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_volt,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["12V"]["Voltage"] = thisVerification

        #12V Low Current Verification
        thisVerification = Verification(
            {"abs_error":2,
             "rel_error":2,
            "test_min":100,     # 100uA
            "test_max":100000, # 100mA
            "test_step":1.1,
            "units":"uA"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_12v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_cur,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["12V"]["Low Current"] = thisVerification

        #12V High Current Verification
        thisVerification = Verification(
            {"abs_error":2,
             "rel_error":1,
            "test_min":100000,    # 100mA
            "test_max":4000000, # 4A   
            "test_step":1.1,
            "units":"uA"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_12v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_cur,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["12V"]["High Current"] = thisVerification

        # 12V Leakage Verification
        thisVerification = Verification(
            {"abs_error":0,
             "rel_error":100,
            "test_min":10,
            "test_max":12000,
            "test_step":2,
            "units":"mV"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_12v_leakage,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.hd_set_12v_volt,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_12v_cur,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["12V"]["Leakage"] = thisVerification

        # populate 5V channel with verifications
        module.verifications["5V"] = {}

        # 5V Output Offset Verification
        thisVerification = Verification(
            {"abs_error":0,
             "rel_error":1,
            "test_min":4000,
            "test_max":6000,
            "test_step":1.1,
            "units":"mV"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_5v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.hd_set_5v_volt,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.hd_get_5v_volt,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.load_meas_volt,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["5V"]["Output Offset"] = thisVerification

        # 5V Voltage Verification
        thisVerification = Verification(
            {"abs_error":1,
            "rel_error":1,
            "test_min":10,
            "test_max":14000,
            "test_step":1.1,
            "units":"mV"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_5v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.hd_set_5v_volt,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_volt,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_volt,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["5V"]["Voltage"] = thisVerification

        #5V Low Current Verification
        thisVerification = Verification(
            {"abs_error":2,
             "rel_error":2,
            "test_min":100,     # 100uA
            "test_max":100000, # 100mA
            "test_step":1.1,
            "units":"uA"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_5v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_cur,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["5V"]["Low Current"] = thisVerification

        #5V High Current Verification
        thisVerification = Verification(
            {"abs_error":2,
             "rel_error":1,
            "test_min":100000,    # 100mA
            "test_max":4000000, # 4A   
            "test_step":1.1,
            "units":"uA"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_5v,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.load_set_cur,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_cur,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["5V"]["High Current"] = thisVerification

        # 5V Leakage Verification
        thisVerification = Verification(
            {"abs_error":0,
             "rel_error":100,
            "test_min":10,
            "test_max":12000,
            "test_step":2,
            "units":"mV"})
        thisVerification.init = types.MethodType(PowerModuleFactory.hd_init_verify_5v_leakage,thisVerification)
        thisVerification.setRef = types.MethodType(PowerModuleFactory.hd_set_5v_volt,thisVerification)
        thisVerification.readRef = types.MethodType(PowerModuleFactory.load_meas_cur,thisVerification)
        thisVerification.readVal = types.MethodType(PowerModuleFactory.hd_meas_5v_cur,thisVerification)
        thisVerification.finish = types.MethodType(PowerModuleFactory.finalise_hd,thisVerification)
        thisVerification.report = types.MethodType(PowerModuleFactory.report_hd_verify,thisVerification)

        module.verifications["5V"]["Leakage"] = thisVerification


        #return the PowerModule Object
        return module

'''
bestFit(points)

takes in a list of x and y coordinates of ADC values (x value) and reference values (y value)
and returns offset and gradient for the best fit straight line approximation of those points
'''
def bestFit(points):

    # calculate the mean value of all x coordinates
    AveX = reduce(lambda sum,point : sum+point[0],points,0)/len(points)
    # calculate the mean value of all y coordinates
    AveY = reduce(lambda sum,point : sum+point[1],points,0)/len(points)
    # calculate the sum of (x-x'mean)*(y-y'mean) for all points
    SumXY = reduce(lambda sum,point : sum + ((point[0]-AveX)*(point[1]-AveY)), points, 0)
    # calculate the sum of (x-x'mean)*(x-x'mean) for all points
    SumX2 = reduce(lambda sum,point : sum + ((point[0]-AveX)*(point[0]-AveX)), points, 0)

    Slope = SumXY/SumX2
    Intercept = AveY-(Slope*AveX)
        
    return Slope,Intercept

'''
getError(reference_value,calculated_value,abs_error,rel_error)

    takes in a reference value and a calculated value
    returns a tuple with actual error (reference-calculated), absolute error, relative error and result

    abs_error is the absolute error allowance for this calibration, in the same units as the result
    rel_error is a percentage error allowance for this calibration, it is the percentage error between calibrated and reference value after the absolute error allowance is subtracted.

'''
def getError(reference_value,calculated_value,abs_error,rel_error):

    #the error at this point is reference value - test value
    error_value = reference_value -  calculated_value
            
    # if error at this point is greater than absolute_error, set abs_error_val to absolute_error
    if abs(error_value) >= abs_error:
        # preserve the sign
        if error_value > 0:
            abs_error_val = abs_error 
        else:
            abs_error_val = - abs_error

        # calculate relative error after deduction of abolute error allowance, and as a percentage of the calculated value (not the reference value)
        rel_error_val = ((error_value - abs_error) /  calculated_value) * 100 

    # else round up to the nearest integer 
    else:
        # preserve the sign
        if error_value > 0:
            abs_error_val = int(error_value) - (error_value > 0)
        else:
            abs_error_val = int(error_value) + (error_value < 0)
        rel_error_val = 0

    # set pass/fail
    if abs(rel_error_val) <= rel_error:
        result = True;
    else:
        result = False;

    #  Actual Error, Absolute Error, Relative Error, Pass/Fail
    return([error_value,abs_error_val,rel_error_val,result])

if __name__== "__main__":
 main()

