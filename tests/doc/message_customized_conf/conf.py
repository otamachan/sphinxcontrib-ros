import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../../../src'))
import sphinxcontrib; reload(sphinxcontrib)
master_doc = 'index'
extensions = ['sphinxcontrib.ros']
