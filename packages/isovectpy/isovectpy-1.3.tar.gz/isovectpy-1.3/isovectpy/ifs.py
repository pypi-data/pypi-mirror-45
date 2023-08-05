#The program generates an array of ifs mass isotope data for\
#denomination algorithm by isoVector.
#Input: NONE. Customers may change element list and threshold. By\
#default element list only includes non-radioactive element, and\
#threshold was set to 1e-15 for abs probability.
#Output: IfsData, which is an array with the following\
#data structure:

#Some abbrevations:
#L means list structure for ifs isotope data
#v means 1-D array(vector)
#s means 2-D array(square)
#c means 3-D array(cube)

#Data structure for ifs computation is as follows:
#L=list[B0,B1,B2,...Bn], n means the total number of centered isotopes
#B0=np.array([[M],[P]]),dim=2*(k+1),k depends on the number of isotoplogues
#M=np.array([m0,m1,m2,...mk]),dim=1*(k+1)
#m0 is center mass, m1,...,mk are isotoplogue mass value for m0
import numpy as np
import matplotlib.pyplot as plt
import time
from functools import reduce
import os
#######################isoFunction############################################
def isoConsec(s):
    #arrange mass vector in consecutive manner WITHOUT sorting
    #input 2-D array should be sorted before using this function
    if s.shape[1]==1:
        return s
    else:
        mv=[s[0,0]]
        pv=[s[1,0]]
        for i in range(1,s.shape[1]):
            if s[0,i]-s[0,i-1]<1.1:
                mv.append(s[0,i])
                pv.append(s[1,i])
            elif s[0,i]-s[0,i-1]>=1.1:
                DeltaRnd=round(s[0,i]-s[0,i-1])
                Delta=round((s[0,i]-s[0,i-1])/DeltaRnd,14)
                for ii in range(1,int(DeltaRnd)):
                    mv.append(s[0,i-1]+ii*Delta)
                    pv.append(0)
                mv.append(s[0,i])
                pv.append(s[1,i])
        return np.array([mv,pv])
    
def isoMulti(s1,s2):
    #Multiplication of two input isotope array(2D)
    #for s, row0=mass value, row1=prob value
    #Output is a cubic array(3D) of multiplied mass and prob
    #Output: layer0=mass array(2D), layer1=prob array(2D)
    pv1=np.array([s1[1,:]])
    pv2=np.array([s2[1,:]])
    prob=np.dot(pv1.T,pv2)
    mv1=np.array([s1[0,:]])
    mv2=np.array([s2[0,:]])
    mass=prob.copy()
    mass[:]=0
    for i in range(mass.shape[0]):
        for j in range(mass.shape[1]):
            mass[i,j]=mv1[0,i]+mv2[0,j]
    return np.array([mass,prob])

def isoShift(c):
    #Shift each row in mass-probability cube (3D) by 1 unit
    #Input: np.array([[mass(2D)],[probability(2D)]])
    #Output: shifted mass-probability cube(3D)
    ms=c[0,...]
    ps=c[1,...]
    msArr=np.zeros(ms.shape[0]*(ms.shape[0]+ms.shape[1]-1)).\
           reshape(ms.shape[0],ms.shape[0]+ms.shape[1]-1)
    psArr=msArr.copy()
    for i in range(int(ms.shape[0])):
        msArr[i,i:ms.shape[1]+i]=ms[i,...]
        psArr[i,i:ms.shape[1]+i]=ps[i,...]
    return np.array([msArr,psArr])

def isoCollapse(c):
    #Input: shifted mass-probability cube
    #Output: mass-probability square(2D), np.array([[mass_vector],[prob_vector]])
    ms=c[0,...]
    ps=c[1,...]
    mv=np.zeros(ms.shape[1]).reshape(ms.shape[1],)
    pv=mv.copy()
    for i in range(ms.shape[1]):
        mv_temp=np.vdot(ms[...,i],ps[...,i])
        pv_temp=np.array([0])
        for j in range(ms.shape[0]):
            pv_temp=pv_temp+ps[j,i]
        pv[i]=pv_temp 
        if pv[i]!=0:
            mv[i]=mv_temp/pv[i]
        elif pv[i]==0:
            mv[i]=mv[i-1]+1
    return np.array([mv,pv])

def isoTrunc(s,thre):
    mv=[]
    pv=[]
    for i in range(s.shape[1]):
        if s[1,i]>=thre:
            mv.append(s[0,i])
            pv.append(s[1,i])
    return np.array([mv,pv])

def isoFormula(Str):
    #This function is used to read input molecular formula and
    #transform the formula into an element name list and a number
    #list.
    #check formula
    if ord(Str[-1])>=65 and ord(Str[-1])<=122:
        print('Error: Please check the input formula')
        return
    IsotopeNameList=['H','Li','Be','B','C','N','O','F','Na','Mg','Al','Si',\
                     'P','S','Cl','K','Ca','Ti','V','Cr','Mn','Fe','Co','Zn',\
                     'Ga','Ge','As','Se','Br','Rb','Sr','Y','Zr','Nb','Mo',\
                     'Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Cs',\
                     'Ba','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl',\
                     'Pb','Bi']
    #divide Str into name list and number list
    NameList=[]
    NumberList=[]
    NameListTemp=''
    NumberListTemp=''
    i=0
    while i<len(Str):
        if ord(Str[i])>=65 and ord(Str[i])<=122:
            for ii in range(i,int(len(Str))):
                if ord(Str[ii])>=65 and ord(Str[ii])<=122:
                    NameListTemp=NameListTemp+Str[ii]
                else:
                    break
            i=ii
            NameList.append(NameListTemp)
            NameListTemp=''
        elif ord(Str[i])>=48 and ord(Str[i])<=57:
            for ii in range(i,int(len(Str))):
                if ord(Str[ii])>=48 and ord(Str[ii])<=57:
                    NumberListTemp=NumberListTemp+Str[ii]
                else:
                    break
            i=ii
            NumberList.append(int(NumberListTemp))
            NumberListTemp=''
            if i==int(len(Str))-1:
                i=i+1               
    #check formula
    for i in range(0,int(len(NameList))):
        if NameList[i] not in IsotopeNameList:
            print('Error: Please check the input formula.')
            return
    #merge name list
    NameListMerge=[NameList[0]]
    NumberListMerge=[NumberList[0]]
    for i in range(1,int(len(NameList))):   
        judge=0
        for j in range(0,int(len(NameListMerge))):
            if NameListMerge[j]==NameList[i]:
                NumberListMerge[j]=NumberListMerge[j]+NumberList[i]
                judge=1
        if judge==0:
            NameListMerge.append(NameList[i])
            NumberListMerge.append(NumberList[i])
    return [NameListMerge,NumberListMerge]

