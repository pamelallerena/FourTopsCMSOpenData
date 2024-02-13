# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: --python_filename doublemuon_cfg.py --eventcontent NANOAOD --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --fileout file:/home/hep/ekauffma/test/testaod1.root --conditions 106X_dataRun2_v36 --step NANO --filein file:root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/00006301-CAA8-E511-AD39-549F35AD8BC9.root, filein file:root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/0034202D-A3A8-E511-BA9C-00259073E3DA.root --era Run2_25ns,run2_nanoAOD_106X2015 --no_exec --data -n -1

# edited by ekauffma to allow for multiple file input via text file argument

import sys, os

import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_25ns_cff import Run2_25ns
from Configuration.Eras.Modifier_run2_nanoAOD_106X2015_cff import run2_nanoAOD_106X2015
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

#---- sys.argv takes the parameters given as input cmsRun PhysObjectExtractor/python/poet_cfg.py <isData (default=False)>
#----  e.g: cmsRun PhysObjectExtractor/python/poet_cfg.py True
#---- NB the first two parameters are always "cmsRun" and the config file name
#---- Work with data (if False, assumed MC simulations)
#---- This needs to be in agreement with the input files/datasets below.
if len(sys.argv) > 2:
    isData = eval(sys.argv[2])
else:
    isData = False

process = cms.Process('NANO',Run2_25ns,run2_nanoAOD_106X2015)

### import of standard configurations ###
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.MessageLogger.cerr.threshold = "WARNING"
process.MessageLogger.categories.append("POET")
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit=cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

process.load('Configuration.EventContent.EventContent_cff')
 
if not isData:
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')

if isData:
    process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
else:
    process.load('Configuration.StandardSequences.MagneticField_cff')

process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# file to process is provided as argument
#input_file = '../../' + sys.argv[-1] + '.txt'
#with open(input_file) as file:
#    lines = [line.rstrip() for line in file]#
#lines = tuple(lines[:2]) # only process two files instead of fifty; use for testing purposes

# Input source
#process.source = cms.Source("PoolSource",
 #   fileNames = cms.untracked.vstring(*lines),
  #  secondaryFileNames = cms.untracked.vstring()
#)

#---- Define the test source files to be read using the xrootd protocol (root://), or local files (file:)
#---- Several files can be comma-separated
#---- A local file, for testing, can be downloaded using, e.g., the cern open data client (https://cernopendata-client.readthedocs.io/en/latest/):
#---- python cernopendata-client download-files --recid 6004 --filter-range 1-1
#---- For running over larger number of files, comment out this section and use/uncomment the FileUtils infrastructure below
#if isData: 
#    sourceFile="root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/00006301-CAA8-E511-AD39-549F35AD8BC9.root"
#else: 
#    sourceFile="root://eospublic.cern.ch//eos/opendata/cms/mc/RunIIFall15MiniAODv2/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/0EB5E88C-FE0D-E611-915D-003048FFD76C.root"
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring(
#        #'file:/playground/1EC938EF-ABEC-E211-94E0-90E6BA442F24.root'
#        sourceFile
#    )
#)

#---- Alternatively, to run on larger scale, one could use index files as obtained from the Cern Open Data Portal
#---- and pass them into the PoolSource.  The example is for 2012 data
files = FileUtils.loadListFromFile("data/CMS_Run2015D_SingleMuon_MINIAOD_16Dec2015-v1_10000_file_index.txt")
files.extend(FileUtils.loadListFromFile("data/CMS_Run2015D_SingleMuon_MINIAOD_16Dec2015-v1_10001_file_index.txt"))
files.extend(FileUtils.loadListFromFile("data/CMS_Run2015D_SingleMuon_MINIAOD_16Dec2015-v1_20000_file_index.txt"))
files.extend(FileUtils.loadListFromFile("data/CMS_Run2015D_SingleMuon_MINIAOD_16Dec2015-v1_60000_file_index.txt"))
process.source = cms.Source(
    "PoolSource", fileNames=cms.untracked.vstring(*files))


#---- Apply the data quality JSON file filter. This example is for 2015 data                                                                                                             
#---- It needs to be done after the process.source definition                                                                                                                                #---- Make sure the location of the file agrees with your setup                                                                                                                           
if isData:
    goodJSON = "data/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt"
    myLumis = LumiList.LumiList(filename=goodJSON).getCMSSWString().split(",")
    process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
    process.source.lumisToProcess.extend(myLumis)


process.options = cms.untracked.PSet(

)

### Production Info ###
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

### Output definition ###

if isData:
    process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
                                             compressionAlgorithm = cms.untracked.string('LZMA'),
                                             compressionLevel = cms.untracked.int32(9),
                                             dataset = cms.untracked.PSet(
                                                 dataTier = cms.untracked.string('NANOAOD'),
                                                 filterName = cms.untracked.string('')
                                             ),
                                             fileName = cms.untracked.string('out.root'),
                                             outputCommands = process.NANOAODEventContent.outputCommands
    )

else:
   process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
                                               compressionAlgorithm = cms.untracked.string('LZMA'),
                                               compressionLevel = cms.untracked.int32(9),
                                               dataset = cms.untracked.PSet(
                                                   dataTier = cms.untracked.string('NANOAODSIM'),
                                                   filterName = cms.untracked.string('')
                                               ),
                                               fileName = cms.untracked.string('out.root'),
                                               outputCommands = process.NANOAODSIMEventContent.outputCommands
   )


### Additional output definition ###

## Other statements ##
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
if isData:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v36', '')
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, '102X_mcRun2_asymptotic_v8', '')

## Path and EndPath definitions ##
if isData:
    process.nanoAOD_step = cms.Path(process.nanoSequence)
else:
    process.nanoAOD_step = cms.Path(process.nanoSequenceMC)

process.endjob_step = cms.EndPath(process.endOfProcess)

if isData:
    process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)
else:
    process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

## Schedule definition ##
if isData:
    process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODoutput_step)
else:
    process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

## Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff ##
if isData:
    from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeData
else:
    from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC

## call to customisation function nanoAOD_customizeData imported from PhysicsTools.NanoAOD.nano_cff
if isData:
    process = nanoAOD_customizeData(process)
else:
    process = nanoAOD_customizeMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion


