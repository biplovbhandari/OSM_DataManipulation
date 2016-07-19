import wx
import os
import sys
from gdal2tiles import *

class GenerateTiles:
     def __init__(self, source_file, save_file):
          self.source_file_path = source_file
          self.save_file_path = save_file
          self.argv = []
          self.argv.append('--profile=mercator')
          self.argv.append('-z 1-18')
          self.argv.append(self.source_file_path) # source file path
          self.argv.append(self.save_file_path) # save file path

     def tilesGenerator(self):
          gdal2tiles = GDAL2Tiles(self.argv)
          gdal2tiles.process()