def isoCombine(s1,s2,thre):
    #A combination of isoMulti, isoShift, isoCollapse, and isoTrunc fuction
    #for two input isotope array(2D), and threshold.
    #for s, row0=mass value, row1=prob value
    #Output is a square of new isotope distribution, having the same data\
    #structure as input s1 and s2.
    Ns1=isoConsec(s1)
    Ns2=isoConsec(s2)
    Temp1=isoMulti(s1,s2)
    Temp2=isoShift(Temp1)
    Temp3=isoCollapse(Temp2)
    Temp=isoTrunc(Temp3,thre)
    return Temp

def isoElementFinder():
    #generate a reference number list for element in IsoDataCenterMass
    ElementList=[]
    for i in range(IsoDataCenterMass.shape[0]):
        ElementList.append(IsoDataCenterMass[i][0])
    return ElementList

def isoDecom(Number,Limit):
    #This function decomposes an input Number into a denomination system
    #(1,2,5,10,20,50,...)with a upper Limit.
    DenomiSys=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000]
    LimitIndex=DenomiSys.index(Limit)
    Denom=DenomiSys[0:LimitIndex+1]
    Denom.reverse()
    #decomposition of Number into Denom
    Count=[0]*int(len(Denom))
    while Number>0:
        for i in range(int(len(Denom))):
            if Denom[i]-Number<=0:
                Count[i]=Count[i]+1
                Number=Number-Denom[i]
                break     
    return np.array([Denom,Count])

def isoElement(formula,thre):
    #computing isotope center structure of given element clusters
    #by denomination algorithm
    #Input: element clusters 'Xn',threshold
    #Output: mass-probability square(2D), np.array([[mass_vector],[prob_vector]]
    DenomiSys=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000]
    ElementName=isoFormula(formula)[0][0]
    ElementNumber=isoFormula(formula)[1][0]
    ElementCoord=isoElementFinder().index(ElementName)
    ElementIsotope=IsoDataCenterMass[ElementCoord][2:]
    Limit=IsoDataCenterMass[ElementCoord][1]
    DecomArray=isoDecom(ElementNumber,Limit)
    for i in range(DecomArray.shape[1]):
        if DecomArray[1,i]>=1:
            ElementNumberDenom=DecomArray[0,i]
            DenomRef=DenomiSys.index(ElementNumberDenom)
            EleIsotopeAdder=isoTrunc(ElementIsotope[DenomRef],thre)
            DecomArray[1,i]=DecomArray[1,i]-1
            break
    DecomSum=sum(DecomArray[1,...])
    if DecomSum==0:
        return EleIsotopeAdder
    else:
        while DecomSum>0:
            for i in range(DecomArray.shape[1]):
                if DecomArray[1,i]>=1:
                    ElementNumberDenom=DecomArray[0,i]
                    DenomRef=DenomiSys.index(ElementNumberDenom)
                    EleIsotopeTemp=isoTrunc(ElementIsotope[DenomRef],thre)
                    DecomArray[1,i]=DecomArray[1,i]-1
                    break
            EleIsotopeAdder=isoCombine(EleIsotopeAdder,EleIsotopeTemp,thre)
            DecomSum=sum(DecomArray[1,...])
        return EleIsotopeAdder

def isoMonoMass(formula):
    EleNameList=isoFormula(formula)[0]
    EleNumberList=isoFormula(formula)[1]
    Len=len(EleNameList)
    for i in range(len(IsoDataCenterMass)):
        if IsoDataCenterMass[i][0]==EleNameList[0]:
             pos=i
             break
    m=EleNumberList[0]*IsoDataCenterMass[i][2][0][0]
    if Len==1:
        MonoMass=m
    elif Len>1:
        for j in range(1,len(EleNameList)):
            for i in range(len(IsoDataCenterMass)):
                if IsoDataCenterMass[i][0]==EleNameList[j]:
                    pos=i
                    break
            m=m+EleNumberList[j]*IsoDataCenterMass[pos][2][0][0]
        MonoMass=m
    return MonoMass

def isoWeighAveMass(formula):
    #computing average mass by averaging isotope mass
    EleNameList=isoFormula(formula)[0]
    EleNumberList=isoFormula(formula)[1]
    Len=len(EleNameList)
    for i in range(len(IsoDataCenterMass)):
        if IsoDataCenterMass[i][0]==EleNameList[0]:
             pos=i
             break
    m=np.dot(IsoDataCenterMass[i][2][0],IsoDataCenterMass[i][2][1])\
       *EleNumberList[0]
    if Len==1:
        AveMass=m
    elif Len>1:
        for j in range(1,len(EleNameList)):
            for i in range(len(IsoDataCenterMass)):
                if IsoDataCenterMass[i][0]==EleNameList[j]:
                    pos=i
                    break
            m=m+EleNumberList[j]*np.dot(IsoDataCenterMass[pos][2][0],\
                                        IsoDataCenterMass[pos][2][1])
        AveMass=m
    return AveMass

def iso(formula,thre):
    #computing isotope center structure of given element clusters
    #by denomination algorithm
    t0=time.process_time()
    EleNameList=isoFormula(formula)[0]
    EleNumberList=isoFormula(formula)[1]
    Len=len(EleNameList)
    if Len==1:
        IsotopeCenter=isoElement(formula,thre)
    elif Len>1:
        IsoCenterAdder=isoElement(EleNameList[0]+str(EleNumberList[0]),thre)
        for i in range(1,Len):
            IsoCenterTemp=isoElement(EleNameList[i]+str(EleNumberList[i]),thre)
            IsoCenterAdder=isoCombine(IsoCenterAdder,IsoCenterTemp,thre)
        IsotopeCenter=IsoCenterAdder
    t1=time.process_time()-t0
    aveMass=np.dot(IsotopeCenter[0],IsotopeCenter[1])
    abdMass=isoMax(IsotopeCenter)[0]
    print('----------SUMMARY OF ISO CALCULATION-----------------------')
    print('Molecular formula =',formula)
    print('Intensity threshold =',format(thre,'0.2e'))
    print('Monoisotopic mass =',format(isoMonoMass(formula),'0.4f'),'Da')
    print('The most abundant mass =',format(abdMass,'0.4f'),'Da')
    print('Average mass =',format(aveMass,'0.4f'),'Da')
    print('Weighing average mass =',format(isoWeighAveMass(formula),'0.4f'),'Da')
    print('Mass error with reference to average =',\
          format(abs(aveMass-isoWeighAveMass(formula)),'0.2e'),'Da')
    print('Elapsed time =',format(t1,'0.3f'),'seconds')
    print('\n----------DATA DISPLAY-------------------------------------')
    print('Use isoPlot to view the spectrum')
    print('Use isoNorm to view relative intensity')
    print('Use isoList to print mass and intensity list')
    print('Use ifs to zoom in isotopologues at an interested mass')
    return IsotopeCenter

