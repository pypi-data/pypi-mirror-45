#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  load_model.py
#  
#  Copyright 2019 scimmia <scimmia@scimmia-pc>
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
from autoenchoder_standalone_version import *
import torch,os
def load_model(model=2):
	from autoenchoder_standalone_version import *
	cw=os.path.dirname(os.path.realpath(__file__))+'/'
	if model=='1':
		auto=torch.load(cw+'/marshalled/autoencoder.mtorch') # the method with the full set of Cs. this may retur a lot of -10 (missing values) because of the scarcity of cs data for some residues
	elif model=='2':
		auto=torch.load(cw+'/marshalled/autoenchoder_only_common_atoms.mtorch') # the method with just the most common Cs values
	elif model=='3':
		auto=torch.load(cw+'/marshalled/autoenchoder_only_N_H_atoms.mtorch') # the method with only N and H CS. Used for dimers
	else:
		try:
			self.auto=torch.load(model)
		except:
			print "custom model", model,'not found'
			return asd
	return auto

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
