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
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn import metrics 
##funcion que carga el dataset
def carga_csv(file_name):
    valores=read_csv(file_name,header=None).values
    return valores
#tranforma un valor del array en popular 1, o no popular.
##se eligió el valor de 30 para determinar cuando es popular o no
# con esta función pasamos de 100 clases a dos clases, de forma que
# pasamos a un problema de clasificación binaria.
def popular(Y):
    N=np.arange(0,len(Y))
    ret = np.zeros((Y.shape))
    for i in N:
        if( Y[i]>30.0):
            ret[i]=1
        else:
            ret[i]=0
    return ret



data=carga_csv('spotify_model.csv')


#seleccionnamos todas las columnas menos la primera
X=data[:,[1,2,3,4]] 
#borramos la fila correspodondiente al nombre de las columnas
X=np.delete(X,0,0)
X=X.astype(float)

Y=data[:,0] 

m=np.shape(X)[0]#num filas
#borramos la fila correspodondiente al nombre de las columnas
Y=np.delete(Y,0,0)
#añadimos columna de unos a la matriz
X=np.hstack([np.ones([m,1]),X])
Y=Y.astype(float)

##seleccionamos datos de entrenamito
X_train=X[20000:30000,:]
Y_train=Y[20000:30000]

#seleccionamos conjunto de test
X_test=X[40000:45000,:]
Y_test=Y[40000:45000]

#tranformamos la variable a predecir a un valor binario
Y_train_fit=popular(Y_train)
#entrenamos la red neuronal
clf = MLPClassifier(activation='logistic',solver='sgd',random_state=1, max_iter=300).fit(X_train, Y_train_fit)

Y_test_fit=popular(Y_test)
#predecimos los valores para el cunjunto de test
pre=clf.predict(X_test)
#escribimos el % de acierto sobre el conjunto de test
print(metrics.accuracy_score(Y_test_fit,pre))
##el acierto es de aprox 99.7 
#otra forma de obtener el porcentaje de acierto
num_correct=sum( Y_test==pre for  Y_test, pre in zip(Y_test_fit,pre)   )

porce=  (num_correct/ len(Y_test)  )*100
print(porce)