def isoNorm(s,switch):
    #Display prob in rel-scale or abs-scale
    #Input: square array data, switch=rel or abs
    if switch=='rel':
        prob_max=max(s[1,...])
        prob_rel=100*s[1,...]/prob_max
        s_disp=np.array([s[0,...],prob_rel])
    elif switch=='abs':
        s_disp=s
    return s_disp

def isoPlot(s):
    plt.stem(s[0,...],s[1,...],'k',',',',')
    plt.show()
    return

def isoMax(s):
    pMax=np.max(s[1])
    pos=np.where(s[1]==pMax)
    return [s[0][pos][0],s[1][pos][0]]

def isoList(s):
    m=list(s[0])
    p=list(s[1])
    return [m,p]
#######################the end of isoFunction#################################


#######################ifsFunction############################################
def ifsConsec(A):
    #advanced version of isoConsec for ifs data structure
    #Input: ifs data structure
    #Output data will be applied ifsMulti
    if A.shape[1]==1:
        return A
    else:
        mArr=[]
        m=[]
        mc=A[0][0][0]
        m.append(mc)
        mf=A[0][0][1]
        m.append(mf)
        mArr.append(m)
        pArr=[]
        p=[]
        pc=A[1][0][0]
        p.append(pc)
        pf=A[1][0][1]
        p.append(pf)
        pArr.append(p)
        for i in range(1,A.shape[1]):
            if A[0][i][0]-A[0][i-1][0]<1.1:
                m=[]
                mc=A[0][i][0]
                m.append(mc)
                mf=A[0][i][1]
                m.append(mf)
                mArr.append(m)
                p=[]
                pc=A[1][i][0]
                p.append(pc)
                pf=A[1][i][1]
                p.append(pf)
                pArr.append(p)
            elif A[0][i][0]-A[0][i-1][0]>=1.1:
                DeltaRnd=round(A[0][i][0][0]-A[0][i-1][0][0])
                Delta=round((A[0][i][0][0]-A[0][i-1][0][0])/DeltaRnd,18)
                for ii in range(1,int(DeltaRnd)):
                    mass=A[0][i-1][0][0]+ii*Delta
                    m=[]
                    mc=np.array([mass])
                    m.append(mc)
                    mf=np.array([mass,mass])
                    m.append(mf)
                    mArr.append(m)
                    p=[]
                    pc=np.array([0])
                    p.append(pc)
                    pf=np.array([0,0])
                    p.append(pf)
                    pArr.append(p)
                m=[]
                mc=A[0][i][0]
                m.append(mc)
                mf=A[0][i][1]
                m.append(mf)
                mArr.append(m)
                p=[]
                pc=A[1][i][0]
                p.append(pc)
                pf=A[1][i][1]
                p.append(pf)
                pArr.append(p)
        return np.array([mArr,pArr])
    
def ifsCenterArray(A):
    #This function extract center mass array data from L for\
    #computation of center isotope distribution
    #Output: np.array([[ms],[ps]]),2D data for computation by\
    #any of isoFunction
    mv=[]
    pv=[]
    for i in range(A.shape[1]):
        mv.append(A[0][i][0][0])
        pv.append(A[1][i][0][0])
    return np.array([mv,pv])

def ifsIsotoplogArray(A,pos):
    #This function extract isotoplog mass array data from A for\
    #computation of isotoplog isotope distribution@certain center mass
    #Input: A data, pos indicating position in A
    #Output: np.array([[ms],[ps]]),2D data
    mv=A[0][pos][1]
    pv=A[1][pos][1]
    return np.array([mv,pv])

def ifs_isoMulti(s1,s2):
    #Multiplication of two input isotope array(2D)
    #for s, row0=mass value, row1=prob value
    #Output is a cubic array(3D) of multiplied mass and prob
    #Output: layer0=mass array(2D), layer1=prob array(2D)
    pv1=np.array([s1[1,:]])
    pv2=np.array([s2[1,:]])
    prob=np.dot(pv1.T,pv2)
    mv1=np.array([s1[0,:]])
    mv2=np.array([s2[0,:]])
    mass=prob.copy()
    mass[:]=0
    for i in range(mass.shape[0]):
        for j in range(mass.shape[1]):
            mass[i,j]=mv1[0,i]+mv2[0,j]
    return np.array([mass,prob])

def ifsMultiSub(A1,pos1,A2,pos2):
    #Input: L, pos indicating position in L
    #Output: np.array([[ms],[ps]]),2D data
    s1=ifsIsotoplogArray(A1,pos1)
    s2=ifsIsotoplogArray(A2,pos2)
    c=ifs_isoMulti(s1,s2)
    mv=c[0].flatten()
    pv=c[1].flatten()
    return np.array([mv,pv])

def ifsShift(L):
    #Advanced version of isoShift
    #Input: L=[CM,FM]
    #CM=cube data for center m-p from isoMulti
    #FM=data from ifsMultiSub
    #Output: L' similar to L, but center mass cube shifted
    #and isotoplog list shifted correspondingly.
    ms=L[0][0]
    ps=L[0][1]
    IsotoplogMP=L[1]
    msArr=np.zeros(ms.shape[0]*(ms.shape[0]+ms.shape[1]-1)).\
           reshape(ms.shape[0],ms.shape[0]+ms.shape[1]-1)
    psArr=msArr.copy()
    Isotoplog1D=[[]]*(ms.shape[0]+ms.shape[1]-1)
    Isotoplog=[]
    for i in range(ms.shape[0]):
        msArr[i,i:ms.shape[1]+i]=ms[i]
        psArr[i,i:ms.shape[1]+i]=ps[i]
        Isotoplog1D[i:ms.shape[1]+i]=IsotoplogMP[i]
        Isotoplog.append(Isotoplog1D.copy())
        Isotoplog1D=[[]]*(ms.shape[0]+ms.shape[1]-1)
    return [np.array([msArr,psArr]),Isotoplog]

