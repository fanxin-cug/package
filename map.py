import numpy as np
import matplotlib.pyplot as plt

# 计算e
a = 6378140
b = 6356755
e = np.sqrt((np.square(a) - np.square(b)) / np.square(a))
#计算r和U
def get_r(Phi):
    Phi_=np.radians(Phi)
    r=a*np.cos(Phi_)/np.sqrt(1-np.square(e)*np.square(np.sin(Phi_)))
    return r
def get_U(Phi):
    Phi_=np.radians(Phi)
    Psi=np.arcsin(e*np.sin(Phi_))
    Psi_=np.degrees(Psi)
    U=np.tan(np.radians(45+Phi/2))/np.power(np.tan(np.radians(45+Psi_/2)),e)
    return U
#计算r1与r2,U1与U2 Alpha k1,k2和k
Phi1=24
Phi2=48
r1=get_r(Phi1)
r2=get_r(Phi2)
U1=get_U(Phi1)
U2=get_U(Phi2)
Alpha=(np.log10(r2)-np.log10(r1))/(np.log10(U2)-np.log10(U1))
k1=r1*np.power(U1,Alpha)/Alpha
k2=r2*np.power(U2,Alpha)/Alpha
k=(k1+k2)/2

#计算Rho
def get_Rho(Phi):
    Rho=k/np.power(get_U(Phi),Alpha)
    return Rho

#读取经纬度 计算投影区域最低纬线的纬度
path="/home/fanxin/1.txt"
file=open(path,'r')
latitudeList=list()
longitudeList=list()
for line in file.readlines():
    col=line.split(" ")
    latitudeList.append(col[-1])
    longitudeList.append(col[0])
latitudeList_=list()
longitudeList_=list()
for i in range(len(latitudeList)):
    #去掉纬度\n
    temp=latitudeList[i].strip()
    latitudeList_.append(float(temp))
    longitudeList_.append(float(longitudeList[i]))
min_latitude=min(latitudeList_)

Rho_s=get_Rho(min_latitude)

#根据经纬度计算大地坐标
def axesTransfer(Lambda,Phi):
    Lambda_=np.radians(Lambda)
    #计算Sigma
    Sigma=Alpha*Lambda_
    x=Rho_s-get_Rho(Phi)*np.cos(Sigma)
    y=get_Rho(Phi)*np.sin(Sigma)
    return x,y

X_list=list()
Y_list=list()
for i in range(len(longitudeList_)):
    tmp=axesTransfer(longitudeList_[i],latitudeList_[i])
    X_list.append(tmp[0])
    Y_list.append(tmp[1])

#绘制图像
plt.plot(X_list,Y_list)
plt.show()
