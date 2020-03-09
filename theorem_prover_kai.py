class Formula:
  def __init__(self , name , value = False , flag = 0):
    self.name = name
    self.value = value
    self.flag = flag
    self.left = None
    self.right = None


  def eval(self):
    if self.left == None and self.right == None :
      if self.flag == 1:
        return (not self.value)
      else:
        return self.value
    else:
      if self.name == '|' :
        return (self.left.eval() or self.right.eval())
      elif self.name == '&' :
        return (self.left.eval() and self.right.eval())
      elif self.name == '=>' :
        return imply(self.left.eval() , self.right.eval())
      elif self.name == '<=>' :
        return bimply(self.left.eval() , self.right.eval())
      else :
        return 'Error symbol not recognized in the function'

def imply(a,b):
  if a and (not b):
    return False
  else:
    return True

def bimply(a,b):
  if imply(a,b) and imply(b,a):
    return True
  else:
    return False


def find_leaf_nodes_1(tree):
  leaf_nodes = [] 
  def find_leaf_nodes(tree):
    for i in [tree.left , tree.right] :
      if i.left == None and i.right == None:
        leaf_nodes.append(i)
      else:
        find_leaf_nodes(i)
    return leaf_nodes
  if tree.left == None and tree.right == None :
    y = [tree]
  else:  
    y = find_leaf_nodes(tree)
  return y

def check_outer_brackets(expression):
  D= {}
  D['('] = 0
  D[')'] = 0
  if expression[0] != '(':
    return False
  else:
    for i in range(len(expression)):
      if expression[i] == "(":
        D['('] = D['('] + 1
      if expression[i] == ")":
        D[')'] = D[')'] + 1
      if D['('] == D[')']:
        break
    if i == len(expression) - 1:
      return True
    else:
      return False

def seperator(expression):
  term = []
  if check_outer_brackets(expression):
    expression = expression[1:-1]
  if expression[0] == '(':
    D = {}
    D['('] = 0
    D[')'] = 0
    for i in range(len(expression)):
      if expression[i] == "(":
        D['('] = D['('] + 1
      if expression[i] == ')':
        D[')'] = D[')'] + 1
      if D[')'] == D['(']:
        break
    term.append(expression[:i+1])
    if expression[i+2] == "|" or expression[i+2] == "&" :
      term.append(expression[i+2])
      term.append(expression[i+4:])
    elif expression[i+2] == "=":
      term.append(expression[i+2:i+4])
      term.append(expression[i+5:])
    elif expression[i+2] == "<":
      term.append(expression[i+2:i+5])
      term.append(expression[i+6:])
  else:
    for i in range(len(expression)):
      if expression[i] == "|" or expression[i] == "&" :
        term.append(expression[:i-1])
        term.append(expression[i])
        term.append(expression[i+2:])
        break
      elif expression[i] == "=":
        term.append(expression[:i-1])
        term.append(expression[i:i+2])
        term.append(expression[i+3:])
        break
      elif expression[i] == "<":
        term.append(expression[:i-1])
        term.append(expression[i:i+3])
        term.append(expression[i+4:])
        break
  return term


def check_if_literal(expression):
  flag = 0
  for i in expression:
    if i == " ":
      flag = flag + 1
  if flag == 0:
    return True
  else:
    return False

def make_tree(node , expression):
  terms = seperator(expression)
  if terms:
    if check_if_literal(terms[0]) and check_if_literal(terms[2]):
      node.name = terms[1]
      x = Formula(terms[0])
      y = Formula(terms[2])
      if terms[0][0] == "~":
        x.flag = 1
        x.name = x.name[1:]
      if terms[2][0] == "~":
        y.flag = 1
        y.name = y.name[1:]
      node.left = x
      node.right = y
      return node

    else:
      node.name = terms[1]
      if check_if_literal(terms[0]):
        x = Formula(terms[0])
        if terms[0][0] == "~":
          x.flag = 1
          x.name = x.name[1:]
        node.left = x
      else:
        x = Formula('Null')
        node.left = make_tree(x , terms[0])
      
      if check_if_literal(terms[2]):
        y = Formula(terms[2])
        if terms[2][0] == "~":
          y.flag = 1
          y.name = y.name[1:]
        node.right = y 
      else:
        y = Formula('Null')
        node.right = make_tree(y , terms[2])
  else:
    node.name = expression
    if expression[0] == "~":
      node.flag = 1
      node.name = node.name[1:]

  return node


