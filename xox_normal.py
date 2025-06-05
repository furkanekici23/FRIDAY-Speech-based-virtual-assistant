import random as rd
import os
def xox() :
    global player,computer 
player=''
computer=' '

def clr() :
 cl=input("\nPress enter to clear the page and end the game.")
 os.system('cls' if os.name == 'nt' else 'clear')

matrix = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

def show_matrix():
 for row in matrix:
     print(" ".join(row))
 print("\n")

def pick_side():
 global player,computer
 while True:
  side=input("\nPlease pick a side: X or O ? ")
  if side== 'X' or side== 'x':
    player = 'X'
    computer ='O'
    break
  elif  side== 'O' or side == 'o':
   player = 'O' 
   computer='X'
   break 
  else:
   print("You didn't pick neither 'x' or 'o'")
   continue
  
def control_space(x,y):
  if matrix [x][y] == '-' :
     return True
  else :
    return False
  
def move():
  global player
  print("Please type the row and column numbers which you wish to make a  respectively")
  print("(For example,type '12' to make a move on 1st row and 2nd column)")
  while True:
   m=input("Your move: ")
   list_m=['11','12','13','21','22','23','31','32','33']
   if m in list_m :
    row=int(m[0])-1
    column=int(m[1])-1
    if control_space(row,column) == True:
     matrix[row][column] = player
     break
    else:
     print("The place you are trying to make a move on is already filled,please make another move.")
     continue
   else:
    print("Your input is invalid ! Please try again to make a valid move.")
    continue
def computer_random_move():
  global computer
  def nm():
    number=[0,1,2]
    return int(rd.choice(number))
  while True:
   row=nm()
   column=nm()
   if control_space(row,column) == True:
     matrix[row][column] = computer
     break
   else:
     continue

def computer_move():
  global computer
  print("Computer made a move :")
  a=b=c=0
  cntrl=0
  #controling rows 
  #Firstly controling for winning
  for row in range (len(matrix)):
    a=matrix[row][0]
    b=matrix[row][1]
    c=matrix[row][2]
    if (a=='-' or b=='-' or c== '-') and cntrl ==0 :
      if a==b==computer  :
        matrix[row][2] = computer
        cntrl=1
      elif a==c==computer :
        matrix[row][1] = computer
        cntrl=1
      elif b==c==computer  :
        matrix[row][0] = computer
        cntrl=1
  #Secondly controling for blocking
  for row in range (len(matrix)):
    a=matrix[row][0]
    b=matrix[row][1]
    c=matrix[row][2]
    if (a=='-' or b=='-' or c== '-') and cntrl ==0 :
      if a==b==player  :
        matrix[row][2] = computer
        cntrl=1
      elif a==c==player :
        matrix[row][1] = computer
        cntrl=1
      elif b==c==player  :
        matrix[row][0] = computer
        cntrl=1
      
  #controling columns 
  if cntrl==0:
    #Firstly controling for winning
    for col in range(3):  
        a=matrix[0][col] 
        b=matrix[1][col] 
        c=matrix[2][col]
        if (a=='-' or b=='-' or c== '-') and cntrl ==0 :
         if a==b==computer  :
          matrix[2][col] = computer
          cntrl=1
         elif a==c==computer :
           matrix[1][col] = computer
           cntrl=1
         elif b==c==computer  :
           matrix[0][col] = computer
           cntrl=1
    #Secondly controling for blocking
    for col in range(3):  
        a=matrix[0][col] 
        b=matrix[1][col] 
        c=matrix[2][col]
        if (a=='-' or b=='-' or c== '-') and cntrl ==0 :
         if a==b==player  :
          matrix[2][col] = computer
          cntrl=1
         elif a==c==player :
           matrix[1][col] = computer
           cntrl=1
         elif b==c==player  :
           matrix[0][col] = computer
           cntrl=1

  #controling crosses 
  a=matrix[0][0]  
  b=matrix[0][2]
  c=matrix[1][1]
  d=matrix[2][0]
  e=matrix[2][2]
  if cntrl==0:
   if a==c and a != '-' and e=='-' :
     matrix[2][2]=computer
     cntrl = 1
   elif a==e and a != '-' and c=='-' :
     matrix[1][1]=computer
     cntrl = 1
   elif c==e and c != '-' and a=='-' :
     matrix[0][0]=computer 
     cntrl = 1
  
  if cntrl==0:
   if b==c and b != '-' and d=='-' :
     matrix[2][0]=computer
     cntrl = 1
   elif b==d and b != '-' and c=='-' :
     matrix[1][1]=computer
     cntrl = 1
   elif c==d and c!= '-' and b=='-' :
     matrix[0][2]=computer
     cntrl = 1  

  #if there is no trivial winning move or a trivial blocking move, computer just plays a random move      
  if cntrl==0:
    computer_random_move()  
        
    
def is_table_full():
 exists = any('-' in row for row in matrix)
 if exists:
  return False  
 else:
   return True
 

def full_row():
  for row in matrix:
    if all(cell == row[0] for cell in row) and  row[0] != '-':  
        return True
  return False

def full_column():
    for col in range(3):  
        if matrix[0][col] == matrix[1][col] == matrix[2][col] and matrix[0][col] != "-":
            return True
    return False

def game_over():
 if full_row()== True :
  return True
  
 elif full_column()== True :
  return True
  
 elif matrix[0][0]== matrix[1][1]== matrix[2][2] != '-':
  return True
 elif matrix[0][2]== matrix[1][1]== matrix[2][0] !='-' :
  return True
 else:
   return False
 
def who_won():
 #controling rows
 for row in matrix:
    if all(cell == row[0] for cell in row) and  row[0] == 'X':  
        print("X HAS WON THE GAME!")
        
    elif all(cell == row[0] for cell in row) and  row[0] == 'O':  
        print("O HAS WON THE GAME!")
        
 #controling columns
 for col in range(3):  
        if matrix[0][col] == matrix[1][col] == matrix[2][col] and matrix[0][col] == "X":
          print("X HAS WON THE GAME!")
          
        elif matrix[0][col] == matrix[1][col] == matrix[2][col] and matrix[0][col] == "O":
          print("O HAS WON THE GAME!")

 #controling crosses
 if matrix[0][0]== matrix[1][1]== matrix[2][2] == 'X':
   print("X HAS WON THE GAME!")
   
 elif matrix[0][0]== matrix[1][1]== matrix[2][2] == 'O':
   print("O HAS WON THE GAME!")
   
  
 if matrix[0][2]== matrix[1][1]== matrix[2][0] =='X' :
   print("X HAS WON THE GAME!")
   
 elif matrix[0][2]== matrix[1][1]== matrix[2][0] =='O' :
   print("O HAS WON THE GAME!") 
  
   

# Main code
pick_side()
if player == 'X' :
  move()
  show_matrix()

while is_table_full() == False :
  
 computer_move()
 show_matrix()
 if game_over() == True:
   who_won()
   print("THE GAME IS OVER.")
   clr()
   break

 if is_table_full()== False:
  move()
  show_matrix()
  if game_over() == True:
   who_won()
   print("THE GAME IS OVER.")
   clr()
   break
 
 if is_table_full()== True and game_over() == False:
      print("THE GAME IS TIED AND OVER\n")
      clr()


    

 

  

