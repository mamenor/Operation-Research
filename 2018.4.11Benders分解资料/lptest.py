#coding=utf-8
from __future__ import print_function
import cplex
from cplex.exceptions import CplexError


# <editor-fold desc="step 0">
r=0
_s=0
v=0

def popbyrow(prob,my_obj,my_lb,my_ub,my_colnames,my_rhs,my_rownames,my_rows,my_sense):
    prob.objective.set_sense(prob.objective.sense.minimize)
    prob.variables.add(obj=my_obj, lb=my_lb,ub=my_ub, names=my_colnames)
    prob.linear_constraints.add(lin_expr=my_rows, senses=my_sense, rhs=my_rhs, names=my_rownames)

my_obj = [100, 150, 1]
my_lb = [40, 20, -9999999]
my_ub = [cplex.infinity, cplex.infinity, cplex.infinity]
my_colnames = ["x1", "x2", "theta"]
my_rhs = [120]
my_rownames = ["c1"]
my_sense = "L"
my_rows = [[["x1", "x2", "theta"], [1, 1, 0]]]
# </editor-fold>

# <editor-fold desc="step 1 ini">
def stage_ini( ):
    my_prob = cplex.Cplex()
    popbyrow(my_prob,my_obj,my_lb,my_ub,my_colnames,my_rhs,my_rownames,my_rows,my_sense)
    my_prob.solve()
    solution=my_prob.solution.get_objective_value()
    x = my_prob.solution.get_values()
    pi = my_prob.solution.get_dual_values()
    return (solution,x)
# </editor-fold>

#scenarios
E=[[500,100,-24,-28],[300,300,-28,-32]]
probability=[0.4,0.6]

# <editor-fold desc="step 3">
def stage2(solution1,x1):
    my_lb2=[0,0]
    my_colnames2=["y1","y2"]
    my_rhs2=[60*x1[0],80*x1[1]]
    my_rownames2=["c1","c2"]
    my_sense2="LL"
    my_rows2 = [[["y1", "y2"], [6, 10]],
            [["y1", "y2"], [8, 5]]]
    h1=[0,0,500,100]
    h2=[0,0,300,300]
    T=[[-60,0,0,0],
       [0,-80,0,0]]
    PP=[]

    # number of scenarios = 2
    for i in range(2):
        my_ub2=[E[i][0],E[i][1]]
        my_obj2=[E[i][2],E[i][3]]
        P=[]
        my_prob = cplex.Cplex()
        popbyrow(my_prob,my_obj2,my_lb2,my_ub2,my_colnames2,my_rhs2,my_rownames2,my_rows2,my_sense2)
        my_prob.solve()
        solution=my_prob.solution.get_objective_value()
        pi = my_prob.solution.get_dual_values()
        x = my_prob.solution.get_values()
        dj = my_prob.solution.get_reduced_costs()
        print("~~~~~~~~~~~~~pi:", pi)
        print("~~~~~~~~~~~~dj:", dj)

        # python： the　ｄｉｆｆｅｒｅｎｃｅ　ｂｅｔｗｅｅｎ　ｅｘｔｅｎｄ　ａｎｄ　ａｐｐｅｎｄ
        for j in range(len(pi)):
            P.append(pi[j])
        for j in range(len(dj)):
            P.append(dj[j])
        PP.append(P)
#求e E w
    sume=0
    for i in range(len(h1)):
        sume=(probability[0] * PP[0][i] * h1[i] + probability[1] * PP[1][i] * h2[i])+sume
    e1=sume

    sumt=[0,0]
    for j in range(len(T)):
        for i in range(len(T[0])):
            sumt[j]=(probability[0] * PP[0][i] * T[j][i] + probability[1] * PP[1][i] * T[j][i])+sumt[j]

    E1=sumt
    EX=0
    for i in range(len(x1)-1):
        EX=x1[i]*E1[i]+EX
    w=e1-EX

    #theta=x1[2]
    if w>x1[2]:
        return(E1,e1,w)
    else:
        print("STOP！the optimal solution is : ")
        print(x1)
# </editor-fold>

# <editor-fold desc="step 1">
def stage1(_E1,_e1,_w1):
    my_obj = [100, 150, 1]
    my_lb = [40, 20, -99999]
    my_ub = [cplex.infinity, cplex.infinity, cplex.infinity]
    my_colnames = ["x1", "x2", "theta"]
    my_rhs = [120]
    my_rownames = ["c1"]
    my_rows = [[["x1", "x2", "theta"], [1, 1, 0]]]
    my_sense = "L"
    for i in range(len(_E1)):
        # Ｅ１存的只是ｘ１ｘ２的系数，ａｐｐｅｎｄ１是ｔｈｅｔａ的系数。
        _E1[i].append(1)
        my_rownames.append("c")
        my_sense = my_sense+"G"
        my_rows.append([["x1", "x2", "theta"],_E1[i]])
        my_rhs.append(_e1[i])

    my_prob = cplex.Cplex()
    popbyrow(my_prob,my_obj,my_lb,my_ub,my_colnames,my_rhs,my_rownames,my_rows,my_sense)
    my_prob.solve()
    solution=my_prob.solution.get_objective_value()
    x = my_prob.solution.get_values()
    return (solution,x)
# </editor-fold>




# <editor-fold desc="Iteration">
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
    print("—————————Iteration count:",v,"———————————" )
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
# </editor-fold>






