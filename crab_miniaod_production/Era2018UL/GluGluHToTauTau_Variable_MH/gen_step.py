import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')
options.register('jobNum', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"jobNum")
options.register('jobEvents', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"jobEvents")
options.register('nEvents', 0, VarParsing.multiplicity.singleton,VarParsing.varType.int,"nEvents")
options.register('nThreads', 1, VarParsing.multiplicity.singleton,VarParsing.varType.int,"nThreads")
options.register('outputName', "genStep.root", VarParsing.multiplicity.singleton,VarParsing.varType.string,"outputName")
options.register('higgsPtMin', 30., VarParsing.multiplicity.singleton,VarParsing.varType.float,"higgsPtMin")
options.register('higgsPtMax', 250., VarParsing.multiplicity.singleton,VarParsing.varType.float,"higgsPtMax")
options.register('higgsMassMin', 20., VarParsing.multiplicity.singleton,VarParsing.varType.float,"higgsMassMin")
options.register('higgsMassMax', 200., VarParsing.multiplicity.singleton,VarParsing.varType.float,"higgsMassMax")
options.register('higgsMassStepSize', 1, VarParsing.multiplicity.singleton,VarParsing.varType.int,"higgsMassStepSize")
options.register('generationStep', 1, VarParsing.multiplicity.singleton,VarParsing.varType.int,"generationStep")
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
import os,random
random.seed = os.urandom(1000)
mass_rnd = random.randint(options.higgsMassMin,options.higgsMassMax);
mass = mass_rnd - (mass_rnd%options.higgsMassStepSize) 
process.RandomNumberGeneratorService.generator.initialSeed = random.randint(0,999999)
if options.higgsPtMin >= 0 and options.higgsPtMax > 0:
        print("Generate in pt range [",options.higgsPtMin,",",options.higgsPtMax,"]  a Higgs with mass ",mass)
else:
        print("Generate a Higgs with mass ",mass)

## ggH+jets simulation at LO in pythia with pt distribution sampled via ptHat. Decaying exclusively to tautau
process.generator = cms.EDFilter("Pythia8GeneratorFilter",
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(1),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    PythiaParameters = cms.PSet( 
                pythia8CommonSettingsBlock,
                pythia8CP5SettingsBlock,
                pythia8PSweightsSettingsBlock,
                processParameters = cms.vstring(
                        'HiggsSM:gg2Hg(l:t) = on',
                        'HiggsSM:qg2Hq(l:t) = on',
                        'HiggsSM:qqbar2Hg(l:t) = on',                        
                        '25:m0 = '+str(mass),
                        '25:mWidth = 0.00374',
                        '25:mMin = '+str(options.higgsMassMin),
                        '25:mMax = '+str(options.higgsMassMax),
                        '25:onMode = off',
                        '25:onIfMatch = 15 -15'
                ),
                parameterSets = cms.vstring(
                        'pythia8CommonSettings',
                        'pythia8CP5Settings',
                        'pythia8PSweightsSettings',
                        'processParameters'
                )
    )
)

if options.higgsPtMin >= 0 and options.higgsPtMax > 0:
        process.generator.PythiaParameters.processParameters.append('PhaseSpace:pTHatMin = '+str(options.higgsPtMin));
        process.generator.PythiaParameters.processParameters.append('PhaseSpace:pTHatMax = '+str(options.higgsPtMax));

        ## gen particle selection --> require gen higgs to be in a certain range
        process.genParticles = cms.EDProducer("GenParticleProducer",
                                        abortOnUnknownPDGCode = cms.untracked.bool(False),
                                        saveBarCodes = cms.untracked.bool(True),
                                        src = cms.InputTag("generatorSmeared")
        )

        process.genParticlePtFilter = cms.EDFilter("CandViewSelector",
                                src = cms.InputTag("genParticles"),
                                cut = cms.string("(pdgId==25) && (pt>%f) && (pt<%f) && (status==62)"%(options.higgsPtMin,options.higgsPtMax))
        )

        process.nGenParticlePassingFilter = cms.EDFilter("CandViewCountFilter",
                                src = cms.InputTag("genParticlePtFilter"),
                                minNumber = cms.uint32(1)
        )
        process.ProductionFilterSequence = cms.Sequence(process.generator+cms.SequencePlaceholder("pgen")+process.genParticles+process.genParticlePtFilter+process.nGenParticlePassingFilter);

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
        if options.higgsPtMin >= 0 and options.higgsPtMax > 0:
                getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq

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
