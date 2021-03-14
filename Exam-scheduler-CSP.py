#!/usr/bin/env python
# coding: utf-8
# Author : Ghadeer Abualrub
# # Code skeleton
# the code designed based on OOP
# 
# 3 classes :
#     * exam
#     * constraints
#     * CSPsolver
# 
# 2 enumerations :
#     * time_slots : ordered enumeration 
#     * constraintsType : 4 type of constraints >> same_value, before, after, hall
# 
# CSP solution : based on backtracking technique with ordering improvment using most constrained variable 

# In[112]:


from enum import Enum





'''
Enumeration of constraints type

same_value: two exams at same time and in same hall
before: examA before examB 
after: examA after examB
hall: examA in certain hall
'''
class constraintsType(Enum):
    same_value = 0
    before = 1
    after = 2
    hall = 3


# In[114]:



'''
class that inherits Enum and override logical operation (<=,>=,<,>)
'''
class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

'''
Enumeration of time slots in ascending order, that inherits orderedEnum to use  
logical operations in comperison 
t1 < t2 < t3 < t4
'''
# formulate time slots as orderd enumeration     
class time_slot(OrderedEnum):
    t1 = 0
    t2 = 1
    t3 = 2
    t4 = 3


# In[ ]:





# In[115]:


'''
class exam: to represent exam information
name: exam name {E1, E2, E3, ..., E10}
time: exam time slot {t1, t2, t3, t4}
place: exam hall
value: a tuple that contains time and place of exam
'''
class exam:
    def __init__(self, name, time=None, place=None):
        self.name = name
        self.time = time
        self.place = place
        if time and place:
            self.value = tuple([self.time, self.place])
        else:
            self.value = ()
        
    def isAssigned(self):
        '''
        check if the exam is assigned or not 
        '''
        if len(self.value) == 0:
            return False
        return True
    
    def assignValue(self, time, place):
        '''
        set time and hall of exam 
        '''
        self.value = tuple([time, place])
        self.time = time
        self.place = place 
        
    def assignTupleValue(self, value):
        '''
        set and assigned value of exam to a tuple of time and hall
        '''
        self.value = value
        self.time = value[0]
        self.place = value[1]
        
    def getExamInfo(self):
        '''
        get exam information as string
        '''
        str1 = ''
        str1 += self.name
        if self.isAssigned():
            str1 +=  ': (' + self.value[0].name +', '+ self.value[1] + ')'
        else: 
            str1 += ':()'
        return str1
    


# In[ ]:





# In[116]:



'''
constraints class: represnt constraints satisfaction 

constraints: dictionery of constraints, the key is the name of the exam{E1, E2, E3, ..., E10}
and the value is a list of constraints type of the exam

if the constraint is of type before, after or hall, then the value of the dictionery will be a 
dictionery >> its key is the type of constraints and it value a list of exams or halls.
'''
class constraints:
    def __init__(self):
        self.constraints = dict() #dict(key,value) key = variable name, value = list of constraints
        
    def prepareConstForVariable(self, variableName, constList):
        '''
        assigned each variable to its constraints 
        and add the constrainte to the self.constraints dictionary
        '''
        self.constraints[variableName] = constList
        

    def getMostConstrainedVar(self, unassignedVar):
        '''
        get an unassigned variable which has most constraints 
        return the name of the variable from unassigned and is the most constrained
        '''
        count = -1
        variable = ''
        for k in unassignedVar.keys():
            if len(self.constraints[k]) > count:
                count = len(self.constraints[k])
                variable = k
        return variable # name of the variable : string 
        
        
    def satisfy(self, variable, assignedVariables):
        '''
        check if the value of the variable staisfy constraints or not 
        '''
        #variable of type exam
        consistent = True 
        
        for const in self.constraints[variable.name]:
            if const == constraintsType.same_value:
                # no two exams have the sam place and time
                if len(assignedVariables) != 0:
                    for var in assignedVariables.values():
                        if variable.value == var.value:
                            print('this assignment is not consistent, two variable have same value')
                            consistent = False
                            break
            # check before, after, and hall constraints
            if type(const) == dict:
                if constraintsType.before in const.keys(): # before constraints
                    vars = const[constraintsType.before]
                    # check if the exam time is greater or equal to the corresponding exams
                    for v in vars:
                        if v in assignedVariables.keys():
                            if variable.time >= assignedVariables[v].time:
                                consistent = False
                                print('inconsistent before constraints')
                                break
                                
                if constraintsType.after in const.keys(): # after constraints
                    vars = const[constraintsType.after]
                    # check if the exam time is less or equal to the corresponding exams
                    for v in vars:
                        if v in assignedVariables.keys():
                            if variable.time <= assignedVariables[v].time:
                                consistent = False
                                print('inconsistent after constraints')
                                break
                # check if the exam is in the correct hall or not                
                if constraintsType.hall in const.keys():  # hall constraints
                    vars = const[constraintsType.hall]
                    if variable.place not in vars:
                            consistent = False
                            print('inconsistent Hall constraints')
        
        return consistent


