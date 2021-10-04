# popPhyl_PCA  
Performs PCA of genotypes.  
Works in two steps.  
  
## 1. PCA  
Single python command line (**popphyl2PCA.py**).  
Before, you need to have these **python** dependencies available:  
1. pandas
2. sklearn
3. biopython

`python3 ~/Programmes/popPhyl_PCA/popphyl2PCA.py [name of the subdirectory created by the script where output files will be written] [name of the input fasta file]`  
  
**Example:**  
`python3 ~/Programmes/popPhyl_PCA/popphyl2PCA.py ~/Documents/PCA/testPCA ~/Programmes/popPhyl_PCA/test.fas`  
 Can takes between 10 minutes and 2 hours, depending on the number of SNPs and individuals.     
   
## 2. vizualisation  
Little Shiny interface (**plotPCA.R**).  
Before, you need to have these **R** dependencies available:  
1. shiny
2. plotly
3. tidyverse
4. shinycssloaders

Then, in R:
1. source(~/Programmes/popPhyl_PCA/plotPCA.R)
2. shinyApp(ui=ui, server=server)
3. upload the files with coordinates (**table_coord_PCA_genotypes.txt**) and eigen values (**table_eigen_PCA_genotypes.txt**)  