def binary(length):
  ts = []
  number = 2**length - 2 
  flag = [0]*length
  count = 1
  sumi = 0
  ss = []
  for i in range(length):
    ss.append(2**(i+1))
  while sumi < number:
    sumi = 0
    for i in range(len(flag)):
      sumi = sumi + (2**(len(flag) - 1 -i))*flag[i]
    for i in range(len(ss)):
      if count%ss[i] < int((ss[i]/2)) + 1 and count%ss[i] > 0:
        flag[length- i - 1] = 0
      else:
        flag[length - i - 1] = 1
    flag1 = flag[:]
    ts.append(flag1)
    count = count + 1
  return ts

def number_unique_leaf_nodes(list_nodes):
  D = {}
  for i in list_nodes:
    D[i.name] = 0
  for i in list_nodes:
    D[i.name] = D[i.name] + 1
  count = 0
  return len(D.keys())

def binary(length):
  ts = []
  number = 2**length - 2 
  flag = [0]*length
  count = 1
  sumi = 0
  ss = []
  for i in range(length):
    ss.append(2**(i+1))
  while sumi < number:
    sumi = 0
    for i in range(len(flag)):
      sumi = sumi + (2**(len(flag) - 1 -i))*flag[i]
    for i in range(len(ss)):
      if count%ss[i] < int((ss[i]/2)) + 1 and count%ss[i] > 0:
        flag[length- i - 1] = 0
      else:
        flag[length - i - 1] = 1
    flag1 = flag[:]
    ts.append(flag1)
    count = count + 1
  for i in range(len(ts)):
    for j in range(length):
      if ts[i][j] == 0:
        ts[i][j] = False
      else:
        ts[i][j] = True
  return ts

def assign(dicti , list_values):
  i = 0
  for k in dicti.keys():
    dicti[k] = list_values[i]
    i = i + 1
  return dicti

def collect_all_nodes(KB):
  D = {}
  for i in KB:
    x = find_leaf_nodes_1(i)
    for k in x:
      D[k.name] = 'There'
  return D

def assign_to_formula(dicti , formula):
  y = find_leaf_nodes_1(formula)
  for i in y:
    i.value = dicti[i.name]

def truth_table_enumeration(KB , conclusion):
  list_formulas = []

  check1 = 0 
  check2 = 0
  length = len(KB)
  for i in KB:
    tree = Formula('Null')
    list_formulas.append(make_tree(tree , i))
  tree = Formula('Null')
  formula_conclusion = make_tree(tree , conclusion)
  doct = collect_all_nodes(list_formulas + [formula_conclusion])
  list_of_models = binary(len(doct.keys()))
  for i in list_of_models:
    y = assign(doct , i)
    count = 0
    for j in list_formulas:
      assign_to_formula(y , j)
      if j.eval() == True:
        count = count + 1
    if count == length :
      check1 = check1 + 1
      assign_to_formula(y , formula_conclusion)
      if formula_conclusion.eval() == True:
        check2 = check2 + 1
  if check2 == 0:
    return 'False'
  elif check1 > check2 : 
    return 'Maybe'
  elif check1 == check2 :
    return 'True'


def remove_ands(expression):
  l = []
  i = 0
  for k in range(len(expression)):
    if expression[k] == '&':
      l.append(expression[i:k-1])
      i = k+2
  l.append(expression[i:])
  return l

