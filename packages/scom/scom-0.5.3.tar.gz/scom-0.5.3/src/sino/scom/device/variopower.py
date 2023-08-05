#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, HES-SO Valais
# All rights reserved.
#
# Initial author: Thomas Sterren
# Creation date: 2016-07-12
#
# $Id: variopower.py 1577 2016-12-29 11:30:25Z thomas.sterren $
# $Author: thomas.sterren $
# $Revision: 1577 $

import struct
import logging
#import sino.scom
from ..property import Property
from ..frame import Frame as ScomFrame
from ..device.scomdevice import ScomDevice

logging.getLogger(__name__).setLevel(logging.INFO)  # DEBUG, INFO, WARNING, ERROR, CRITICAL

class VarioPower(ScomDevice):

    DEFAULT_RX_BUFFER_SIZE = 1024
    DEVICE_START_ADDRESS = 701              # 101: Extender, 301: Track, 701: String/Power
    DEVICE_MAX_ADDRESS = 705                # 109: Extender, 315: Track, 715: String/Power

    OBJECT_TYPE_READ_USER_INFO  = 1
    OBJECT_TYPE_PARAMETER       = 2
    OBJECT_TYPE_MESSAGE         = 3
    OBJECT_TYPE_CUSTOM_DATALOG  = 5
    OBJECT_TYPE_DATALOG_TX      = 0x0101

    DEFAULT_VARIOPOWER_SEARCH_OBJ_ID = 15000

    PROPERTY_ID_READ            = 0x01
    PROPERTY_VALUE_QSP          = 0x05
    PROPERTY_MIN_QSP            = 0x06
    PROPERTY_MAX_QSP            = 0x07
    PROPERTY_LEVEL_QSP          = 0x08      # To get access level: VIEW_ONLY, BASIC, EXPERT, etc.
    PROPERTY_UNSAVED_VALUE_QSP  = 0x0D
    PROPERTY_LAST               = 0xEE      # Not Studer specific. Introduced by sth

    scom = None
    log = logging.getLogger(__name__)

    paramInfoTable = {'wiringTypeConfig' :              {'name': 'wiringTypeConfig',               'number': 14001, 'propertyFormat': 'enum',  'default': 1,    'studerName': 'Configuration of wiring type' },
                      'batteryMaximumVoltage':          {'name': 'batteryMaximumVoltage',          'number': 14002, 'propertyFormat': 'float', 'default': 48.0, 'studerName': 'uBatMax'},
                      'batteryMinimumVoltage':          {'name': 'batteryMinimumVoltage',          'number': 14003, 'propertyFormat': 'float', 'default': 48.0, 'studerName': 'uBatMin'},
                      'regulationMode':                 {'name': 'regulationMode',                 'number': 14071, 'propertyFormat': 'enum',  'default': 0,    'studerName': 'regModeS'},
                      'gridReferenceCurrent':           {'name': 'gridReferenceCurrent',           'number': 14073, 'propertyFormat': 'float', 'default': 0.0,  'studerName': 'iPvSConsigne'},
                      'batteryChargeReferenceCurrent':  {'name': 'batteryChargeReferenceCurrent',  'number': 14075, 'propertyFormat': 'float', 'default': 0.0,  'studerName': 'iBatSConsigne' },
                     }

    userInfoTable = {'batteryVoltage':  {'name': 'batteryCurrent',    'number': 15000, 'propertyFormat': 'float', 'default': 0.0, 'studerName': 'Battery voltage'},
                     'batteryCurrent':  {'name': 'batteryCurrent',    'number': 15001, 'propertyFormat': 'float', 'default': 0.0, 'studerName': 'Battery current'},
                     'pvVoltage':       {'name': 'pvVoltage',         'number': 15004, 'propertyFormat': 'float', 'default': 0.0, 'studerName': 'PV voltage'},
                     'busVoltage':      {'name': 'busVoltage',        'number': 15004, 'propertyFormat': 'float', 'default': 0.0, 'studerName': 'PV voltage'},
                     'operatingMode':   {'name': 'operatingMode',     'number': 15013, 'propertyFormat': 'enum',  'default': 0,   'studerName': 'PV operating mode'},
                     'softVersionMsb':  {'name': 'softVersionMsb',    'number': 15077, 'propertyFormat': 'float', 'default': 0.0, 'studerName': 'ID SOFT msb'},
                     'softVersionLsb':  {'name': 'softVersionLsb',    'number': 15078, 'propertyFormat': 'float', 'default': 0.0, 'studerName': 'ID SOFT lsb'},
                    }

    opModeToStringTable = {0: u'Night',
                           1: u'Security',
                           2: u'OFF',
                           3: u'Charge',
                           4: u'limUBat',
                           5: u'limIBat',
                           6: u'limP',
                           7: u'limIPv',
                           8: u'limT',
                           9: u'---',
                          10: u'limIBsp',
                          11: u'limUPv'}

    stringToOpModeTable = {u'Night': 0,
                           u'Security': 1,
                           u'OFF': 2,
                           u'Charge': 3,
                           u'limUBat': 4,
                           u'limIBat': 5,
                           u'limP': 6,
                           u'limIPv': 7,
                           u'limT': 8,
                           u'---': 9,
                           u'limIBsp': 10,
                           u'limUPv': 11}

    def __init__(self, device_address):
        """
        :param device_address The device number on the SCOM interface. Own address of the device.
        :type device_address int
        """
        super(VarioPower, self).__init__(device_address)             # Call base class constructor
        self._add_instance(self.SD_VARIO_POWER)                      # Add this instance to the instance counter

        # Give paramInfoTable to ScomDevice base class
        super(VarioPower, self)._set_param_info_table(self.paramInfoTable)

    @classmethod
    def classInitialize(cls, scom):
        """Tells devices with which SCOM interface to communicate."""
        cls.scom = scom

    @classmethod
    def _get_scom(cls):
        """Implementation of ScomDevice interface.
        """
        return cls.scom

    @property
    def device_type(self):
        """Implementation of ScomDevice interface.
        """
        return self.SD_VARIO_POWER

    @property
    def software_version(self):
        """Implementation of ScomDevice interface.
        """
        return self.getSoftwareVersion()

    @classmethod
    def searchDevices(cls):
        """Searches for VarioPower devices on the SCOM interface."""
        deviceList = []

        requestFrame = scom.data_link.Frame(cls.DEFAULT_RX_BUFFER_SIZE)

        deviceIndex = cls.DEVICE_START_ADDRESS
        while deviceIndex <= cls.DEVICE_MAX_ADDRESS:
            requestFrame.initialize(srcAddr=1, destAddr=deviceIndex)

            prop = Property(requestFrame)
            prop.setObjectRead(cls.OBJECT_TYPE_READ_USER_INFO, cls.DEFAULT_VARIOPOWER_SEARCH_OBJ_ID, cls.PROPERTY_ID_READ)

            if requestFrame.isValid():
                responseFrame = cls.scom.writeFrame(requestFrame, 0.5) # Set a short timeout during search)

                if responseFrame and responseFrame.isValid():
                    cls.log.info('Found VarioPower on address: ' + str(deviceIndex))
                    deviceList.append(deviceIndex)
            else:
                cls.log.warning('Frame with error: ' + requestFrame.lastError())

            deviceIndex += 1

        if len(deviceList) == 0:
            cls.log.warning('No VarioPower devices found')

        return deviceList

    @classmethod
    def _stringToRegulationMode(cls, s):
        """Converts a human readable sting to regModeS.
        """
        regModeS = 0

        if s == u'uPv':
            regModeS = 1
        elif s == u'iPv':
            regModeS = 2
        elif s == u'pPv':
            regModeS = 4
        elif s == u'iBat':
            regModeS = 8
        elif s == u'PVSim':
            regModeS = 16
        elif s == u'IUcurve':
            regModeS = 32

        return regModeS

    @classmethod
    def _wiringTypeToString(cls, wtc):
        str = ''
        if wtc == 1:
            str = 'independent'
        elif wtc == 2:
            str = 'serial'
        elif wtc == 4:
            str = 'parallel'
        return str

    def getBatteryVoltage(self):
        """Reads and returns the actual battery voltage."""
        return self._read_user_info_ex(self.userInfoTable['batteryVoltage'])

    def getBatteryCurrent(self):
        """Reads and returns the actual battery current."""
        return self._read_user_info_ex(self.userInfoTable['batteryCurrent'])

    def getOperatingMode(self):
        """Reads and returns the actual operating mode."""
        return self._read_user_info_ex(self.userInfoTable['operatingMode'])

    def getGridVoltage(self):
        """Reads and returns the actual PV/grid voltage."""
        return self._read_user_info_ex(self.userInfoTable['busVoltage'])

    def getSoftwareVersion(self):
        idSoftMsb = self._read_user_info_ex(self.userInfoTable['softVersionMsb'])
        idSoftLsb = self._read_user_info_ex(self.userInfoTable['softVersionLsb'])

        if idSoftMsb and idSoftLsb:
            idSoftMajorVersion = int(idSoftMsb) >> 8
            idSoftMinorVersion = int(idSoftLsb) >> 8
            idSoftRevision = int(idSoftLsb) & 0xFF

            return {'major': idSoftMajorVersion, 'minor': idSoftMinorVersion, 'patch': idSoftRevision }
        return {'major': 0, 'minor': 0, 'patch': 0 }

    def getRegulationMode(self):
        """Reads and returns the actual regulation mode."""
        return self._read_parameter_info('regulationMode')

    def setRegulationMode(self, regulationMode):
        """Sets the regulation mode of the device.

        :param The regulation mode as string 'uPv, iPV, etc.'
        :type str
        :return True on success
        """
        regModeS = self._stringToRegulationMode(regulationMode)

        if regModeS != 0:
            return self._write_parameter_info('regulationMode', regModeS, property_id=self.PROPERTY_VALUE_QSP)
        return False

    def getBatteryChargeCurrent(self, propertyIdName='value'):
        current = 0.0

        propertyId = self.PROPERTY_VALUE_QSP
        if propertyIdName == 'min':
            propertyId = self.PROPERTY_MIN_QSP
        elif propertyIdName == 'max':
            propertyId = self.PROPERTY_MAX_QSP

        value = self._read_parameter(1138, propertyId)   # 1138

        if value:
            current = struct.unpack('f', value[0:4])[0]

        return current

    def setGridReferenceCurrent(self, current):
        """Sets the grid reference current.

        Positive values for parameter 'current' means charging the battery!
        If you want to feed energy to the grid you need to give a negative
        value.
        Please take in mind that the battery may not be able to give the
        needed current as between the grid current and the battery current
        is about a factor of GridVoltage/BatteryVoltage (ex. 700V/50V=14).
        The BatteryMonitor may limit the current drawn by the battery according
        to the values presented by the ApollionsCube's BMS.

        Takes only affect if the regulation mode is set to 'iPv'.
        """
        try:
            self._write_parameter(14073, current, property_format='float', property_id=self.PROPERTY_UNSAVED_VALUE_QSP)
        except:
            return False
        return True

    def setBatteryChargeReferenceCurrent(self, current, propertyId=PROPERTY_UNSAVED_VALUE_QSP):
        """Sets the battery charge reference current.

        Takes only affect if the regulation mode is set to 'iBat'.
        """
        return self._write_parameter_info('batteryChargeReferenceCurrent', current, property_id=propertyId)

    def getBatteryChargeReferenceCurrent(self, propertyId=PROPERTY_LAST):
        """

        """
        return self._read_parameter_info('batteryChargeReferenceCurrent', property_id=propertyId)

    def setPowerEnable(self, enable):
        """Enables/disables the VarioPower
        """
        try:
            if (enable):
                self._write_parameter(14081, 1, property_format='int32')
            else:
                self._write_parameter(14082, 1, property_format='int32')
        except:
            return False
        return True

    def getWiringTypeConfig(self):
        return self._read_parameter_info('wiringTypeConfig')

    def setWiringTypeConfig(self, newValue=2):
        """Set the wiring type of the device.

            1: Independent, 2: Serial, 3: Parallel
        """
        return self._write_parameter_info('wiringTypeConfig', newValue, self.PROPERTY_VALUE_QSP)

    def getWiringTypeConfigAsString(self):
        wtc = self.getWiringTypeConfig()
        return self._wiringTypeToString(wtc)

    def getBatteryMaximumVoltage(self):
        return self._read_parameter_info('batteryMaximumVoltage')

    def setBatteryMaximumVoltage(self, newValue):
        """Sets the maximum battery voltage.
        """
        return self._write_parameter_info('batteryMaximumVoltage', newValue, self.PROPERTY_UNSAVED_VALUE_QSP)

    def getBatteryMinimumVoltage(self):
        return self._read_parameter_info('batteryMinimumVoltage')

    def setBatteryMinimumVoltage(self, newValue):
        """Sets the minimum battery voltage.
        """
        return self._write_parameter_info('batteryMinimumVoltage', newValue, self.PROPERTY_UNSAVED_VALUE_QSP)
