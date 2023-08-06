from typing import (List, Dict, Tuple)
import pandas
import numpy
import sys
import pympi  # Import pympi to work with elan files
import ntpath  # needed for the basename function
import os
from . import xml_validation
from . import ErrorCodesBPF2EAF


ELAN_XML_SCHEMA: str = "../schemas/EAFv3.0.xsd"


class BPFParser:

    # add : so we do not have to add it in later steps
    __supportedTiers:List[str] = ['ORT:', 'KAN:', 'MAU:', 'TRN:']
    # add : so we do not have to add it in later steps
    __headerTiers:List[str]    = ['LHD:', 'REP:', 'SNB:', 'SAM:', 'SBF:', 'SSB:', 'NCH:', 'SPN:', 'LBD:']

    __tiersToProcess:List[str] = None   # which tiers should be processed (needs to be subset from supportedTiers
    __topLevelTier:str = None           # which tier should be the top level.

    __bpfContent: Dict[str, pandas.DataFrame] = dict()

    __sampleRate: int = -1

    # location of the signal file
    __signalLocation = None

    __tierNamePrefix = None

    #
    # Constructor that lets one define under which topLevel tier the MAUS tiers should be put,
    # and which tiers should be used
    #
    def __init__(self,
                 sampleRate:int,
                 signalLocation: str,
                 topLevelTier: str = "ORT:",
                 tiersToProcess: List[str] = None,
                 tierNamePrefix: str = ""):
        self.__sampleRate = sampleRate
        self.__signalLocation = signalLocation

        self.__topLevelTier = topLevelTier

        self.__tierNamePrefix = tierNamePrefix

        if(tiersToProcess == None):
            self.__tiersToProcess = self.__supportedTiers
        else:
            a_set = set(tiersToProcess)
            b_set = set(self.__supportedTiers)
            if not a_set.issubset(b_set):
                sys.stderr.write("Unsupported tiers requested. Ignoring the unsupported ones")

            self.__tiersToProcess = b_set.intersection(a_set)


    #
    # Method that removes whitespaces in the third KAN column
    #
    def __replaceKANTierSpaces(self, filename: str):
        # extract the KAN tier as we want it and save it to tmpFile
        sedCommand: str = "sed -i -e '/^KAN:/s/ //3g' " + filename
        #print("Executing: " + sedCommand)
        os.system(sedCommand)

        #sedCommand: str = "sed -i -e '/^KAN:/s/ //3g' " + filename + " && grep '^KAN:' " + filename + "> " + tmpFile
        #os.system(sedCommand)
        # remove the old KAN tier
        #sedCommand: str = "sed -i /^KAN:.*/d " + filename
        #print("Executing: " + sedCommand)
        #os.system(sedCommand)

        # add the new KAN tier
        #catCommand: str = "cat " + tmpFile + " >> " + filename
        #print("Executing: " + catCommand)
        #os.system(catCommand)

        #os.remove(tmpFile)
        return()

    #
    # Method that replaces whitespaces with semicolon in the fourth TRN column
    #
    def __replaceTRNTierSpaces(self, filename: str):
        # extract the KAN tier as we want it and save it to tmpFile
        sedCommand: str = "sed -i -e '/^TRN:/s/ /;/5g' " + filename
        os.system(sedCommand)

        return()

    #
    # Method that reads the content of the filename to class and saves it as pandas data frames
    #
    def readBPFFile(self, filename: str) -> None:

        #### corret KAN and TRN tier
        self.__replaceKANTierSpaces(filename)
        self.__replaceTRNTierSpaces(filename)

        df = self.__readBPFFileInternal(filename)
        # print(df["tiername"].unique())

        tiernamesPresent:List[str] = df["tiername"].unique()
        if not self.__checkIfTierNamesMatch(self.__supportedTiers, tiernamesPresent):
            sys.stderr.write("BPF file contains tiers that are not supported. Supported tiers are "
                             + str(self.__supportedTiers) + ". Ignoring unsupported tiers.")

        for currTier in self.__tiersToProcess:
            # print("Extracting tier " + currTier)
            currDF = df[df["tiername"].str.contains(currTier)]
            currDF = currDF.dropna(axis='columns')

            if len(currDF) > 0:  # only add the tiers that do exist
                self.__bpfContent[currTier] = currDF

        if not self.__checkIfTierExists("MAU:"):
            sys.stderr.write("BPF file does not contain mandatory MAU tier. Aborting")
            quit(ErrorCodesBPF2EAF.ERROR_CODE_MAU_TIER_MISSING)
        # csv.register_dialect('bpfDialect', delimiter=' ')

        # with open(filename, 'r') as f:
            # reader = csv.reader(f, dialect='bpfDialect')
            # for row in reader:
                # print(row)

    #
    # Method that reads a filename as a BPF file and forces it to have 5 columns (if not specified otherwise)
    #
    # col_names : name of the columns (and implicitely also the number of columns) to read in
    #
    def __readBPFFileInternal(self, filename: str, col_names: List[str] = ["tiername", "B", "C", "D", "E"]) \
            -> pandas.DataFrame:
        df = pandas.read_csv(filename, names=col_names, delim_whitespace=True)
        return(df)

    #
    # Check a list of tier names against a list of supported tiernames if they all are supported.
    # This can, e.g., be used to issue a warning to the user
    #
    def __checkIfTierNamesMatch(self, tiernamesSupported: List[str], currentTiernames: List[str]) -> bool:
        # print("Current tier names: " + currentTiernames)
        currentTiernamesInternal = currentTiernames

        for currHeaderTierName in self.__headerTiers:
            currentTiernamesInternal \
                = numpy.delete(currentTiernamesInternal, numpy.argwhere(currentTiernamesInternal==currHeaderTierName))

        a_set = set(tiernamesSupported)
        b_set = set(currentTiernamesInternal)
        if len(a_set.intersection(b_set)) > 0:
            return (True)
        return False

    #
    # Check if tier exists
    #
    def __checkIfTierExists(self, tierName) -> bool:
        if self.__bpfContent.get(tierName) is None:
            return False
        else:
            return True

    #
    # Method that gets the information from the MAU tier in samples
    #
    def __getTimingInformationFromMAUTier(self, wordIndex: int) -> Tuple[int, int]:
        mauDF: pandas.DataFrame = self.__bpfContent.get("MAU:")
        startTime: int = -1
        endTime: int = -1

        for index, currRow in mauDF.iterrows():
            wordIndexMAU: int = int(currRow[3])
            phonemeStartTime: int = int(currRow[1])
            phonemeDuration: int = int(currRow[2])

            if wordIndexMAU == wordIndex and startTime == -1: # if we first hit the start time -> save it
                startTime = phonemeStartTime
            # for brevity sake, always save the end time, until we no longer see MAU entries with the same wordIndex
            if wordIndexMAU == wordIndex:
                endTime = (phonemeStartTime + phonemeDuration)

            if wordIndexMAU == (wordIndex + 1): # if we are one further, stop iterating
                return (startTime, endTime)

        # for the last element we will be here -> return tuple also
        return (startTime, endTime)

    #
    # Method that calls the pympi hack the removes the double namespace information which gets added
    # if an EAF file does already exist. Issue reported to github
    # https://github.com/dopefishh/pympi/issues/15
    #
    def __pympiEAFHack(self, filename):
        sedCommand: str = "sed -i -e 's#xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"##1' " + filename
        os.system(sedCommand)
        sedCommand: str \
            = "sed -i -e 's#xsi:noNamespaceSchemaLocation=\"http://www.mpi.nl/tools/elan/EAFv2.8.xsd\" ##1' " + filename
        os.system(sedCommand)

    #
    # Method that converts the BPF to an ELAN file and writes it out
    #
    def convertToEAF(self, outFilename: str, ling: str) -> None:

        eafObj = None
        fileAlreadyExisted = False
        if not os.path.isfile(outFilename):  # if file does not exist, than we create it
            eafObj = pympi.Elan.Eaf()

            # set a header
            eafObj.header = {'MEDIA_FILE': '',
                             'TIME_UNITS': 'milliseconds'}

            # get relative path (assuming it is in the same folder)
            signalName = ntpath.basename(self.__signalLocation)
            eafObj.add_linked_file(file_path=self.__signalLocation,
                                   relpath=signalName,
                                   mimetype="audio/x-wav")
        else:  # otherwise just open it and append the stuff
            eafObj = pympi.Elan.Eaf(outFilename)
            fileAlreadyExisted = True  # this is needed for the pympi hack for the namespace bug

        # HINT: in the following, the hard coded tiernames are the ones that come out of the BPF files,
        # the other ones are prefixed (if a prefix is set).
        # HINT: all tier names are internally saved with : which means they have to be removed by [:-1] before
        # adding them to the eaf object
        for currTierName in self.__tiersToProcess:
            # print("Processing tier " + currTierName)
            currDF: pandas.DataFrame = self.__bpfContent.get(currTierName)
            # print(currDF)
            # if there is information for the tier, process it
            if currDF is not None:

                if currTierName == "ORT:" and self.__topLevelTier != "ORT:":
                    eafObj.add_tier(self.__tierNamePrefix + currTierName[:-1],
                                    ling=ling,
                                    parent=self.__topLevelTier)

                elif currTierName == "ORT:" and self.__topLevelTier == "ORT:":
                    eafObj.add_tier(self.__tierNamePrefix + currTierName[:-1], ling=ling)  # no parent

                elif currTierName != "ORT:":
                    eafObj.add_tier(self.__tierNamePrefix + currTierName[:-1],
                                    ling=ling,
                                    parent=self.__tierNamePrefix + "ORT")  # add it without last char (manually deleted)

                if currTierName == "ORT:" or currTierName == "KAN:":
                    for index, currRow in currDF.iterrows():
                        # print(currRow)
                        wordIndex:int = int(currRow[1])
                        wordToken:str = currRow[2]

                        (startTime, endTime) = self.__getTimingInformationFromMAUTier(wordIndex)

                        # calculate ms from samples
                        startTime = self.__convertSamplesToMS(startTime)
                        endTime = self.__convertSamplesToMS(endTime)

                        eafObj.add_annotation(self.__tierNamePrefix + currTierName[:-1], startTime, endTime, wordToken)

                # MAU Tier and TRN tier are equal (only difference is that the 4th column can contain a single index
                # (MAU) or multiple indices (TRN). This, however, does not influence the check for -1.
                elif currTierName == "MAU:" or currTierName == "TRN:":
                    for index, currRow in currDF.iterrows():
                        wordIndex:int = currRow[3]

                        # if wordIndex is not -1 (which denotes a pause) process it
                        if wordIndex != -1:
                            wordToken:str = currRow[4]
                            # replace all ; (that have been introduced in the constructor) with blanks
                            wordToken = wordToken.replace(";", " ")

                            # extract start and duration from bpf content and convert to integer
                            startTime = self.__convertSamplesToMS(int(currRow[1]))
                            duration = self.__convertSamplesToMS(int(currRow[2]))
                            endTime = startTime + duration

                            eafObj.add_annotation(self.__tierNamePrefix + currTierName[:-1],
                                                  startTime,
                                                  endTime,
                                                  wordToken)

        eafObj.to_file(outFilename)

        # make sure the namespace information occurs only once - if file already existed
        if fileAlreadyExisted:
            self.__pympiEAFHack(outFilename)

        xml_validation.validateXML(outFilename, ELAN_XML_SCHEMA)

    #
    # Function that calculates the milliseconds from samples using the internal sample rate
    #
    def __convertSamplesToMS(self, timeInSamples: int):
        return int(round(timeInSamples / self.__sampleRate * 1000))