def make_seperate_clauses(KB):
  K = []
  for i in KB:
    count = 0
    for j in i:
      if j == '&':
        count = count + 1
    if count == 0:
      K.append(i)
    else:
      l = remove_ands(i)
      K = K + l
  return K

def factor(tree):
  list1 = find_leaf_nodes_1(tree)
  list3 = []
  for i in range(len(list1)):
    for j in range(i+1 , len(list1)):
      if list1[i].name == list1[j].name and list1[i].flag == list1[j].flag:
        if list1[j] not in list3:
          list3.append(list1[j])
      elif list1[i].name == list1[j].name and list1[i].flag + list1[j].flag == 1:
        return Formula('MUZAN')

  def dfs(tree , node):
    if tree == None:
      return
    elif tree.right == None or tree.right.left == None or tree.right.right == None:
      pass
    elif tree.right.right == node:
      tree.right = tree.right.left
    elif tree.right.left == node:
      tree.right = tree.right.right
    dfs(tree.right , node)
    return tree
    

  if list3 == []:
    return tree
  for i in list3:
    tree = dfs(tree , i)

  if tree.left.name == tree.right.name and tree.left.flag == tree.right.flag:
    return tree.left
  else: 
    return tree

def resolve(formula1 , formula2) :
  list1 = find_leaf_nodes_1(formula1)
  list2 = find_leaf_nodes_1(formula2)
  count = 0
  #if list1 == None or list2 == None:
  #  return Formula('MUZAN')
  for i in list1:
    for j in list2:
      if i.name == j.name and i.flag + j.flag == 1 :
        count = count + 1
        break
    if i.name == j.name and i.flag + j.flag == 1 :
      break
  if count == 0:
    return False
  node1 = i
  node2 = j

  def prune(tree , node):
    tree1 = tree
    count = 0
    while count == 0:
      if tree == None:
        break
      elif tree.right == None or tree.right.left == None or tree.right.left == None:
        pass
      elif tree.right.left == node:
        tree.right = tree.right.right
        count = count + 1
      elif tree.right.right == node:
        tree.right = tree.right.left
        count = count + 1
      tree = tree.right
    return tree1
  flag = 0

  if formula1 == node1:
    a = Formula('Null')
  elif formula1.left == node1:
    a = formula1.right
    flag = 1
  elif formula1.right == node1:
    a = formula1.left
    flag = 1
  else:
    a = prune(formula1 , node1)

  if formula2 == node2:
    b = Formula('Null')
  elif formula2.left == node2:
    b = formula2.right
  elif formula2.right == node2:
    b = formula2.left
  else:
    b = prune(formula2 , node2)

  

  x = Formula('|')
  x.right = b
  if a.name == 'Null' or flag == 1:
    x.left = a
    return x
  else:
    return find_rightmost_node(a , x)



def print_tree(tree):
  list1 = find_leaf_nodes_1(tree)
  for i in list1:
    print(i.name , i.flag)
def find_rightmost_node(tree , y):
  count = 0
  tree1 = tree
  while count == 0:
    if tree.right.right == None:
      y.left = tree.right
      tree.right = y
      count = count + 1
    else:
      tree = tree.right
  return tree1


def are_they_equal(formula1 , formula2):
  if formula2 == None:
    return False
  if not formula1:
    return False
  list1 = find_leaf_nodes_1(formula1)
  list2 = find_leaf_nodes_1(formula2)
  count = 0
  if len(list1) != len(list2):
    return False
  for i in list1:
    for j in list2:
      if i.name == j.name and i.flag == j.flag:
        count = count + 1
  if count == len(list1):
    return True
  else:
    return False

