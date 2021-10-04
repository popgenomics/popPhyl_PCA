#!/usr/bin/python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from Bio.SeqIO import parse
import sys
import os

timeStamp = sys.argv[1]
infileFastaName = sys.argv[2]
infile = parse(infileFastaName, 'fasta')

if os.path.isdir(timeStamp)==False:
	os.system('mkdir {0}'.format(timeStamp))

aln = {}
list_ind = []
liste_species = {}

# read informations from the fasta
for i in infile:
	locus = i.id.split('|')[0]
	species = i.id.split('|')[1]
	individual = i.id.split('|')[2]
	if individual not in list_ind:
		list_ind.append(individual)
		liste_species[individual] = species
	if locus not in aln:
		aln[locus] = {}
	if individual not in aln[locus]:
		aln[locus][individual] = []
	aln[locus][individual].append(i.seq)

# keep loci where all individuals were sequenced
retained_loci = []
for locus in aln:
	if len(aln[locus]) == len(list_ind):
		retained_loci.append(locus)

# dictionnary recording the individual genotypes
genotypes = {}
for i in list_ind:
	genotypes[i] = []

# looping over sequences to get the genotypes
for locus in retained_loci:
	L = len(aln[locus][list_ind[0]][0]) # number of positions
	for pos in range(L):
		site = {}
		nuc = []
		for individual in list_ind:
			allele0 = aln[locus][individual][0][pos]
			allele1 = aln[locus][individual][1][pos]
			site[individual] = [allele0, allele1]
			
			nuc.append(aln[locus][individual][0][pos])
			nuc.append(aln[locus][individual][1][pos])
		
			liste_nuc = list(dict.fromkeys(nuc))
			
		if len(liste_nuc) == 2:
			if 'N' not in liste_nuc:
				alleleValue = {liste_nuc[0]:0, liste_nuc[1]:1}
				for individual in list_ind:
					tmp = alleleValue[site[individual][0]] + alleleValue[site[individual][1]]
					genotypes[individual].append(tmp)


res = 'individual\tspecies\t{0}\n'.format( '\t'.join([ 'SNP_{0}'.format(i) for i in range(len(genotypes[list_ind[0]])) ]))
for individual in list_ind:
	res += '{0}\t{1}\t{2}\n'.format(individual, liste_species[individual], '\t'.join([ str(i) for i in genotypes[individual] ]))

output = open('{0}/output_PCA.txt'.format(timeStamp), 'w')
output.write(res)
output.close()

#### PCA

#df = pd.read_table('output_PCA.txt') # CRoux 30 09 2021
df = pd.read_table('{0}/output_PCA.txt'.format(timeStamp))

features = [ i for i in df.columns if 'SNP_' in i ]
x = df.loc[:, features].values
individual = df.loc[:,['individual']].values
species = df.loc[:,['species']].values

x = StandardScaler().fit_transform(x)

pca = PCA(n_components=3)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2', 'principal component 3'])

finalDf = pd.concat([principalDf, df[['species']], df[['individual']]], axis = 1)

# coordinates PCA
res = 'species\tindividual\tPC1\tPC2\tPC3\n'
for i in range(len(finalDf['species'])):
	res += '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(finalDf['species'][i], finalDf['individual'][i], finalDf['principal component 1'][i], finalDf['principal component 2'][i], finalDf['principal component 3'][i])

output = open('{0}/table_coord_PCA_genotypes.txt'.format(timeStamp), 'w')
output.write(res)
output.close()

# Explained variance
res = 'PC1\tPC2\tPC3\n' + '\t'.join( [ str(round(i*100, 2)) for i in pca.explained_variance_ratio_ ]) + '\n' 
output = open('{0}/table_eigen_PCA_genotypes.txt'.format(timeStamp), 'w')
output.write(res)
output.close()

