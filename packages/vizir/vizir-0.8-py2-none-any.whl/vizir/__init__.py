import index
import app
import logic
import data 
from .apps import config_viewer
from .apps import datatable
from .apps import plot_viewer 

requirements = [
	dash==0.39
	dash_html_components==0.14
	dash_core_components==0.44
	dash_table==3.6
	dash_daq==0.1
	pymongo==3.7
	pandas==0.23
]