def resolution(KB , conclusion):
  K = make_seperate_clauses(KB)
  #K.append("~" + conclusion)
  formulas = []
  count1 = 0
  count = 0
  for i in K:
    treex = Formula('Null')
    formulas.append(make_tree(treex , i))
  treey = Formula('Null')
  new = [make_tree(treey , "~" + conclusion)]
  for i in new:
    for j in formulas:
      output = resolve(factor(i),factor(j))
      count = 0
      if output == False:
        continue
      output = factor(output)
      if output.name == 'MUZAN':
        continue
      for k in formulas:
        if are_they_equal(output , k):
          count = count + 1
          break
      if count == 0 and output.name != 'MUZAN':
        new.append(output)
        formulas.append(output)
      count1 = 0
      
      for mm in find_leaf_nodes_1(output):
        if mm.name == 'Null':
          count1 = count1 + 1
      if count1 == len(find_leaf_nodes_1(output)):
        return "Empty Clause Found"
  return "No Empty Clause Found"

  
print("Modus Ponens Test")
print("Knowledge Base :")
KB = ['~P | Q' , 'P']
conclusion = 'Q'
for i in KB:
	print(i)
print("Query:")
print(conclusion)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion)))
print("\n\n")

print("Wumpus World Test")
print("Knowledge Base :")
KB = ['~P11' , '~B11 | (P12 | P21) & (B11 | ~P12) & (B11 | ~P21)' , '(~B21 | P11 | P22 | P31) & (B21 | ~P11) & (B21 | ~P22) & (B21 | ~P31)' , '~B11' , 'B21']
conclusion = 'P12'
for i in KB:
	print(i)
print("Query:")
print(conclusion)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion)))
print("\n\n")

print("Horn Clause Test")
print("Knowledge Base :")
KB = ['~My | Im' , '(My | Mo) & (My | Ma)' , '(~Im | Ho) & (Ho | ~Ma)' , '~Ho | Ma']
conclusion1 = "My"
conclusion2 = "Ma"
conclusion3 = "Ho"
for i in KB:
	print(i)
print("For Query1:")
print(conclusion1)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion1)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion1)))
print("For Query2:")
print(conclusion2)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion2)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion2)))
print("For Query3:")
print(conclusion3)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion3)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion3)))
print("\n\n")

print("Doors of Enlightenment : Smulliyan's Problem")
print("Knowledge Base :")
KB = ['(~A | X) & (A | ~X)' , '(~B | Y | Z) & (B | ~Y) & (B | ~Z)' , '(~C | A) & (~C | B) & (C | ~A | ~B)' , '(~D | X) & (~D | Y) & (D | ~X | ~Y)' , '(~E | X) & (~E | Z) & (E | ~X | ~Z)' , '(~F | D | E) & (F | ~D) & (F | ~E)' , '(~G | ~C | F) & (G | C) & (G | ~F)' , '(~H | ~G | ~H | A) & (H | G) & (H | H) & (H | ~A)']
conclusion1 = 'X'
conclusion2 = 'Y'
conclusion3 = 'Z'
for i in KB:
	print(i)
print("For Query1:")
print(conclusion1)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion1)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion1)))
print("For Query2:")
print(conclusion2)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion2)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion2)))
print("For Query3:")
print(conclusion3)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion3)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion3)))
print("\n\n")

print("Doors of Enlightenment : Liu's Problem")
print("Knowledge Base :")
KB = ['(~A | X) & (A | ~X)' ,  '(~C | A) & (C | ~A)' , '(~G | ~C | Fdf) & (G | C) & (G | ~Fdf)' , '(~H | ~G | ~H | A) & (H | G) & (H | H) & (H | ~A)']
conclusion1 = 'X'
conclusion2 = 'Y'
conclusion3 = 'Z'
for i in KB:
	print(i)
print("For Query1:")
print(conclusion1)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion1)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion1)))
print("For Query2:")
print(conclusion2)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion2)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion2)))
print("For Query3:")
print(conclusion3)
print("Ans with model checking : {}".format(truth_table_enumeration(KB , conclusion3)))
print("Ans with Resolution : {}".format(resolution(KB , conclusion3)))
print("\n\n")
