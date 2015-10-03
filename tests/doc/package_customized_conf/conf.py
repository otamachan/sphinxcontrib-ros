import os, sys
from docutils import nodes
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../../../src'))
import sphinxcontrib; reload(sphinxcontrib)
master_doc = 'index'
extensions = ['sphinxcontrib.ros']

ros_base_path = [os.path.abspath(os.path.dirname(__file__) + '/../../packages/default_base')]
ros_package_attrs_formatter = {'version': 'bold_formatter'}

def bold_formatter(version):
    return ['**' + version + '**']

def setup(app):
    sphinxcontrib.ros.add_formatter('bold_formatter', bold_formatter)
