#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  parser.py
#  
#  Copyright 2017  <@gmail.com>
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
from readNef import readNefFile
import cPickle as pickle
import numpy as np
letters={'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ASN': 'N', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ALA': 'A', 'HIS': 'H', 'GLY': 'G', 'ILE': 'I', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

ss_3class={'H':'H','G':'H','I':'H','E':'E','B':'E','S':'C','T':'C','C':'C','-':'-','b':'-','R':'-','D':'-','_':'-','A':'-','L':'-'}
import os,torch

class protein_class():
	def __init__(self):
		self.seq=''
		self.resi=[]
		self.ss=''
		self.rci=[]
class residue_class():
	def __init__(self):
		self.resname=None
		self.atom={}
		self.ss=None
		self.rci=None
	
def parse_official(fil='bound_free/bmr16065_bound.nef',bound=False):
	start=False


	oldnum=None
	chainold=None
	prot=protein_class()
	cominciato=False
	cont=0
	out=[]
	diz=readNefFile(fil)
	oldnum=None
	chainold=None
	for l in diz:
		

		
		atom_tag=l['atom_name']
		resname=l['residue_name']
		shift=l['value']
		resinum=l['sequence_code']
		if letters.has_key(resname):
			resitype=letters[resname]
		else:
			resitype='X'
		atom=atom_tag
		if oldnum==None:
			oldnum=resinum
			resi=residue_class()
			resi.resname=resitype
	
		if 	oldnum!=resinum:
			#print prot.seq,resi.resname,prot.seq+resi.resname
			prot.seq+=resi.resname
			prot.resi+=[resi]
			oldnum=resinum
			resi=residue_class()
		#print prot.seq
		resi.atom[atom]=shift
		resi.resname=resitype
		oldnum=resinum
		#print resinum,oldnum
	prot.seq+=resi.resname
	prot.resi+=[resi]	
	return [prot]
def parse_train(fil):
		header=True
		diz={}
		saltato=0
		for protein in os.listdir(fil):
			header=True
			cattivo=False
			if protein=='bmr4207.1orc_1.cosh':
				###bad pdb
				continue
			prot_name=protein.split('.')[0]
			diz[prot_name]=protein_class()
			old_number=None
			aatype_old=None
			for i in open(fil+'/'+protein).readlines():
			
				if 'MODEL 1' == i[:7]:
					header=False
					continue
				if header:
					continue
				if 'ENDMDL' == i[:6]:
					break
				a=i.split()
				if 'Unknown' in a:
					continue
				
				aatype=letters[a[3]] 

					
		
				atom=a[2]
				
				res_number=int(a[5])
				if not ss_3class.has_key(a[9].upper()):
					cattivo=True
					saltato+=1
					break
				ss=ss_3class[a[9].upper()]
				if res_number==old_number and aatype!=aatype_old:
					
					cattivo=True
					saltato+=1
					break
				aatype_old=aatype

				if res_number!=old_number:
					diz[prot_name].seq+=aatype
					diz[prot_name].ss+=ss
					diz[prot_name].resi+=[residue_class()]
					diz[prot_name].resi[-1].resname=aatype
					diz[prot_name].resi[-1].ss=ss
					old_number=res_number
				if len(a)>11: ##chem shift data
					val=float(a[11])
					diz[prot_name].resi[-1].atom[atom]=val
					#diz[aatype][entry_name][0][atom]=[val]

			if aatype_old==None: ##pdb vuoto
				saltato+=1
				cattivo=True
			if cattivo:
		
				if diz.has_key(prot_name):
					del diz[prot_name]
			
		print 'total proteins:',len(diz.keys()),'saltate:',saltato		
		return diz

if __name__ == '__main__':
    import sys
    a=parse_official('../input_examples/prova.nef')

