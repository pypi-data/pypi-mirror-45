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
import warnings
warnings.filterwarnings("ignore")
import parser
import torch
import argparse
import os
#from autoenchoder_standalone_version import *
#from load_model import load_model
cw=os.path.dirname(os.path.realpath(__file__))+'/'
#from autoenc_solo4 import autoencoder

def run_shiftcrypt(results):

	#prot=parser.parse_official(fil=results.infile)[0]
	if results.test:
		results.infile=cw+'input_examples/bmr15315_1.nef'
	try:
		prot=parser.parse_official(fil=results.infile)[0]
	except:
		print 'error in the parsing of the file. Please double check the format. If everyhting is correct, please report the bug to @gmail.com'
		return
	
	#from autoenchoder_standalone_version import *
	#main('d')
	#zxc
	#auto=torch.load(cw+'marshalled/new_full.mtorch') # the method with the full set of Cs. this may retur a lot of -10 (missing values) because of the scarcity of cs data for some residues
	
	auto=torch.load(cw+'marshalled/new_commons.mtorch')
	try:
		if results.model=='1':
			auto=torch.load(cw+'marshalled/new_full.mtorch') # the method with the full set of Cs. this may retur a lot of -10 (missing values) because of the scarcity of cs data for some residues
		elif results.model=='2':
			auto=torch.load(cw+'marshalled/new_commons.mtorch') # the method with just the most common Cs values
		elif results.model=='3':
			auto=torch.load(cw+'marshalled/new_NH.mtorch') # the method with only N and H CS. Used for dimers
		else:
			try:
				auto=torch.load(results.model)
			except:
				print "custom model", results.model,'not found'
				return

	except:
		print 'error loading the model. Please double check you installed all the dependencies. If everyhting is correct, please report the bug to @gmail.com'
		return
	


	#out=auto.transform(prot)
	try:
		print 'running transformation'
		out=auto.transform(prot)
	except:
		print 'error transforming the CS data. Please double check you installed all the dependencies. If everyhting is correct, please report the bug to @gmail.com'
		return
	
	if results.outfile!=None:
		f=open(results.outfile,'w')
		for i in range(len(prot.seq)):
			f.write(prot.seq[i]+' '+str(out[i])+'\n')
		f.close()
		#print out
	else:
		for i in range(len(prot.seq)):
			print prot.seq[i]+' '+str(out[i])
	
	if results.test:
		print 'TEST WORKED!'		
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(run_shiftcrypt(sys.argv))
