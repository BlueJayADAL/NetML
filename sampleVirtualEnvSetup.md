# Creating Python virtualenv using ```conda``` on Ubuntu (16.04) System (*with optional jupyter notebook install*)
## 1. ```conda config --add channels intel```
## 2. ```conda create -n idp python=3 ipykernel intelpython3_full notebook nb_conda```
## 3. ```conda activate idp``` 
### ^Do this everytime before you run DAAL script^
## 4. ```python -m ipykernel install --user```
### ^Ensures jupyter notebook will use the correct Intel Python when running^
