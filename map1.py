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
path="/home/fanxin/2.txt"
file=open(path,'r')
lines=file.readlines()
latitudeList=list()
longitudeList=list()
regionNum=list()
num=8
for line in lines[8:]:
    if "Region" in line:
        a=lines[num+1]
        b=a.strip()
        regionNum.append(int(b))
    if "Pline" in line:
        col=line.split(" ")
        a=col[1]
        b=a.strip()
        regionNum.append(int(b))
    if '.' in line:
        col=line.split(" ")
        if len(col)==2:
            latitudeList.append(col[1])
            longitudeList.append(col[0])
    num+=1
latitudeList_=list()
longitudeList_=list()
for i in range(len(latitudeList)):
    #去掉纬度\n
    temp=latitudeList[i].strip()
    latitudeList_.append(float(temp))
    longitudeList_.append(float(longitudeList[i]))
min_latitude=list()
ans=0
for i in range(len(regionNum)):
    min_latitude.append(min(latitudeList_[ans:ans+regionNum[i]]))
    ans += regionNum[i]
Rho_s=list()
for i in range(len(min_latitude)):
    Rho_s.append(get_Rho(min_latitude[i]))

def axesTransfer(Lambda,Phi,R_s):
    Lambda_=np.radians(Lambda)
    #计算Sigma
    Sigma=Alpha*Lambda_
    x=R_s-get_Rho(Phi)*np.cos(Sigma)
    y=get_Rho(Phi)*np.sin(Sigma)
    return x,y

X_list=list()
Y_list=list()
res=0
for i in range(len(regionNum)):
    for j in range(regionNum[i]):
        tmp=axesTransfer(longitudeList_[res+j],latitudeList_[res+j],Rho_s[i])
        X_list.append(-tmp[0])
        Y_list.append(tmp[1])
    res+=regionNum[i]

plt.scatter(X_list,Y_list,s=1)
plt.show()
