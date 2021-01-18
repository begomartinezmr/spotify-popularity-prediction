import numpy as np
from pandas.io.parsers import read_csv
import matplotlib.pyplot as plt
#para graficar en 3D
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
#calculas valores optimos
import scipy.optimize as opt
from sklearn.preprocessing import PolynomialFeatures
from scipy.io import loadmat
#pr6
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split


def carga_csv(file_name):
    valores=read_csv(file_name,header=None).values
    return valores


data=carga_csv('spotify_model.csv')

#seleccion de los datos, elegimos todas las columnas menos la primera
X=data[:,[1,2,3,4]] 
X=np.delete(X,0,0)
X=X.astype(float)

Y=data[:,0] #seleccionamos la primera columnas como variable a predecir

m=np.shape(X)[0]#num filas
Y=np.delete(Y,0,0)
X=np.hstack([np.ones([m,1]),X])
Y=Y.astype(int)


##conjunto de entrenamiento
X_train=X[0:10000,:]
Y_train=Y[0:10000]


##conjunto de test
X_test=X[20000:25000,:]
Y_test=Y[20000:25000]

#los valores óptimos fueron 30 en ambos
C_vec=[0.01 ,0.03 ,0.1 ,0.3 ,1, 3 ,10,30]
sigma_vec=[0.01 ,0.03 ,0.1 ,0.3 ,1, 3 ,10,30]



##modelo con kerner gaussiano
svm=SVC(kernel='rbf',C=C_vec[7],gamma=1/(2 * sigma_vec[7]**2))


clf=svm.fit(X_train,Y_train.ravel())

pre=clf.predict(X_test)
num_correct=sum( Y_test==pre for  Y_test, pre in zip(Y_test,pre)   )
porce=  (num_correct/ len(Y_test)  )*100
print(porce)
