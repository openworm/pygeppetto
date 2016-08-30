from IPython.display import display
import GeppettoLibrary as G
import GeppettoNeuron

def showSampleModelsPanel():
    loadVerySimpleCellButton = G.addButton('Very simple cell', ['from verysimple_cell import *'])    
    loadSimpleCellButton = G.addButton('Simple cell', ['from simple_cell import *'])    
    loadSimpleNetworkButton = G.addButton('Simple network', ['from simple_network import *'])    

    loadModelPanel = G.addPanel('Load Models', items = [loadVerySimpleCellButton, loadSimpleCellButton, loadSimpleNetworkButton])
    
    display(loadModelPanel)    
    
def showAnalysisPanel():
    analysisButton = G.addButton('Analysis!', ['analysis()'])    

    analysisPanel = G.addPanel('Analysis', items = [analysisButton])
    
    display(analysisPanel)    
    

    