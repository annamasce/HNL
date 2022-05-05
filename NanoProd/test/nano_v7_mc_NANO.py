# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: nano_v7_mc_cff -s NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --no_exec --conditions 102X_upgrade2018_realistic_v21 --era Run2_2018,run2_nanoAOD_102Xv1
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

# process = cms.Process('NANO',eras.Run2_2018,eras.run2_nanoAOD_106Xv1)
process = cms.Process('NANO',eras.Run2_2018,eras.run2_nanoAOD_102Xv1)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('HNL.NanoProd.DiMuon_cff')

process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring('file:/eos/user/s/steggema/HNL/samples/M3mu.root'),
    # fileNames = cms.untracked.vstring('file:/eos/user/a/amascell/007FEA64-717A-6C48-8A96-66D8777F9F96.root'),
    # fileNames = cms.untracked.vstring('/store/mc/RunIISummer20UL18MiniAODv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/04A0B676-D63A-6D41-B47F-F4CF8CBE7DB8.root'),
    fileNames = cms.untracked.vstring('file:/eos/user/a/amascell/Samples/026955F4-14DD-504B-8740-4DD45AF2E998.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('nano_v7_mc_cff nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('nano_v7_mc_cff_NANO.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
# GlobalTagName = '106X_upgrade2018_realistic_v15_L1v1'
GlobalTagName = '102X_upgrade2018_realistic_v21'
process.GlobalTag = GlobalTag(process.GlobalTag, GlobalTagName, '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# customisation of the process.
from HNL.NanoProd.DiMuon_cff import nanoAOD_customizeDisplacedDiMuon
nanoAOD_customizeDisplacedDiMuon(process, is_mc=True)

from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 
process = nanoAOD_customizeMC(process)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_diDSAMuon_step, process.nanoAOD_patDSAMuon_step, process.nanoAOD_diMuon_step, process.endjob_step, process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# End of customisation functions

process.NANOAODSIMoutput.outputCommands = cms.untracked.vstring(
    'drop *', 
    'keep nanoaodFlatTable_*Table_*_*', 
    'drop nanoaodFlatTable_fatJet*Table_*_*',
    'drop nanoaodFlatTable_subJet*Table_*_*',
    'drop nanoaodFlatTable_subjet*Table_*_*',
    'drop nanoaodFlatTable_softActivity*Table_*_*',
    'drop nanoaodFlatTable_farPhotonTable_*_*',
    'drop nanoaodFlatTable_HTXSCategoryTable_*_*',
    'drop nanoaodFlatTable_corrT1METJetTable_*_*',
    'drop nanoaodFlatTable_sa*Table_*_*',
    'drop nanoaodFlatTable_svCandidateTable_*_*',
    'drop nanoaodFlatTable_rivet*Table_*_*',
    # it does not seem possible to skim the trigger information saved with existing tools
    'keep edmTriggerResults_*_*_*',  
    'keep String_*_genModel_*', 
    'keep nanoaodMergeableCounterTable_*Table_*_*', 
    'keep *MergeableCounterTable_*_*_*', 
    'keep nanoaodUniqueString_nanoMetadata_*_*'
)

process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(
    SelectEvents=cms.vstring(
        'nanoAOD_diDSAMuon_step',
        'nanoAOD_patDSAMuon_step',
        'nanoAOD_diMuon_step',
    )
)
         

# Customisation from command line
process.MessageLogger.cerr.FwkReport.reportEvery=cms.untracked.int32(20)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
