import re
import os

def cleanTab(file1, file2):
	with open(file1, 'r') as inp, open(file2, 'w') as out:
		data = inp.read()
		
		# get only tab
		pattern = re.compile(r'\be.+\|\n|\bB.+\|\n|\bG.+\|\n|\bD.+\|\n|\bA.+\|\n|\bE.+\|\n|\bE.+\|')
		matches = pattern.finditer(data)
		
		justTab = ''
		for match in matches:
			justTab += match.group()
		
		# now clean up tab
		cleanTab = re.sub(r'[^eBGDAE\-\|0123456789\n]','-',justTab)
		
		# check to see if the first char is E or e
		if(cleanTab[0] == 'E'):
			# reset cursor
			inp.seek(0)
			
			# change E to e
			index = 0
			
			# get each line
			tabList = cleanTab.split('\n')
			
			while(index < len(tabList) - 1):
				tabList[index] = 'e' + tabList[index][1:]
				index += 6
				
			cleanTab = ''

			for line in tabList:
				cleanTab += line + '\n'
				
		# now arrange tab to where we can scroll
		# e
		epattern = re.compile(r'\be.+\|')
		ematches = epattern.finditer(cleanTab);
		
		estrings = ''
		for e in ematches:		
			estrings += e.group()
	
		#B 
		Bpattern = re.compile(r'\bB.+\|')
		Bmatches = Bpattern.finditer(cleanTab);
		
		Bstrings = ''
		for B in Bmatches:
			Bstrings += B.group()

		
		#G
		Gpattern = re.compile(r'\bG.+\|')
		Gmatches = Gpattern.finditer(cleanTab);
		
		Gstrings = ''
		for G in Gmatches:
			Gstrings += G.group()

		
		#D
		Dpattern = re.compile(r'\bD.+\|')
		Dmatches = Dpattern.finditer(cleanTab);
		
		Dstrings = ''
		for D in Dmatches:
			Dstrings += D.group()
		
		#A
		Apattern = re.compile(r'\bA.+\|')
		Amatches = Apattern.finditer(cleanTab);
		
		Astrings = ''
		for A in Amatches:
			Astrings += A.group()
		#E
		Epattern = re.compile(r'\bE.+\|')
		Ematches = Epattern.finditer(cleanTab);
		
		Estrings = ''
		for E in Ematches:
			Estrings += E.group()
		
		# don't accept tabs that are too long
		if(len(estrings) > 1800):
			out.close()
			os.remove(file2)
			return False
			
		#make final tab
		finaltab = ''
		
		finaltab += estrings + '\n'
		finaltab += Bstrings + '\n'
		finaltab += Gstrings + '\n'
		finaltab += Dstrings + '\n'
		finaltab += Astrings + '\n'
		finaltab += Estrings
			
		out.write(finaltab)
		
		return True