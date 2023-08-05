import index
import app
import logic
import data 
from .apps import config_viewer
from .apps import datatable
from .apps import plot_viewer 

requirements = [
	dash==0.39
	dash-html-components==0.14
	dash-core-components==0.44
	dash-table==3.6
	dash-daq==0.1
	pymongo==3.7
	pandas==0.23
]