def ifs_isoCollapse(c):
    #Input: shifted mass-probability cube
    #Output: mass-probability square(2D), np.array([[mass_vector],[prob_vector]])
    ms=c[0,...]
    ps=c[1,...]
    mv=np.zeros(ms.shape[1]).reshape(ms.shape[1],)
    pv=mv.copy()
    for i in range(ms.shape[1]):
        mv_temp=np.vdot(ms[...,i],ps[...,i])
        pv_temp=np.array([0])
        for j in range(ms.shape[0]):
            pv_temp=pv_temp+ps[j,i]
        pv[i]=pv_temp 
        if pv[i]!=0:
            mv[i]=mv_temp/pv[i]
        elif pv[i]==0:
            mv[i]=mv[i-1]+1
    return np.array([mv,pv])

def ifsArr2EleExtract(mpArray):
    mpList=list(mpArray)
    if mpList==[]:
        MassAdder=np.array([])
        ProbAdder=np.array([])
    else:
        MassAdder=mpArray[0]
        ProbAdder=mpArray[1]
    return [MassAdder, ProbAdder]

def ifsCollapse(CenterIsotoplogShift):
    #Input: output data from ifsShift, L=[CM,FM]
    #Output: collapsed data L'=[CM',FM']
    #CM' is a 3D np.array
    #FM' is np.array([Mass,Prob])
    CubeCenter=CenterIsotoplogShift[0]
    CenterCollapse=ifs_isoCollapse(CubeCenter)
    ListIsotoplog=CenterIsotoplogShift[1]
    MassArrayAdder=[]
    ProbArrayAdder=[]
    if CubeCenter.shape[1]>1 and CubeCenter.shape[2]>1:
        for j in range(CubeCenter.shape[2]):
            MassAdder=ifsArr2EleExtract(ListIsotoplog[0][j])[0]
            ProbAdder=ifsArr2EleExtract(ListIsotoplog[0][j])[1]
            for i in range(1,CubeCenter.shape[1]):
                MassTemp=ifsArr2EleExtract(ListIsotoplog[i][j])[0]
                ProbTemp=ifsArr2EleExtract(ListIsotoplog[i][j])[1]
                MassAdder=np.append(MassAdder,MassTemp)
                ProbAdder=np.append(ProbAdder,ProbTemp)
            MassArrayAdder.append(MassAdder.copy())
            ProbArrayAdder.append(ProbAdder.copy())
        IsotoplogCollapse=np.array([MassArrayAdder,ProbArrayAdder])
    elif CubeCenter.shape[1]>1 and CubeCenter.shape[2]==1:
        MassAdder=ifsArr2EleExtract(ListIsotoplog[0][0])[0]
        ProbAdder=ifsArr2EleExtract(ListIsotoplog[0][0])[1]
        for i in range(1,CubeCenter.shape[1]):
            MassTemp=ifsArr2EleExtract(ListIsotoplog[i][0])[0]
            ProbTemp=ifsArr2EleExtract(ListIsotoplog[i][0])[1]
            MassAdder=np.append(MassAdder,MassTemp)
            ProbAdder=np.append(ProbAdder,ProbTemp)
        IsotoplogCollapse=np.array([MassAdder,ProbAdder])
    elif CubeCenter.shape[1]==1 and CubeCenter.shape[2]>1:
        for j in range(CubeCenter.shape[2]):
            MassAdder=ifsArr2EleExtract(ListIsotoplog[0][j])[0]
            ProbAdder=ifsArr2EleExtract(ListIsotoplog[0][j])[1]
            MassArrayAdder.append(MassAdder)
            ProbArrayAdder.append(ProbAdder)
        IsotoplogCollapse=np.array([MassArrayAdder,ProbArrayAdder])
    elif CubeCenter.shape[1]==1 and CubeCenter.shape[2]==1:
        MassAdder=ifsArr2EleExtract(ListIsotoplog[0][0])[0]
        ProbAdder=ifsArr2EleExtract(ListIsotoplog[0][0])[1]
        IsotoplogCollapse=np.array([MassAdder,ProbAdder])
    return [CenterCollapse,IsotoplogCollapse]

def ifsList2Array(CenterIsotoplogCollapse):
    #Input: output data from ifsCollapse, L=[CM,FM]
    #Output: array data for ifsMulti computation
    Center=CenterIsotoplogCollapse[0]
    Isotoplog=CenterIsotoplogCollapse[1]
    massArray=[]
    probArray=[]
    for i in range(Center.shape[1]):
        mass=[]
        prob=[]
        masscenter=np.array([Center[0][i]])
        massfine=Isotoplog[0][i]
        mass.append(masscenter)
        mass.append(massfine)
        probcenter=np.array([Center[1][i]])
        probfine=Isotoplog[1][i]
        prob.append(probcenter)
        prob.append(probfine)
        massArray.append(mass)
        probArray.append(prob)
    return np.array([massArray,probArray])
    
def ifsMulti(A1,A2):
    #Input: Array=np.array([MassArray,ProbArray])
    #MassArray=[m1,m2,m3,...]
    #m1=[mc1,mf1]
    #mc1=np.array([center mass value])
    #mf1=np.array([isotoplog mass1, isotoplog mass2, ...])
    #ProbArray is similar to MassArray
    #Output: Array with similar structure to the Input to include the
    #combination of L1 and L2
    s1=ifsCenterArray(A1)
    s2=ifsCenterArray(A2)
    cubeCenter=ifs_isoMulti(s1,s2) #Center m-p data is a cube array
    listIsotoplog=[] #Isotoplog m-p data is a 3D list
    for i in range(cubeCenter.shape[1]):
        listIsotoplog1D=[]
        for j in range(cubeCenter.shape[2]):
            listIsotoplog1D.append(ifsMultiSub(A1,i,A2,j))
        listIsotoplog.append(listIsotoplog1D)
    CenterIsotoplogShift=ifsShift([cubeCenter,listIsotoplog])
    CenterIsotoplogCollapse=ifsCollapse(CenterIsotoplogShift)
    CenterIsotoplog=ifsList2Array(CenterIsotoplogCollapse)
    return CenterIsotoplog

