'''
As dependências usadas na maior parte do projeto estão nesse arquivo
'''
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from skimage import io, draw
from dash_table import DataTable
import dash_canvas
from dash_canvas.utils import (parse_jsonstring,
                              superpixel_color_segmentation,
                              image_with_contour, image_string_to_PILImage,
                              array_to_data_url)
from dash_canvas.components import image_upload_zone
import dash_table
import dash_daq as daq
import plotly.graph_objs as go
import visdcc
from dash.dependencies import Input, Output, State
import cv2 as cv
from PIL import Image, ImageDraw
import json
from dash.exceptions import PreventUpdate
