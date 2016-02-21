import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../../../src'))
from imp import reload; import sphinxcontrib; reload(sphinxcontrib)
master_doc = 'index'
extensions = ['sphinxcontrib.ros', 'sphinx.ext.intersphinx']
ros_base_path = ['/opt/ros/indigo/share']
#intersphinx_mapping = {'ros': ('file:///home/tamaki/work/sphinxros/doc/indigo/_build/html', None)}
# https://otamachan.github.io/sphinxros
import sphinx_rtd_theme
#html_theme = 'sphinx_rtd_theme'
#html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
