import os
import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')
options.register('jobNum', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"jobNum")
options.register('jobEvents', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"jobEvents")
options.register('nEvents', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"nEvents")
options.register('nThreads', 1, VarParsing.multiplicity.singleton,VarParsing.varType.int,"nThreads")
options.register('outputName', "genStep.root", VarParsing.multiplicity.singleton,VarParsing.varType.string,"outputName")
options.register('generationStep', 1, VarParsing.multiplicity.singleton,VarParsing.varType.int,"generationStep")
options.register('gridpacks', 'gridpacks.list', VarParsing.multiplicity.singleton,VarParsing.varType.string,"gridpacks")
options.parseArguments()


process = cms.Process('GEN',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(options.nEvents)
)

# Input source
process.source = cms.Source("EmptySource",
        firstRun = cms.untracked.uint32(options.jobNum),
        numberEventsInRun = cms.untracked.uint32(options.jobEvents),
        firstLuminosityBlock  = cms.untracked.uint32(options.generationStep),
        numberEventsInLuminosityBlock = cms.untracked.uint32(options.nEvents),
        firstEvent = cms.untracked.uint32((options.generationStep-1)*options.nEvents+1)                            
)

process.options = cms.untracked.PSet()
process.options.numberOfConcurrentLuminosityBlocks =  cms.untracked.uint32(1)
# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('gen_step.py nevts:'+str(options.nEvents)),
    name = cms.untracked.string('\\$Source$'),
    version = cms.untracked.string('\\$Revision$')
)

# Output definition
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(1),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string('file:'+options.outputName),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag,'106X_upgrade2018_realistic_v11_L1v1', '')

from Configuration.Generator.Pythia8CommonSettings_cfi import pythia8CommonSettingsBlock
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import pythia8CP5SettingsBlock
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import pythia8PSweightsSettingsBlock

## generate radom value of the mass in the range set by the job
process.generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

gridpack_list = [];
inputfile = open(options.gridpacks,"r").read().splitlines();
for f in inputfile:
    name = f.split("/")[-1];        
    name = name.replace("\n","");
    name = name.replace("_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz","")
    gridpack_list.append([f,name]);
gridpack_list.sort();

print ("Number of gridpacks = ",len(gridpack_list))
for gridpack in gridpack_list:    
    gridpack[0] = os.getcwd()+"/"+gridpack[0].replace("\n","");
    gridpack[1] = gridpack[1].replace("\n","");
    process.generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(1),
            GridpackPath =  cms.string(gridpack[0]),
            ConfigDescription = cms.string(gridpack[1]),
            PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CP5SettingsBlock,
                pythia8PSweightsSettingsBlock,
                processParameters = cms.vstring(
                    '25:onMode = off',
                    '25:oneChannel = 1 1 100 5 -5',
                    '25:onIfMatch = 5 -5',
                    '35:onMode = off',
                    '35:oneChannel = 1 1 100 15 -15',
                    '35:onIfMatch = 15 -15',
                    'ResonanceDecayFilter:filter = on',
                    'ResonanceDecayFilter:exclusive = on',
                    'ResonanceDecayFilter:mothers = 25,35',
                    'ResonanceDecayFilter:daughters = 5,5,15,15'
                ),
                parameterSets = cms.vstring(
                    'pythia8CommonSettings',
                    'pythia8CP5Settings',
                    'pythia8PSweightsSettings',
                    'processParameters',
                )
            )
        )
   )

import os,random
random.seed = os.urandom(1000)
process.RandomNumberGeneratorService.generator.initialSeed = random.randint(0,999999)

process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

process.options.numberOfThreads = cms.untracked.uint32(options.nThreads)
process.options.numberOfStreams = cms.untracked.uint32(0)
process.options.wantSummary = cms.untracked.bool(True)

# filter all path with the production filter sequence
for path in process.paths:
        if path in ['lhe_step']: continue
        getattr(process,path).insert(0, process.ProductionFilterSequence)

# customisation of the process.

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
