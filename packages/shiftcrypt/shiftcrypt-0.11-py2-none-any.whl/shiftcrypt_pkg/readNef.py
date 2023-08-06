import re



def readNefFile(fileName,printData=True):

    import File as nmrStar

    origNefFile = nmrStar.File(verbosity = 2, filename = fileName)

    #
    # Read star file
    #

    if origNefFile.read():
      print "  Error reading NEF file " 
      return False

    #
    # Go through the data in the file
    #
    l=[]
    if printData:
      for origSaveFrame in origNefFile.datanodes:
      
        # This is the title of the saveframe
        #print origSaveFrame.title

        for tagtable in origSaveFrame.tagtables:
        
          if tagtable.free:

            # This is for values directly associated with saveframe, only one value per tagname
            
            for tagIndex in range(len(tagtable.tagnames)):

              tagName = tagtable.tagnames[tagIndex]
              tagValue = tagtable.tagvalues[tagIndex][0]  # Only one value, always!
              
              #print tagName, tagValue
          
          else:

            # This is a loop with multiple rows of values for the tags
            # Have to loop over the value index to get rows out
            
            #print("Table with tags {}".format(",".join(tagtable.tagnames)))
            tags=tagtable.tagnames
            t=[]
            for i in tags:
				t+=[i.split('.')[-1]]
            

            tags=t

            
            
            
            
            
            
            
            
			#### convert  ####
		
			
			
			
			
            converting={'_Atom_name':'atom_name','_Chem_shift_value':'value','_Residue_label':'residue_name','_Residue_seq_code':'sequence_code'}
            for i in range(len(tags)):
                 if converting.has_key(tags[i]):
                   
                    tags[i]=converting[tags[i]]
             
            
            if not 'value' in tags or not 'atom_name' in tags:
                   continue
    
            numTagIndexes = len(tagtable.tagnames)
            
            # Using first tag index (0) to get number of data value rows in loop
            for valueIndex in range(len(tagtable.tagvalues[0])): 
              dataRow = {}
              for tagIndex in range(numTagIndexes):
                tagValue = tagtable.tagvalues[tagIndex][valueIndex]
                dataRow[tags[tagIndex]]=tagValue
              l+=[dataRow]
             
             


    return l
    
if __name__ == '__main__':
  
 
  print readNefFile("../input_examples/prova.nef")
