#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, HES-SO Valais
# All rights reserved.
#
# Initial author: Thomas Sterren
# Creation date: 2016-07-12
#
# $Id: variostring.py 1443 2016-11-21 15:16:50Z thomas.sterren $
# $Author: thomas.sterren $
# $Revision: 1443 $

import logging
import struct
import scom
from scom.scom_property import Property
from scom.pyscom_frame import ScomFrame
from scom.device.scomdevice import ScomDevice

logging.getLogger(__name__).setLevel(logging.INFO)  # DEBUG, INFO, WARNING, ERROR, CRITICAL

class VarioString(ScomDevice):
    DEFAULT_RX_BUFFER_SIZE = 1024
    DEVICE_START_ADDRESS = 101              # 101: Extender, 301: Track, 701: String
    DEVICE_MAX_ADDRESS = 101                # 109: Extender, 315: Track, 715: String

    OBJECT_TYPE_READ_USER_INFO  = 1
    OBJECT_TYPE_PARAMETER       = 2
    OBJECT_TYPE_MESSAGE         = 3
    OBJECT_TYPE_CUSTOM_DATALOG  = 5
    OBJECT_TYPE_DATALOG_TX      = 0x0101

    DEFAULT_XTENDER_SEARCH_OBJ_ID = 3000
    DEFAULT_TRACK_SEARCH_OBJ_ID = 11000

    PROPERTY_ID_READ            = 0x01
    PROPERTY_VALUE_QSP          = 0x05
    PROPERTY_MIN_QSP            = 0x06
    PROPERTY_MAX_QSP            = 0x07
    PROPERTY_LEVEL_QSP          = 0x08      # To get access level: VIEW_ONLY, BASIC, EXPERT, etc.
    PROPERTY_UNSAVED_VALUE_QSP  = 0x0D

    scom = None
    log = logging.getLogger(__name__)

    def __init__(self, deviceAddress):
        """Constructor
        Parameters:
            deviceAddress : int
                Own address of the device.
        """
        super(VarioString, self).__init__(deviceAddress)    # Call base class constructor
        self._addInstance(self.SD_VARIO_STRING)             # Add this instance to the instance counter

    @classmethod
    def classInitialize(cls, scom):
        """Tells devices with which SCOM interface to communicate."""
        cls.scom = scom

    @classmethod
    def searchDevices(cls):
        """Searches for VarioString devices on the SCOM interface."""
        FRAME_DATA_SIZE = 11
        deviceList = []

        requestFrame = scom.data_link.Frame(cls.DEFAULT_RX_BUFFER_SIZE)

        deviceIndex = cls.DEVICE_START_ADDRESS
        while deviceIndex <= cls.DEVICE_MAX_ADDRESS:
            requestFrame.initialize(srcAddr=1, destAddr=deviceIndex, dataLength=FRAME_DATA_SIZE)

            prop = Property(requestFrame)
            prop.setObjectRead(cls.OBJECT_TYPE_READ_USER_INFO, cls.DEFAULT_XTENDER_SEARCH_OBJ_ID, cls.PROPERTY_ID_READ)

            if requestFrame.isValid():
                responseFrame = cls.scom.writeFrame(requestFrame)

                if responseFrame and responseFrame.isValid():
                    print('Found VarioString on address: ' + str(deviceIndex))
                    deviceList.append(deviceIndex)
            else:
                print('Frame with error: ' + requestFrame.lastError())

            deviceIndex += 1

        if len(deviceList) == 0:
            print('No VarioString devices found')

        return deviceList

    def _readUserInfo(self, parameterId):
        """Reads a user info on the device.
        Return:
            value : bytearray
                Parameter read.
        """
        value = bytearray()
        requestFrame = ScomFrame()

        requestFrame.initialize(srcAddr=1, destAddr=self.deviceAddress, dataLength=99)

        prop = Property(requestFrame)
        prop.setObjectRead(self.OBJECT_TYPE_READ_USER_INFO, parameterId, self.PROPERTY_ID_READ)

        if requestFrame.isValid():
            responseFrame = self.scom.writeFrame(requestFrame)  # Method call is blocking

            if responseFrame and responseFrame.isValid():
                valueSize = responseFrame.responseValueSize()
                value = responseFrame[24:24 + valueSize]
            elif responseFrame.isDataErrorFlagSet():
                print('Warning: Error flag set in response frame!')
        else:
            print('Request frame not valid')

        return value

    def _readParameter(self, parameterId, propertyId=PROPERTY_VALUE_QSP):
        """Reads a parameter on the device.
        Return:
            value : bytearray
                Parameter read.
        """
        value = bytearray()
        requestFrame = ScomFrame()

        requestFrame.initialize(srcAddr=1, destAddr=self.deviceAddress, dataLength=99)

        prop = Property(requestFrame)
        prop.setObjectRead(self.OBJECT_TYPE_PARAMETER, parameterId, propertyId)

        if requestFrame.isValid():
            responseFrame = self.scom.writeFrame(requestFrame)  # Method call is blocking

            if responseFrame and responseFrame.isValid():
                valueSize = responseFrame.responseValueSize()
                value = responseFrame[24:24 + valueSize]
            elif responseFrame.isDataErrorFlagSet():
                print('Warning: Error flag set in response frame!')
        else:
            print('Request frame not valid')

        return value

    def getBatteryVoltage(self):
        """Reads and returns the actual battery voltage."""
        voltage = 0.0
        value = self._readUserInfo(self.DEFAULT_XTENDER_SEARCH_OBJ_ID)

        if value:
            voltage = struct.unpack('f', value[0:4])[0]

        return voltage

    def getInputVoltage(self):
        """Reads and returns the actual input voltage."""
        voltage = 0.0
        value = self._readUserInfo(3011)

        if value:
            voltage = struct.unpack('f', value[0:4])[0]

        return voltage

    def getBatteryChargeCurrent(self, propertyIdName='value'):
        current = 0.0

        propertyId = self.PROPERTY_VALUE_QSP
        if propertyIdName == 'min':
            propertyId = self.PROPERTY_MIN_QSP
        elif propertyIdName == 'max':
            propertyId = self.PROPERTY_MAX_QSP

        value = self._readParameter(1138, propertyId)   # 1138

        if value:
            current = struct.unpack('f', value[0:4])[0]

        return current

    def getOperatingState(self):
        state = 0

        value = self._readUserInfo(3028)

        if value:
            state = struct.unpack('H', value[0:2])[0]

        return state

    def getSoC(self):
        soc = 0.0
        value = self._readUserInfo(3007)

        if value:
            soc = struct.unpack('f', value[0:4])[0]

        return soc

    def _writeParameter(self, parameterId, value, valueSize=4, propertyFormat='float'):
        requestFrame = ScomFrame()
        requestFrame.initialize(srcAddr=1, destAddr=self.deviceAddress)

        prop = Property(requestFrame)
        prop.setObjectWrite(self.OBJECT_TYPE_PARAMETER, parameterId,
                            self.PROPERTY_VALUE_QSP, value, valueSize,
                            propertyFormat=propertyFormat)

        if requestFrame.isValid():
            responseFrame = self.scom.writeFrame(requestFrame)  # Method call is blocking

            if responseFrame.isValid():
                valueSize = responseFrame.responseValueSize()
                value = responseFrame[24:24 + valueSize]
        else:
            print('Request frame not valid')

        return value

    def setBatteryChargeCurrent(self, current):
        self._writeParameter(1138, current, propertyFormat='float')

    def setPowerEnable(self, enable):
        if enable:
            value = True
        else:
            value = False
        # TODO Remove valueSize parameter
        self._writeParameter(1576, value, valueSize=1, propertyFormat='bool')

    def getPowerEnable(self):
        enabled = False

        value = self._readParameter(1576, self.PROPERTY_VALUE_QSP)

        if value:
            enabled = struct.unpack('b', value[0:1])[0]

        return enabled