def ifsTrunc(A,thre):
    #Input: Array=np.array([MassArray,ProbArray]) from ifsMulti
    #Output: similar data structure, but with prob>=thre
    #NOTICE: since MassArray in A contains a center mass and corresponding\
    #isotoplog masses, ifsTrunc removes isotoplogs lower than thre,\
    #therefore some MassArray may contains only a center mass after truncation.
    #In this situation, the corresponding center mass was also removed even the
    #center prob>=thre.
    mArr=[]
    pArr=[]
    for i in range(len(A[0])):
        m=[]
        mc=A[0][i][0]
        m.append(mc)
        mf=np.array([])
        p=[]
        pc=A[1][i][0]
        p.append(pc)
        pf=np.array([])
        for j in range(len(A[0][i][1])):
            if A[1][i][1][j]>=thre:
                mf=np.append(mf,[A[0][i][1][j]])
                pf=np.append(pf,[A[1][i][1][j]])
        if list(mf)!=[]:
            mf=np.append(mf,mc)
            pf=np.append(pf,[0])
        m.append(mf)
        p.append(pf)
        mArr.append(m)
        pArr.append(p)
    posList=[]
    for i in range(len(mArr)):
        if list(mArr[i][1])==[]:
            posList=posList+[i]
    mTrunc=np.delete(mArr,tuple(posList),axis=0)
    pTrunc=np.delete(pArr,tuple(posList),axis=0)
    return np.array([mTrunc,pTrunc])

def ifsTruncNew(A,thre):
    #Similar to ifsTrunc, but using list instead of array in trunc
    #But computation speed is not good, needs optimization
    #Not used in the current version
    mArr=[]
    pArr=[]
    for i in range(len(A[0])):
        m=[]
        mc=A[0][i][0]
        m.append(mc)
        p=[]
        pc=A[1][i][0]
        p.append(pc)
        mf=[]
        pf=[]
        mfList=[]
        pfList=[]
        mpTemp=np.array([A[0][i][1],A[1][i][1]])
        for j in range(len(mpTemp[0])):
            if mpTemp[1][j]>=thre:
                mfList.append(mpTemp[0][j])
                pfList.append(mpTemp[1][j])
        mf=np.array(mfList)
        pf=np.array(pfList)
        if list(mf)!=[]:
            mf=np.append(mf,mc)
            pf=np.append(pf,[0])
        m.append(mf)
        p.append(pf)
        mArr.append(m)
        pArr.append(p)
    posList=[]
    for i in range(len(mArr)):
        if list(mArr[i][1])==[]:
            posList=posList+[i]
    mTrunc=np.delete(mArr,tuple(posList),axis=0)
    pTrunc=np.delete(pArr,tuple(posList),axis=0)
    return np.array([mTrunc,pTrunc])

def ifsTruncAcc(A,thre):
    #Accerlerated ifsTrunc, only used in the final step of ifsOpt
    #Input: the same as ifsTrunc
    #Output: the same as ifsTrunc
    mpArr=np.array([A[0][0][1],A[1][0][1]])
    mList=[]
    pList=[]
    for i in range(len(mpArr[0])):
        if mpArr[1][i]>=thre:
            mList.append(mpArr[0][i])
            pList.append(mpArr[1][i])
    mArr=[]
    pArr=[]
    m=[]
    mc=A[0][0][0]
    m.append(mc)
    mf=np.array(mList)
    m.append(mf)
    p=[]
    pc=A[1][0][0]
    p.append(pc)
    pf=np.array(pList)
    p.append(pf)
    mArr.append(m)
    pArr.append(p)
    posList=[]
    for i in range(len(mArr)):
        if list(mArr[i][1])==[]:
            posList=posList+[i]
    mTrunc=np.delete(mArr,tuple(posList),axis=0)
    pTrunc=np.delete(pArr,tuple(posList),axis=0)
    return np.array([mTrunc,pTrunc])

def ifsMerge(A):
    Diff=1e-6
    mArr=[]
    pArr=[]
    for i in range(len(A[0])):
        m=[]
        mc=A[0][i][0]
        m.append(mc)
        mf=np.array([])
        p=[]
        pc=A[1][i][0]
        p.append(pc)
        pf=np.array([])
        mf=np.append(mf,[A[0][i][1][0]])
        pf=np.append(pf,[A[1][i][1][0]])
        if len(A[0][i][1])==1:
            mf=np.append(mf,[A[0][i][1][0]])
            pf=np.append(pf,[0])
        else:
            for j in range(1,len(A[0][i][1])):
                judge=0
                for jj in range(len(mf)):
                    if abs(A[0][i][1][j]-mf[jj])<=Diff:
                        pf[jj]=pf[jj]+A[1][i][1][j]
                        judge=1
                        break
                if judge==0:
                    mf=np.append(mf,[A[0][i][1][j]])
                    pf=np.append(pf,[A[1][i][1][j]])
        if len(mf)==1:
            mf=np.append(mf,mf)
            pf=np.append(pf,[0])
        m.append(mf)
        p.append(pf)
        mArr.append(m)
        pArr.append(p)
    return np.array([mArr,pArr])

def ifsCombine(A1,A2,thre):
    NA1=ifsConsec(A1)
    NA2=ifsConsec(A2)
    Temp1=ifsMulti(NA1,NA2)
    Temp2=ifsMerge(Temp1)
    Temp=ifsTrunc(Temp2,thre)
    return Temp

def ifsCombineAcc(A1,A2,thre):
    #Accelerated version of ifsCombine, only used in ifsSuCluster function
    NA1=ifsConsec(A1)
    NA2=ifsConsec(A2)
    Temp1=ifsMulti(NA1,NA2)
    Temp=ifsTrunc(Temp1,thre)
    return Temp

def ifsFormula(Str):
    #This function is used to read input molecular formula and
    #transform the formula into an element name list and a number
    #list.
    #check formula
    if ord(Str[-1])>=65 and ord(Str[-1])<=122:
        print('Error: Please check the input formula')
        return
    IsotopeNameList=['H','Li','Be','B','C','N','O','F','Na','Mg','Al','Si',\
                     'P','S','Cl','K','Ca','Ti','V','Cr','Mn','Fe','Co','Zn',\
                     'Ga','Ge','As','Se','Br','Rb','Sr','Y','Zr','Nb','Mo',\
                     'Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Cs',\
                     'Ba','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl',\
                     'Pb','Bi']
    #divide Str into name list and number list
    NameList=[]
    NumberList=[]
    NameListTemp=''
    NumberListTemp=''
    i=0
    while i<len(Str):
        if ord(Str[i])>=65 and ord(Str[i])<=122:
            for ii in range(i,int(len(Str))):
                if ord(Str[ii])>=65 and ord(Str[ii])<=122:
                    NameListTemp=NameListTemp+Str[ii]
                else:
                    break
            i=ii
            NameList.append(NameListTemp)
            NameListTemp=''
        elif ord(Str[i])>=48 and ord(Str[i])<=57:
            for ii in range(i,int(len(Str))):
                if ord(Str[ii])>=48 and ord(Str[ii])<=57:
                    NumberListTemp=NumberListTemp+Str[ii]
                else:
                    break
            i=ii
            NumberList.append(int(NumberListTemp))
            NumberListTemp=''
            if i==int(len(Str))-1:
                i=i+1               
    #check formula
    for i in range(0,int(len(NameList))):
        if NameList[i] not in IsotopeNameList:
            print('Error: Please check the input formula.')
            return
    #merge name list
    NameListMerge=[NameList[0]]
    NumberListMerge=[NumberList[0]]
    for i in range(1,int(len(NameList))):   
        judge=0
        for j in range(0,int(len(NameListMerge))):
            if NameListMerge[j]==NameList[i]:
                NumberListMerge[j]=NumberListMerge[j]+NumberList[i]
                judge=1
        if judge==0:
            NameListMerge.append(NameList[i])
            NumberListMerge.append(NumberList[i])
    return [NameListMerge,NumberListMerge]

def ifsElementFinder():
    #generate a reference number list for element in ifsData
    ElementList=[]
    for i in range(ifsData.shape[0]):
        ElementList.append(ifsData[i][0][0][0])
    return ElementList

def ifsDecom(Number,Limit):
    #This function decomposes an input Number into a denomination system
    #(1,2,5,10,20,50,...)with a upper Limit.
    DenomiSys=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000]
    LimitIndex=DenomiSys.index(Limit)
    Denom=DenomiSys[0:LimitIndex+1]
    Denom.reverse()
    #decomposition of Number into Denom
    Count=[0]*int(len(Denom))
    while Number>0:
        for i in range(int(len(Denom))):
            if Denom[i]-Number<=0:
                Count[i]=Count[i]+1
                Number=Number-Denom[i]
                break     
    return np.array([Denom,Count])

def ifsBoundary(A):
    #find max of Array
    maxList=[]
    for i in range(A.shape[1]):
        maxList.append(np.max(A[1][i][1]))
    Max=max(maxList)
    return Max

def ifsLen(A):
    #compute the number of isotoplogs in A
    Len=0
    for i in range(A.shape[1]):
        Len=Len+A[0][i][1].shape[0]
    return Len

def ifsElement(formula,thre):
    #advanced version of isoElement
    #computing isotope fine structure of given element clusters
    #by denomination algorithm
    #Input: element clusters 'Xn',threshold
    #Output: Array=np.array([MassArray,ProbArray]) for all ifs functions
    DenomiSys=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000]
    ElementName=ifsFormula(formula)[0][0]
    ElementNumber=ifsFormula(formula)[1][0]
    ElementCoord=ifsElementFinder().index(ElementName)
    ElementIsotope=ifsData[ElementCoord][1] #Isotope list with denomination
    Limit=ifsData[ElementCoord][0][2][0]
    DecomArray=ifsDecom(ElementNumber,Limit)
    for i in range(DecomArray.shape[1]):
        if DecomArray[1,i]>=1:
            ElementNumberDenom=DecomArray[0,i]
            DenomRef=DenomiSys.index(ElementNumberDenom)
            EleIsotopeAdder=ifsTrunc(ElementIsotope[DenomRef],thre)
            DecomArray[1,i]=DecomArray[1,i]-1
            break
    DecomSum=sum(DecomArray[1,...])
    if DecomSum==0:
        return EleIsotopeAdder
    else:
        while DecomSum>0:
            for i in range(DecomArray.shape[1]):
                if DecomArray[1,i]>=1:
                    ElementNumberDenom=DecomArray[0,i]
                    DenomRef=DenomiSys.index(ElementNumberDenom)
                    EleIsotopeTemp=ifsTrunc(ElementIsotope[DenomRef],thre)
                    DecomArray[1,i]=DecomArray[1,i]-1
                    break
            EleIsotopeAdder=ifsCombine(EleIsotopeAdder,EleIsotopeTemp,thre)
            DecomSum=sum(DecomArray[1,...])
        return EleIsotopeAdder

def iso2ifs(Aiso):
    #the function translate data structure of isoFunction into ifsFunction
    #Input: iso() computed array
    #Output: array for ifsFunction
    mArr=[]
    pArr=[]
    for i in range(len(Aiso[0])):
        m=[]
        p=[]
        mc=np.array([Aiso[0][i]])
        mf=np.array([Aiso[0][i],Aiso[0][i]])
        m.append(mc)
        m.append(mf)
        pc=np.array([Aiso[1][i]])
        pf=np.array([Aiso[1][i],0])
        p.append(pc)
        p.append(pf)
        mArr.append(m)
        pArr.append(p)
    return np.array([mArr,pArr])

def ifs2iso(Aifs):
    #the function translate data structure of ifsFunction into isoFunction
    #Input: ifs() computed array
    #Output: array for isoFunction
    m=[]
    p=[]
    for i in range(Aifs.shape[1]):
        m.append(Aifs[0][i][0][0])
        p.append(Aifs[1][i][0][0])
    return np.array([m,p])

def ifsElementAcc(formula,thre):
    #Accelerated version of ifsElement
    #Element contains less than 2 stable isotopes will be computed by\
    #isoFunction instead of ifsFunction to further improve the efficiency
    ElementName=ifsFormula(formula)[0][0]
    ElementCoord=ifsElementFinder().index(ElementName)
    if ifsData[ElementCoord][0][1][0]<=2:
        ArrayIso=isoElement(formula,thre)
        return iso2ifs(ArrayIso)
    elif ifsData[ElementCoord][0][1][0]>2:
        ArrayIfs=ifsElement(formula,thre)
        return ArrayIfs

