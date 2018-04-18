# coding=utf-8
from gurobipy import *


# <editor-fold desc="step 0">
def stage_ini():
    m_ini=Model("m_ini")
    x1=m_ini.addVar(lb=40,vtype=GRB.CONTINUOUS,name="x1")
    x2=m_ini.addVar(lb=20,vtype=GRB.CONTINUOUS,name="x2")
    theta=m_ini.addVar(lb=-9999999,vtype=GRB.CONTINUOUS,name="theta")
    m_ini.update()
    m_ini.setObjective(100*x1+150*x2+theta,GRB.MINIMIZE)
    m_ini.update()
    m_ini.addConstr(x1+x2<=120,"c1")
    m_ini.optimize()
    x_ini=[]
    for v in m_ini.getVars():
        x_ini.append(v.x)
    obj_ini=m_ini.objVal
    return(obj_ini,x_ini)
# </editor-fold>

# print help(GRB.Attr)
#scenarios
E=[[500,100,-24,-28],[300,300,-28,-32]]
probability=[0.4,0.6]

# step 3
def stage2(solution1,x1):
    m21=Model("m21")
    y11=m21.addVar(lb=0,ub=E[0][0],vtype=GRB.CONTINUOUS,name="y11")
    y21=m21.addVar(lb=0,ub=E[0][1],vtype=GRB.CONTINUOUS,name="y21")
    m21.update()
    m21.setObjective(E[0][2]*y11+E[0][3]*y21,GRB.MINIMIZE)
    m21.update()
    m21.addConstr(6*y11+10*y21<=60*x1[0],"c1")
    m21.addConstr(8*y11+5*y21<=80*x1[1],"c2")
    m21.optimize()
    X21=[]
    for v in m21.getVars():
        X21.append(v.x)
    obj21=m21.objVal

    # ｇｒｏｕｂｉ获得对偶乘子的方法。
    P1=m21.getAttr("Pi",m21.getConstrs())
    for i in range(2):
        P1.append(m21.getAttr("rc",m21.getVars())[i])
    print(P1)
    print("hhhhhhhhhhhh")
    # constrs = m21.getConstrs()
    # for c in constrs:
    #     print c.ConstrName, c.Slack
    # print(m21.getAttr("rhs", m21.getConstrs()))
    # for d in m21.getVars():


    # print( X21,obj21,P1)


    m22=Model("m22")
    y1=m22.addVar(lb=0,ub=E[1][0],vtype=GRB.CONTINUOUS,name="y1")
    y2=m22.addVar(lb=0,ub=E[1][1],vtype=GRB.CONTINUOUS,name="y2")
    m22.update()
    m22.setObjective(E[1][2]*y1+E[1][3]*y2,GRB.MINIMIZE)
    m22.update()
    m22.addConstr(6*y1+10*y2<=60*x1[0],"c1")
    m22.addConstr(8*y1+5*y2<=80*x1[1],"c2")
    m22.optimize()
    X22=[]
    for v in m22.getVars():
        X22.append(v.x)
    obj22=m22.objVal
    P2=m22.getAttr("Pi",m22.getConstrs())
    print("kkkkkkkkkkkkkkkkkk")
    print(P2)
    for i in range(2):
        P2.append(m22.getAttr("rc",m22.getVars())[i])
    print(m22.getAttr("rc",m22.getVars()))
    # print( X22,obj22,P2)

    h1 = [0, 0, 500, 100]
    h2 = [0, 0, 300, 300]
    T = [[-60, 0, 0, 0],
         [0, -80, 0, 0]]

#e E w
    sume = 0
    for i in range(len(h1)):
        sume = (probability[0] * P1[i] * h1[i] + probability[1] * P2[i] * h2[i]) + sume
    e1 = sume

    sumt = [0, 0]
    for j in range(len(T)):
        for i in range(len(T[0])):
            sumt[j] = (probability[0] * P1[i] * T[j][i] + probability[1] * P2[i] * T[j][i]) + sumt[j]

    E1 = sumt
    EX = 0
    for i in range(len(x1)-1):
        EX = x1[i] * E1[i] + EX
    w = e1 - EX
    if w > x1[2]:
        return (E1, e1, w)
    else:
        print("_____________stage 2______________")
        print("stage 2 E:", E1)
        print("stage 2 e:", e1)
        print("stage 2 w:", w)
        print("STOP! the optimal solution is : ")
        print(x1)


def stage1(E1,e,w):
    m1 = Model("m1")
    x1 = m1.addVar(lb=40, vtype=GRB.CONTINUOUS, name="x1")
    x2 = m1.addVar(lb=20, vtype=GRB.CONTINUOUS, name="x2")
    theta = m1.addVar(lb=-9999999, vtype=GRB.CONTINUOUS, name="theta")
    m1.update()
    m1.setObjective(100 * x1 + 150 * x2 + theta, GRB.MINIMIZE)
    m1.update()
    m1.addConstr(x1 + x2 <= 120, "c1")
    for i in range(len(E1)):
        m1.addConstr(E1[i][0]*x1 + E1[i][1]*x2 + theta >= e[i], "c1")
    m1.optimize()
    x1 = []
    for v in m1.getVars():
        x1.append(v.x)
    obj1 = m1.objVal
    return (obj1,x1)



#Iteration
_solution=[]
_x=[]
_solution.append(stage_ini()[0])
_x.append(stage_ini()[1])
print("_____________stage_ini______________")
print("stage_ini solution:", _solution)
print("stage_ini x:", _x)
_e1=[]
_E1=[]
_w1=[]
Con=[]
Con2=[]
for v in range(4):
    print("_________________________Iteration count:",v,"_________________________" )
    Con=stage2(_solution[v],_x[v])
    _E1.append(Con[0])
    _e1.append(Con[1])
    _w1.append(Con[2])
    print("_____________stage 2______________")
    print("stage 2 E:", _E1)
    print("stage 2 e:", _e1)
    print("stage 2 w:", _w1)
    Con2=stage1(_E1,_e1,_w1[v])
    _solution.append(Con2[0])
    _x.append(Con2[1])
    print("_____________stage 1______________")
    print("stage 1 solution:", _solution[v])
    print("stage 1 x:", _x[v])
    v = v + 1