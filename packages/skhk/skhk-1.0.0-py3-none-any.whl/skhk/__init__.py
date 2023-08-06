def print1():
	print('aglo \n')
	print('''import math
import numpy as np
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import dendrogram, linkage  
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering

X = [[1.1,60],[8.2,0.20],[4.2,0.35],[1.5,0.21],[7.6,0.15],[2.0,55],[3.9,39]]

Y = []
z = len(X)
cluster=[]
names = [str(i) for i in range(len(X)+1)]
def mini():
    m = 999.0
    a,b = -1,-1
    temp = 0
    for i in range(len(Y)):
        for j in range(len(Y)):
            if(i==j):
                continue
            if(Y[i][j]<m):
                m=Y[i][j]
                a,b=i,j
    if a<b:
        names[a]=str(names[a])+","+str(names[b])
        names.pop(b)
    else:
        names[b]= str(names[a])+","+str(names[b])
        names.pop(a)
        temp =a
        a=b
        b = temp
    cluster.append(m)
    return a,b

def minin(num1,num2):
    if num1 is None or num2 is None:
        return None
    if(num1<num2):
        return num1
    else:
        return num2
    
def reduce_cluster(a,b):
    for i in range(len(Y)):
        for j in range(len(Y)):
            if(i==a or i == b ):
                Y[a][j] = minin(Y[a][j],Y[b][j])
            if(j ==a or j ==b):
                Y[i][a] = minin(Y[i][a],Y[i][b])
    Y.pop(b)
    for i in range(len(Y)):
        Y[i].pop(b)

def find_distance():
    for i in range(0,z): 
        temp_list = []
        for j in range(0,z):    
            if(i==j):
                temp= None
            else:
                temp = round(math.sqrt(math.pow(X[i][0]-X[j][0],2)+ math.pow(X[i][1]-X[j][1],2)),2)
            ##print(temp)
            temp_list.append(temp)
        Y.append(temp_list)
    return Y
Y = find_distance()
print("The Clusters are lablelled as 0,1..",len(X)-1)
for i in range(len(Y)):
    m,n = mini()
    print("For",i+1,"iteration the clusters formed are:",names[m])
    reduce_cluster(m,n)
X = np.array(X)
cluster = AgglomerativeClustering(n_clusters=1, affinity='euclidean', linkage='ward')  
cluster.fit_predict(X)  

linked = linkage(X, 'single')
labelList = range(1, 11)
dendrogram(linked, orientation='top',distance_sort='descending',show_leaf_counts=True)
plt.show()
''')
def print2():
	print('apriori \n')
	print('''from itertools import *
f=open("dataset.txt","r")
data=[]
c1,c2,u={},{},{}
l1,l2={},{}
sp_c,v=3,0
it=2

def association(r,r2,r1):
    print("SR Association rules\t\tSupp_count\t\tConfidence\t\tConfidence in %")
    s=[]
    p=[]
    fp=[]
    sr=0
    for f,v in r2.items():
        s.append(f)
        p.append(v)
    for d in r.keys():
        a,b,c=d
        for t in s:
            q,z=t
            if(b==q and c==z):
                g=3/p[s.index(t)]
            if(c==q and b==z):
                g=3/p[s.index(t)]
            if(a==q and c==z):
                j=3/p[s.index(t)]
            if(c==q and a==z):
                j=3/p[s.index(t)]
            if(a==q and b==z):
                h=3/p[s.index(t)]
            if(b==q and a==z):
                h=3/p[s.index(t)]
        sr=sr+1
        fr=sr
        print(sr,a+"=>"+b+"^"+c+"\t\t\t"+"3"+"\t\t\t{}\t\t\t{}%".format(g,g*100))
        if(g*100>=75):
            fp.append(sr)
        sr=fr+1
        fr=sr
        print(sr,b+"=>"+a+"^"+c+"\t\t\t"+"3"+"\t\t\t{}\t\t\t{}%".format(j,j*100))
        if(j*100>=75):
            fp.append(sr)
        sr=fr+1
        fr=sr
        print(sr,c+"=>"+a+"^"+b+"\t\t\t"+"3"+"\t\t\t{}\t\t\t{}%".format(h,h*100))
        if(h*100>=75):
            fp.append(sr)
             
    print("As the minimum confidence is 75%(given) the association rules are:")
    for pg in range(len(fp)):
        print(fp[pg] ,end =" ")
    
        
def keyprint(test):
    for key in test:
        print(key)
def w_print(test1):
    for key,value in test1.items():
        print("{}:{}".format(key,value))
        
def final1(th,th1,th2):
    print("As there are no items in the candidate list the candidate C3 is chosen for association rules")
    w_print(th)
    association(th,th1,th2)

def check_min_support(cnd):
    pl={}
    for key,value in cnd.items():
        if(value>=3):
            pl[key]=value
    return pl

def Combo(k,b):
    per=0
    if(len(k)>b):
        per=combinations(k,b)
        b+=1
    else:
        #final1(k,l2,l1)
        exit()
    return(per)

#printing dataset
print("dataset")
for i in f:
    data.append(i.split())
    print(i,end="")

print()

#appending dataset items count in key-value pair and printing the values
for j in range(len(data)):
    for i in range(1,len(data[j])):
        if(data[j][i] in c1):
            c1[data[j][i]]=c1.get(data[j][i])+1
        else:
            c1[data[j][i]]=1
            
fir=[]
for sa in c1.keys():
    fir.append(sa)
    
print("Scan D for the count of each candidate.The candidate list is {} and find the support:".format(fir))
print("C1=")
w_print(c1)
#checking min_supp

l1=check_min_support(c1)
print("Compare the candidate key with minimum support count ({}):".format(sp_c))
print("L1=")
w_print(l1)
print()
print("Genrate candidate c2 from l1:")

k=[i for i in l1.keys()]                #getting all keys

comb=Combo(k,it)      #finding all combinations of the items
for h in list(comb):
    c2[h]=0
    
print("C2=")
keyprint(c2)
temp=[i for i in c2.keys()] #getting all keys from c2

for i in range(len(temp)):
    for r in range(len(data)):
            y,z=temp[i]
            if(y in data[r] and z in data[r]):
                c2[temp[i]]=c2.get(temp[i])+1

print("Scan D for count of each candidate in C2 and find support count:")
print("C2=")
w_print(c2)
print("Compare candidate C2 support count with minimum support count:")
l2=check_min_support(c2)
print("L2=")
w_print(l2)
print()

it+=1
k=[p for p in l2.keys()]
data1=[]
for j in range(len(k)):
    y,z=k[j]
    data1.append(y)
    data1.append(z)
s=set(data1)
#print(s)

l4={}
d=[]

comb=Combo(s,it)
for i in list(comb):
    l4[i]=0
    d.append(i)

for i in range(len(d)):
    a,b,c=d[i]
    for t in range(len(data)):
        if(a in data[t] and b in data[t] and c in data[t]):
            l4[d[i]]=l4.get(d[i])+1

print("Genrate candidate C3 from l2:")
print("C3=")
keyprint(l4)
print("Scan D for count of each candidate in C3:")
print("C3=")
w_print(l4)
u=check_min_support(l4)
print("Compare candidate C3 support count with minimum support count:")
print("L3=")
w_print(u)
print()

it+=1
k=[p for p in u.keys()]

data1=[]
for j in range(len(k)):
    y,z,m=k[j]
    data1.append(y)
    data1.append(z)
    data1.append(m)
s=set(data1)

c4=Combo(s,it)
data1=[]
l5={}
for i in c4:
    data1.append(i)
    l5[i]=0
for o in range(len(data1)):
    d,f,g,h=data1[o]
    for j in range(len(data)):
        if(d in data[j] and f in data[j] and g in data[j] and h in data[j]):
            l5[data1[o]]=l5.get(data1[o])+1

print("Generate candidate C4 from l3:")
print("C4=")
keyprint(l5)
print("Scan D for count of each candidate in C4:")
print("C4=")
w_print(l5)
w=check_min_support(l5)
print("Compare candidate C4 with minimum support count:")
print("l4={}".format(w))
final1(u,l2,l1)
---dataset---
T1 I1 I2 I5
T2 I1 I3 I2 I4
T3 I1 I3 I5 I2
T4 I3 I5 I4
T5 I1 I3 I4
T6 I2 I4 I5 I3
T7 I5 I2 I4
T8 I4 I2 I1
T9 I3 I2 I5
T10 I1 I4 I5 I3
''')
def print3():
	print('naive \n')
	print('''X= [[1,2,0,1,0],[1,2,0,0,0],[0,2,0,1,1],[2,1,0,1,1],[2,0,1,1,1],[2,0,1,0,0],[0,0,1,0,1],[1,1,0,1,0],[1,0,1,1,1],[2,1,1,1,1],[1,1,1,0,1],[0,1,0,0,1],[0,2,1,1,1],[2,1,0,0,0]]

test=[0,0,0,0]
probyes = [0.0,0.0,0.0,0.0]
probno = [0.0,0.0,0.0,0.0]

age = input("\nEnter the age like Youth, Middle_aged, Senior : ")
if age=="Youth"or "youth":
	test[0]=1
elif age=="Middle_aged":
	test[0]=0
else:
	test[0]=2

income = input("\nEnter the Income like Medium, Low, High : ")
if income=="Medium" or "medium":
	test[1]=1
elif income=="Low" or "low":
	test[1]=0
else: 
	test[1]=2

student = input("\nEnter if it is Student Yes or No : ")
if student=="Yes" or "yes":
	test[2]=1
else:
	test[2]=0
	
cr=input("\nEnter Credit Rating Fair, Excellent : ")
if cr=="Fair":
	test[3]=0
else:
	test[3]=1
numyes = 9
numno = 5
pyes = float(9/14)
pno = float(5/14)

numyouthyes = 2
numyouthno = 3
nummiddleyes = 4
nummiddleno = 0
numsenioryes = 2 
numseniorno = 3

numhighyes = 2
numhighno = 2
nummiddleyes = 4
nummiddleno = 2
numlowyes = 3
numlowno = 1

numstudentno = 1
numstudentyes = 6 
numnostudentno = 4
numnostudentyes = 3

numfairyes = 6
numfairno = 2
numexcellentyes = 3
numexcellentno = 3

if test[0]==1:
    probyes[0] = float(numyouthyes/numyes)
    probno[0] = float(numyouthno/numno)
elif test[0]==0:
    probyes[0] = float(nummiddleyes/numyes)
    probno[0] = float(nummiddleno/numno)
elif test[0]==2:
    probyes[0] = float(numsenioryes/numyes)
    probno[0] = float(numseniorno/numno)

if test[1]==0:
    probyes[1] = float(numlowyes/numyes)
    probno[1] = float(numlowno/numno)
elif test[1]==1:
    probyes[1] = float(nummiddleyes/numyes)
    probno[1] = float(nummiddleno/numno)
elif test[1]==2:
    probyes[1] = float(numhighyes/numyes)
    probno[1] = float(numhighno/numno)
    

if test[2]==1:
    probyes[2] = float(numstudentyes/numyes)
    probno[2] = float(numstudentno/numno)
elif test[2]==0:
    probyes[2] = float(numnostudentyes/numyes)
    probno[2] = float(numnostudentno/numno)

if test[3]==0:
    probyes[3] = float(numfairyes/numyes)
    probno[3] = float(numfairno/numno)
elif test[3]==1:
    probyes[3] = float(numexcellentyes/numyes)
    probno[3] = float(numexcellentno/numno)

print("\nThe Probability of age is %s for class Yes is: "%age)
if test[0]==1:
	print(2/9)
elif test[0]==2:
	print(4/9)
elif test[0]==0:
	print(2/9)

print("\nThe Probability of age is %s for class No is: "%age)
if test[0]==1:
	print(3/5)
elif test[0]==2:
	print(3/5)
elif test[0]==0:
	print(0)

print("\nThe Probability of Income is %s for class yes is: "%income)
if test[1]==1:
	print(4/9)
elif test[1]==2:
	print(2/9)
elif test[1]==0:
	print(3/9)

print("\nThe Probability of Income is %s for class No is: "%income)
if test[1]==1:
	print(2/5)
elif test[1]==2:
	print(2/5)
elif test[1]==0:
	print(1/5)

print("\nThe Probability of if it is Student %s for class Yes is: "%student)
if test[1]==1:
	print(6/9)
elif test[1]==0:
	print(1/9)
print("\nThe Probability of if it is Student %s for class No is: "%student)
if test[1]==1:
	print(3/5)
elif test[1]==0:
	print(4/5)
print("\nThe Probability of Credit Rating is %s for class Yes is: "%cr)
if test[1]==1:
	print(6/9)
elif test[1]==0:
	print(3/9)
print("\nThe Probability of Credit Rating is %s for class No is: "%cr)
if test[1]==0:
	print(2/5)
elif test[1]==1:
	print(3/5)
for i in range(0,4):
    pyes *= probyes[i]
    pno *= probno[i]
print("\nThe probability of no is: ",pno)
print("\nThe probability of yes is: ",pyes)
if pyes>pno:
    print("\n\n\tProbability of class Yes is Greater than Class no hence He/She will Buys Computer")
elif pyes<pno:
    print("\n\n\tProbability of class No is Greater than Class Yes hence He/She will not Buys Computer")
''')
	