def ifsSuClusterGrouping(EleName,EleClusIsotope,ThreMaxList):
    #the function groups elements of input formula into two classes for\
    #generation of SuperCluster by ifsSuCluster
    #G1 is H,C,N
    #G2 is O,S
    Name=['H','C','N','O','S']
    G=[0,0,0,0,0]
    EleClusIsoG=[[],[],[],[],[]]
    ThreMaxListG=[0,0,0,0,0]
    for i in range(len(EleName)):
        for j in range(len(Name)):
            if EleName[i]==Name[j]:
                G[j]=1
                EleClusIsoG[j]=EleClusIsotope[i]
                ThreMaxListG[j]=ThreMaxList[i]
    return [Name,G,EleClusIsoG,ThreMaxListG]

def ifsSuCluster(EleName,EleClusIsotope,thre,ThreMaxList):
    #Generate two super clusters from EleClusIsotope by ifsCombine
    #for CHNOS, two super clusters are CHO,NS
    #CH=ifsCombine(EleClusIsotope[0],EleClusIsotope[1],thre)
    #CHO=ifsCombine(CH,EleClusIsotope[3],thre)
    #NS=ifsCombine(EleClusIsotope[2],EleClusIsotope[4],thre)
    SuClusterGroup=ifsSuClusterGrouping(EleName,EleClusIsotope,ThreMaxList)
    ClusSum=sum(SuClusterGroup[1])
    if ClusSum==1:
        pos=SuClusterGroup[1].index(1)
        SuCluster=SuClusterGroup[2][pos]
        return [SuCluster]
    elif ClusSum==2:
        pos=[]
        for i in range(len(SuClusterGroup[0])):
            if SuClusterGroup[1][i]==1:
                pos.append(i)
        SuCluster1=ifsTrunc(SuClusterGroup[2][pos[0]],\
                            thre/(SuClusterGroup[3][pos[1]]))
        SuCluster2=ifsTrunc(SuClusterGroup[2][pos[1]],\
                            thre/(SuClusterGroup[3][pos[0]]))
        return [SuCluster1,SuCluster2]
    elif ClusSum==3:
        pos=[]
        for i in range(len(SuClusterGroup[0])):
            if SuClusterGroup[1][i]==1:
                pos.append(i)
        SuCluster1=ifsCombineAcc(SuClusterGroup[2][pos[0]],\
                                 SuClusterGroup[2][pos[1]],\
                                 thre/SuClusterGroup[3][pos[2]])
        SuCluster2=ifsTrunc(SuClusterGroup[2][pos[2]],\
                            thre/(SuClusterGroup[3][pos[0]]*\
                                  SuClusterGroup[3][pos[1]]))
        return [SuCluster1,SuCluster2]
    elif ClusSum==4:
        pos=[]
        for i in range(len(SuClusterGroup[0])):
            if SuClusterGroup[1][i]==1:
                pos.append(i)
        SuCluster1=ifsCombineAcc(SuClusterGroup[2][pos[0]],\
                                 SuClusterGroup[2][pos[1]],\
                                 thre/(SuClusterGroup[3][pos[2]]*\
                                       SuClusterGroup[3][pos[3]]))
        SuCluster2=ifsCombineAcc(SuClusterGroup[2][2],\
                                 SuClusterGroup[2][3],\
                                 thre/(SuClusterGroup[3][0]*\
                                       SuClusterGroup[3][1]))
        return [SuCluster1,SuCluster2]
    elif ClusSum==5:
        SuCluster1=ifsCombineAcc(SuClusterGroup[2][3],\
                                 SuClusterGroup[2][4],\
                                 thre/(SuClusterGroup[3][0]*\
                                       SuClusterGroup[3][1]*\
                                       SuClusterGroup[3][2]))
        SuCluster2Temp=ifsCombineAcc(SuClusterGroup[2][0],\
                                     SuClusterGroup[2][1],
                                     thre/(SuClusterGroup[3][2]*\
                                           SuClusterGroup[3][3]*\
                                           SuClusterGroup[3][4]))
        SuCluster2=ifsCombineAcc(SuCluster2Temp,\
                                 SuClusterGroup[2][2],\
                                 thre/(SuClusterGroup[3][3]*\
                                       SuClusterGroup[3][4]))
        return [SuCluster1,SuCluster2]

def ifsSuClusterMulti(A1,A2,mass):
    #find row and column position for a corresponding mass
    NA1=ifsConsec(A1)
    NA2=ifsConsec(A2)
    judge=0
    j=0
    for i in range(NA1.shape[1]): #NA1 pos
        if abs(NA1[0][i][0][0]+NA2[0][j][0][0]-mass)<=0.2:
            judge=1
            posNA1=i
            posNA2=j
            break
    if judge==0:
        for j in range(1,NA2.shape[1]): #NA2 pos
            if abs(NA1[0][i][0][0]+NA2[0][j][0][0]-mass)<=0.2:
                posNA1=i
                posNA2=j
                break
    posList1=[]
    posList2=[]
    j=posNA2
    for i in range(posNA1,-1,-1):
        posList1.append(i)
        posList2.append(j)
        j=j+1
        if j==NA2.shape[1]:
            break
    mf=[0]
    pf=[0]
    mpcTemp=0 #center mass-prob
    pcTemp=0 #center prob
    for k in range(len(posList1)):
        mpTemp=[]
        mpTemp=ifsMultiSub(NA1,posList1[k],NA2,posList2[k])
        mf=mf+list(mpTemp[0]) #ifs mass
        pf=pf+list(mpTemp[1]) #ifs prob
        pcTemp=pcTemp+NA1[1][posList1[k]][0][0]*NA2[1][posList2[k]][0][0]
        mpcTemp=mpcTemp+(NA1[0][posList1[k]][0][0]+\
                 NA2[0][posList2[k]][0][0])*(NA1[1][posList1[k]][0][0]*\
                                             NA2[1][posList2[k]][0][0])
    pc=pcTemp
    mc=mpcTemp/pc
    mArr=[] #only one center isotope here, but still needs this to keep
    pArr=[] #the consistency in data structure
    m=[]
    mcArr=np.array([mc])
    m.append(mcArr)
    m.append(np.array(mf))
    mArr.append(m)
    p=[]
    pcArr=np.array([pc])
    p.append(pcArr)
    p.append(np.array(pf))
    pArr.append(p)
    return np.array([mArr,pArr])