# In[ ]:





# In[117]:


'''
CSPsolver:
class represent solver using the backtracking technique and ordering as which variable should 
be assigned next according to the number of constraints that the variable have 

assignments: dictionery of assigned variables, key: exam name, value: exam object
variables: list of variables (exams) 
domain: domains for variables which are list of tuples of (time, hall)
constraints: dictionery of constraints (variable name: variable)
unassignedVar: dictionery of unassigned varibales (variable name: variable)

'''

class CSPsolver:
    
    def __init__(self, variables, domain, constraints):
        self.assignments = dict() #dictionary {exam name : exam object}
        self.variables = variables #list of exams 
        self.domain = domain #domain list
        self.constraints = constraints  #constraints object which have a dictionary of constraints
        self.unassignedVar = dict() #dictionary {exam name : exam object}
        
        # filling the unassignedVar key with the name of variables 
        for var in self.variables:
            self.unassignedVar[var.name] = ''
    
    def selectUnAssignedVariable(self):
        '''
        select an unassigned variable which is the most constrained variable
        return the name of the variable, to get it from the dictionary after that
        '''
        return self.constraints.getMostConstrainedVar(self.unassignedVar)
         

    '''
    backtracking technique to solve exam scheduler with ordering as improvement, 
    using the most constrained variable first
    '''
    def backtrackingSearchWithOrdering(self):
        return self.recursiveBacktracking()
    
    def recursiveBacktracking(self):
        
        #if number of assignments the same as number of variables >> we have assigned all exams
        if len(self.assignments.keys()) == len(self.variables):
            return self.assignments
        
        #select variable to be assigned >> unassigned and most constrainted variable
        variableName = self.selectUnAssignedVariable()
        variable = exam(variableName) # object of class exam, to generate new assignment
        
        #loop on all values we can assigned with
        for value in self.domain:
            #assign variable to value
            variable.assignTupleValue(value)
            #check constraints for the variable with this value
            if self.constraints.satisfy(variable, self.assignments):
                # if consistent add the assignment and remove the variable from unassigned dictionary
                self.assignments[variableName] = variable
                self.unassignedVar.pop(variableName)
                result = self.recursiveBacktracking()
                
                if result is not None:
                    return result
        
        return None


# # Scheduling Exams

# In[118]:



'''
define all exams with thier names, empty time slot and place entries
'''
exams = []
for i in range(0,10):
    ex = exam('E'+str(i+1))
    exams.append(ex)

# define constraintType     
T = constraintsType

# define constraints object 
const = constraints() 

# add constraints for variables to the const object
const.prepareConstForVariable('E1',[T.same_value, {T.before:['E3']}, {T.hall:['A','C']}])
const.prepareConstForVariable('E2',[T.same_value])
const.prepareConstForVariable('E3',[T.same_value, {T.after:['E1']}, {T.hall:['A','C']}])
const.prepareConstForVariable('E4',[T.same_value, {T.before:['E10']}, {T.hall:['A','C']}])
const.prepareConstForVariable('E5',[T.same_value])
const.prepareConstForVariable('E6',[T.same_value])
const.prepareConstForVariable('E7',[T.same_value, {T.hall:['A','B']}])
const.prepareConstForVariable('E8',[T.same_value, {T.hall:['A','B']}])
const.prepareConstForVariable('E9',[T.same_value, {T.before:['E10']}, {T.hall:['A','B']}])
const.prepareConstForVariable('E10',[T.same_value, {T.after:['E4','E9']}, {T.hall:['A','B']}])

'''
define exams domains with time slots and halls 
like:
(time_slot.t1,'A')
'''
domain = []

for t in time_slot:
    for h in ['A','B','C']:
        domain.append(tuple([t,h])) 

# define solver object that will take exams list, domain list, constraints object        
solver = CSPsolver(exams, domain, const)

# run backtrackingSearch() function to get the solution
assignments = solver.backtrackingSearchWithOrdering()

# print solution 
print('\n----------------------------------------------------------------------------')
if assignments:
    print('\n*** Exams Schedule *** \n')
    for exam in assignments.values():
        print(exam.getExamInfo())
else:
    print('\nNo solution found\n')


# In[ ]:





# In[ ]:





# In[ ]:




