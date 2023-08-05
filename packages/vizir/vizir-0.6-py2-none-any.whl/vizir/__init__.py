import index
import app
import logic
import data 
from .apps import config_viewer
from .apps import datatable
from .apps import plot_viewer 

requirements = [
	dash==0.39.0
	dash-html-components==0.14.0
	dash-core-components==0.44.0
	dash-table==3.6.0
	dash-daq==0.1.0
	pymongo==3.7.2
	pandas==0.23.0
]