def print4():
	print('11  \n')
	print('''import numpy as np
import scipy as sc
import pandas as pd
from fractions import Fraction
def display_format(my_vector, my_decimal):
    return np.round((my_vector).astype(np.float), decimals=my_decimal)
my_dp = Fraction(1,3)
Mat = np.matrix([[0,0,1],
[Fraction(1,2),0,0],
[Fraction(1,2),1,0]])
Ex = np.zeros((3,3))
Ex[:] = my_dp
beta = 0.7
Al = beta * Mat + ((1-beta) * Ex)
r = np.matrix([my_dp, my_dp, my_dp])
r = np.transpose(r)
previous_r = r
for i in range(1,100):
    r = Al * r
    print (display_format(r,3))
    if (previous_r==r).all():
        break
    previous_r = r
print ("Final:\n", display_format(r,3))
print ("sum", np.sum(r))
''')

def print5():
	print('star \n')
	print('''server mgmt studio---
databases-newdb
tables-new table-(DT)data,primkey
tables-new-facttable(same col name) no allow null, to calculate
save
fact table-empty rightclick-relationships
add-tables and col 1 click, 3dots, <remote><fact>

''')
def print6():
	print('apriori java \n')
	print('''import java.io.*;
class ap
{ 
public static void main(String []arg)throws IOException
{
int i,j,m=0;
int t1=0;
BufferedReader b=new BufferedReader(new InputStreamReader(System.in));
System.out.println("Enter the number of transaction :");
int n=Integer.parseInt(b.readLine());
System.out.println("Enter the number of Items :");
int n1=Integer.parseInt(b.readLine());
int item[][]=new int[n][n1];
int[] itemlist=new int[n1];
for(i=0;i<n;i++)
 for(j=0;j<n1;j++)
   item[i][j]=0;
for(i=0;i<n1;i++)
   itemlist[i]=i+1;

int nt[]=new int[n1];
int q[]=new int[n1];

for(i=0;i<n;i++)
{ System.out.println("\nTransaction "+(i+1)+" :");
  for(j=0;j<n1;j++)
  {
     System.out.print("Is Item "+itemlist[j]+" present in this transaction(1/0)? :");
     item[i][j]=Integer.parseInt(b.readLine()); 
  }
}
System.out.println("\nEnter Minimum Support :");
int ms=Integer.parseInt(b.readLine());
System.out.println("\n "); 
System.out.println("C1=\n"); 
 for(j=0;j<n1;j++) 
  { for(i=0;i<n;i++)
    {if(item[i][j]==1)
      nt[j]=nt[j]+1;
    }
    System.out.println("Number of Item "+itemlist[j]+" :"+nt[j]);
  }
System.out.println("\n "); 
System.out.println("L1=\n"); 
for(j=0;j<n1;j++)
{ if(nt[j]>=ms)
    q[j]=1;
  else
   { q[j]=0;}

  if(q[j]==1)
   {t1++;
    System.out.println("Item "+itemlist[j]+" is selected "); 
   
   }
}
 for(j=0;j<n1;j++) 
  { for(i=0;i<n;i++)
   {
     
     if(q[j]==0)
       { 
        item[i][j]=0;
       }
   }
   }
System.out.println("\n ");
System.out.println("C2=\n "); 
int nt1[][]=new int[n1][n1];
 for(j=0;j<n1;j++) 
    {  for(m=j+1;m<n1;m++) 
       { for(i=0;i<n;i++)
         { if(item[i][j]==1 &&item[i][m]==1)
           { nt1[j][m]=nt1[j][m]+1;
           }
         }
    if(nt1[j][m]!=0)
         System.out.println("Number of Items of  "+itemlist[j]+" & "+itemlist[m]+" :"+nt1[j][m]);
    }
  
   }
System.out.println("\n "); 
System.out.println("L2=\n "); 
for(j=0;j<n1;j++)
{ for(m=j+1;m<n1;m++) 
  {
  if(nt1[j][m]>=ms)
    q[j]=1;
  else
   { q[j]=0;}

  if(q[j]==1)
   {
    System.out.println("Item "+itemlist[j]+" & "+itemlist[m]+" is selected "); 
   
   }
}
}
System.out.println("\n "); 

} 
}

//4 6 110110 001011 110001 000010''')
def print7():
	print('kmeans java \n')
	print('''import java.util.*;
class kmca
{
static int countk[];
static int d[];
static int k[][];
static int tempk[][];
static double m[];
static double diff[];
static int n,p,count=0;

static int cal_diff(int a) 
{
int temp1=0;
for(int i=0;i<p;++i)
{
if(a>m[i])
diff[i]=a-m[i];
else
diff[i]=m[i]-a;
}
int val=0;
double temp=diff[0];
for(int i=0;i<p;++i)
{
if(diff[i]<temp)
{
temp=diff[i];
val=i;
}
}
return val;
}

static void cal_mean() 
{
for(int i=0;i<p;++i)
m[i]=0; 
int cnt=0;
for(int i=0;i<p;++i)
{
cnt=0;
for(int j=0;j<n-1;++j)
{
if(k[i][j]!=-1)
{
m[i]+=k[i][j];
++cnt;
}}
m[i]=m[i]/cnt;
}
}

static int check1() 
{
for(int i=0;i<p;++i)
for(int j=0;j<n;++j)
if(tempk[i][j]!=k[i][j])
{
return 0;
}
return 1;
}

public static void main(String args[])
{
Scanner scr=new Scanner(System.in);

System.out.println("Enter the number of elements ");
n=scr.nextInt();
d=new int[n];

System.out.println("Enter "+n+" elements: ");
for(int i=0;i<n;++i)
d[i]=scr.nextInt();

System.out.println("Enter the number of clusters: ");
p=scr.nextInt();

k=new int[n][n];
tempk=new int[n][n];
m=new double[p];
diff=new double[p];
countk=new int[p];

for(int i=0;i<p;++i)
m[i]=d[i];

for(int k=0;k<p;++k)
{countk[k]=-1;}

int temp=0;
int flag=0;

do
{
for(int i=0;i<p;++i)
for(int j=0;j<n;++j)
{
k[i][j]=-1;
}

for(int i=0;i<n;++i) 
{
  for(int j=0;j<p;++j)
  {
    temp=cal_diff(d[i]);
    if (temp==j)
       k[temp][++(countk[j])]=d[i];
  }
}

cal_mean(); 
flag=check1(); 
if(flag!=1)
for(int i=0;i<p;++i)
for(int j=0;j<n;++j)
tempk[i][j]=k[i][j];

System.out.println("\n\nIteration : "+(++count));
System.out.println("\nValue of clusters");
for(int i=0;i<p;++i)
{
System.out.print("K"+(i+1)+"{ ");
for(int j=0;k[i][j]!=-1 && j<n-1;++j)
System.out.print(k[i][j]+" ");
System.out.println("}");
}
System.out.println("\nValue of m ");
for(int i=0;i<p;++i)
System.out.print("m"+(i+1)+"="+m[i]+"  ");

for(int k=0;k<p;++k)
  {countk[k]=-1;}

}
while(flag==0);

System.out.println("\n\n\nThe Final Clusters : ");
for(int i=0;i<p;++i)
{
System.out.print("K"+(i+1)+"{ ");
for(int j=0;k[i][j]!=-1 && j<n-1;++j)
System.out.print(k[i][j]+" ");
System.out.println("}");
}
}
}
''')