def ifsCheck(A):
    #computing number of isotoplogs, average mass, probability
    #IsoArray=iso(formula,thre)
    #IsoMax=isoMax(IsoArray)
    p=0
    mp=0
    for i in range(len(A[0][0][1])):
        p=p+A[1][0][1][i]
        mp=mp+A[1][0][1][i]*A[0][0][1][i]
    m=mp/p
    return [m,p]

def ifsCheckAbs(A,formula,thre):
    #absolute check version of ifsCheck
    IsoArray=iso(formula,thre)
    for i in range(IsoArray.shape[1]):
        if abs(A[0][0][0][0]-IsoArray[0][i])<=0.2:
            pos=i
            break
    p=0
    mp=0
    for i in range(len(A[0][0][1])):
        p=p+A[1][0][1][i]
        mp=mp+A[1][0][1][i]*A[0][0][1][i]
    m=mp/p
    print('----------SUMMARY OF IFS CALCULATION-----------------------')
    print('Molecular formula =',formula)
    print('Intensity threshold =',format(thre,'0.2e'))
    print('Number of isotopologues =',ifsLen(A))
    print('Average mass from isotopologues =',m)
    print('Average mass from center isotope =',IsoArray[0][pos])
    print('Mass error =',m-IsoArray[0][pos])
    print('Intensity from isotoplogs =',p)
    print('Intensity from center isotope =',IsoArray[1][pos])
    print('Intensity error =',p-IsoArray[1][pos])
    return

def ifs(formula,thre,mass):
    t0=time.process_time()
    thre_low=1e-8
    EleName=ifsFormula(formula)[0]
    EleNumber=ifsFormula(formula)[1]
    EleClusIsotope=[]
    ThreMaxList=[]
    for i in range(len(EleName)):
        t0=time.process_time()
        ClusFormula=ifsFormula(formula)[0][i]+str(ifsFormula(formula)[1][i])
        ClusIsotope=ifsElementAcc(ClusFormula,thre_low)
        EleClusIsotope.append(ClusIsotope)
        ThreMaxList.append(ifsBoundary(ClusIsotope))
    EleClusIsoTrunc=[]
    if len(EleName)==1:
        for i in range(ClusIsotope.shape[1]):
            if abs(ClusIsotope[0][i][0][0]-mass)<=0.2:
                pos=i
        Temp1=np.array([[ClusIsotope[0][pos]],[ClusIsotope[1][pos]]])
        ifsATpos=ifsTruncAcc(Temp1,thre)
    if len(EleName)>1:
        for i in range(len(EleName)):
            ThreCopy=ThreMaxList.copy()
            del ThreCopy[i]
            ThreDyn=reduce(lambda x,y:x*y,ThreCopy)
            ThreDyn=thre/ThreDyn
            ClusIsotopeTrunc=ifsTrunc(EleClusIsotope[i],ThreDyn)
            EleClusIsoTrunc.append(ClusIsotopeTrunc)
        SuCluster=ifsSuCluster(EleName,EleClusIsoTrunc,thre,ThreMaxList)
        SuCluster1=SuCluster[0]
        SuCluster2=SuCluster[1]
        Temp1=ifsSuClusterMulti(SuCluster1,SuCluster2,mass)
        ifsATpos=ifsTruncAcc(Temp1,thre)
    t1=time.process_time()-t0
    ck=ifsCheck(ifsATpos)
    print('----------SUMMARY OF IFS CALCULATION-----------------------')
    print('Molecular formula =',formula)
    print('Selected zoom-in mass =',format(mass,'0.4f'),'+/- 0.2 Da')
    print('Intensity threshold =',format(thre,'0.2e'))
    print('Number of isotopologues =',ifsLen(ifsATpos))
    print('Average mass from isotopologues =',format(ck[0],'0.4f'),'Da')
    print('Average mass from center isotope =',format(ifsATpos[0][0][0][0],'0.4f'),'Da')
    print('Mass error =',format(abs(ck[0]-ifsATpos[0][0][0][0]),'0.2e'),'Da')
    print('Intensity from isotoplogs =',format(ck[1],'0.4f'))
    print('Intensity from center isotope =',format(ifsATpos[1][0][0][0],'0.4f'))
    print('Intensity error =',format(abs(ck[1]-ifsATpos[1][0][0][0]),'0.2e'))
    print('Elapsed time =',format(t1,'0.3f'),'seconds')
    print('\n----------DATA DISPLAY-------------------------------------')
    print('Use ifsPlot to view the spectrum')
    print('Use ifsList to print mass and intensity list')
    return ifsATpos

def ifsNorm(s,switch):
    #Display prob in rel-scale or abs-scale
    #Input: square array data, switch=rel or abs
    if switch=='rel':
        prob_max=max(s[1,...])
        prob_rel=100*s[1,...]/prob_max
        s_disp=np.array([s[0,...],prob_rel])
    elif switch=='abs':
        s_disp=s
    return s_disp

def ifsPlot(A):
    if A.shape[1]==1:
        plt.stem(A[0][0][1],A[1][0][1],'k',',',',')
    else:
        m=[]
        p=[]
        for i in range(A.shape[1]):
            m.append(A[0][i][0][0])
            p.append(A[1][i][0][0])
        plt.stem(m,p,'k',',',',')
    plt.show()
    return

def ifsList(A):
    m=list(A[0][0][1])
    p=list(A[1][0][1])
    return [m,p]
#######################the end of ifsFunction#################################


#######################testing molecular formula##############################
#C520H817N139O147S8  11623.9
#C744H1224N210O222S5
#C2023H3208N524O619S20
#C2934H4615N781O897S39  66431.9
#C5047H8014N1338O1495S48  
#C8574H13378N2092O2392S77  186505.1
#C17600H26474N4752O5486S197  398722.0
#C23832H37816N6528O7031S170  533734.3
#######################end of testing molecular formula#######################


#######################testing code###########################################
rootpath=os.getcwd()
filepath1=os.path.join(rootpath,'Lib\site-packages\isovectpy\ifsData.npy')
filepath2=os.path.join(rootpath,'Lib\site-packages\isovectpy\isoData.npy')
ifsData=np.load(filepath1, allow_pickle=True)
IsoDataCenterMass=np.load(filepath2, allow_pickle=True)
#tt=ifs('C520H817N139O147S8',1e-8,11623.9)
#tt=iso('C23832H37816N6528O7031S170',1e-8)
