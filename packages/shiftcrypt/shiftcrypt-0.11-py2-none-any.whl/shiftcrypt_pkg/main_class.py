#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shiftcrypt.py
#  
#  Copyright 2018  <@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os
import warnings
warnings.filterwarnings("ignore")
import parser
import torch
import argparse
from autoenchoder_standalone_version import *
cw=os.path.dirname(os.path.realpath(__file__))+'/'
class shiftcript:
	def __init__(self,model=2):
		try:
			
			if model==1:
				self.auto=torch.load(cw+'/marshalled/new_full.mtorch') # the method with the full set of Cs. this may retur a lot of -10 (missing values) because of the scarcity of cs data for some residues
			elif model==2:
				self.auto=torch.load(cw+'/marshalled/new_commons.mtorch') # the method with just the most common Cs values
			elif model==3:
				self.auto=torch.load(cw+'/marshalled/new_NH.mtorch') # the method with only N and H CS. Used for dimers
			else:
				try:
					self.auto=torch.load(model)
				except:
					print "custom model", model,'not found'
					return

		except:
			print 'error loading the model. Please double check you installed all the dependencies. If everyhting is correct, please report the bug to @gmail.com'
			return
	def transform(self,infile): ## take a star2 file and returns the shiftcrypt index as a list. index i corresponds to ith residue. A -10 means there are too many missing values
		## parsing ##
		#prot=parser.parse_official(fil=infile)[0]
		try:
			prot=parser.parse_official(fil=infile)[0]
		except:
			print 'error in the parsing of the file. Please double check the format. If everyhting is correct, please report the bug to @gmail.com'
			return
		## transforming ##
		out=self.auto.transform(prot)
		try:
			out=self.auto.transform(prot)
		except:
			print 'error transforming the CS data. Please double check you installed all the dependencies. If everyhting is correct, please report the bug to @gmail.com'
			return
		return out
	def test(self):
		
		for i in os.listdir(cw+'input_examples/'):
			if i=='__init__.py':
				continue
			print 'testing input example '+i
			#print self.transform(cw+'input_examples/'+i)
		print 'TEST WORKED'
def main(args):
	a=shiftcript()
	a.test()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
