#prepares layout before input
def make_game(n):
    game = [[' ' for x in range(n)] for y in range(n)]
    for i in range(n):
        if i == 0:
            game[i] = ['W' for x in range(n)]
        else:
            game[i][0] = 'W'
            game[i][-1] = 'W'
    game[n-1] = ['G' if x == ' ' else x for x in game[n-1]]
    return game

#updates the table
def get_data(n, table):
    y_n = ''
    while(y_n != 'n'):
        y_n = ''
        try:
            x,y,s = input("Enter the brick's position and the brick type: ").split()
            if s == 'S' or s == 'E' or s == 'B':
                game[int(x)][int(y)] = str(s)
            elif s.isdigit():
                game[int(x)][int(y)] = int(s)
            else:
                print("Enter a valid brick type.")
        except:
            print("Enter a valid position.")
        while(y_n != 'y' and y_n != 'n'):
            y_n = input("Do you want to continue(y or N)? ")
        if y_n == 'n':
            break
    ball = int(input("Enter ball count: "))
    game[n-1][int(n/2)] = 'o'
    return game, ball

def down_trav(game,x,y):
    for i in range(n-x):
        if isinstance(game[x+i][y],int):
            game[x+i][y] -= 1
            if game[x+i][y] == 0:
                game[x+i][y] = ' '
        elif game[x+i][y] == 'G':
            break
    return game

def ds(x,y,game):
    if game[x][y] != 'W' or game[x][y] != 'G':
        game[x][y] = ' '
    return game


def end_game(game):
    for i in range(1,n-1):
        for j in range(1,n-1):
            if isinstance(game[i][j], int):
                return False
    return True

def add_base(game):
    for a in range(1,int(len(game)/2)):
        if game[n-1][ball_cord[1]+a] == '_':
            pass
        else:
            game[n-1][ball_cord[1]+a] = '_'
            break
        if game[n-1][ball_cord[1]-a] == '_':
            pass
        else:
            game[n-1][ball_cord[1]-a] = '_' 
            break
    return game


if __name__ == '__main__':
   
    n = int(input("Enter size: "))
    win = 0
    game = make_game(n)
    winref = make_game(n)
    game, ball = get_data(n, game)
    by = int(n/2)
    bx = n-1
    ball_cord = [bx,by]
    temp_ball = ball
    #debug block
    for i in range(n):
        print(*game[i])
    while(ball != 0):
        direction = input("Enter the direction in which the ball need to traverse: ")
        #___________________________STRAIGHT TRAVERSAL__________________________
        if direction == 'ST':
            for i in range(n):
                if isinstance(game[n-1-i][ball_cord[1]], int):
                    game[n-1-i][ball_cord[1]] -= 1
                    if game[n-1-i][ball_cord[1]] == 0:
                        game[n-1-i][ball_cord[1]] = ' '
                    break
                    
                elif game[n-1-i][ball_cord[1]] == 'E':
                    for a in range(1,n-1):
                        game[n-1-i][a] = ' '
                    break
                elif game[n-1-i][ball_cord[1]] == 'S':
                    x = n-1-i
                    y = ball_cord[1]
                    #deleting integers
                    game = ds(x-1,y+1,game)
                    game = ds(x-1,y,game)
                    game = ds(x-1,y-1,game)
                    game = ds(x,y+1,game)
                    game = ds(x,y,game)
                    game = ds(x,y-1,game)
                    game = ds(x+1,y+1,game)
                    game = ds(x+1,y,game)
                    game = ds(x+1,y-1,game)
                    break
                elif game[n-1-i][ball_cord[1]] == 'B':
                    game = add_base(game)
                    game[n-1-i][ball_cord[1]] = ' '
                    break
                elif game[n-1-i][ball_cord[1]] == 'W':
                    ball-=1

        #______________________LEFT DIAGONAL TRAVERSAL_______________________
        elif direction == 'LD':
            for i,j in zip(range(n),range(n)):
                #-------NUMERICAL VALUE CHECK-----------------
                if isinstance(game[n-1-i][ball_cord[1]-j], int):
                    #x - i, y - i for left diagonal traversal
                    game = down_trav(game, n-1-i, ball_cord[1]-j)
                    #changing ball co-ord
                    if ball_cord[1]-j != ball_cord[1]:
                                if game[n-1][ball_cord[1]-j] == '_':
                                    if temp_ball == ball:
                                        game[n-1][ball_cord[1]] = '_'
                                        ball_cord[1] = ball_cord[1]-j
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball
                                    else: 
                                        game[n-1][ball_cord[1]] = 'G'
                                        ball_cord[1] = ball_cord[1]-j
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball
                                else:
                                    if temp_ball == ball and '_' in game[n-1]:
                                        game[ball_cord[0]][ball_cord[1]] = '_'
                                    else:
                                        game[ball_cord[0]][ball_cord[1]] = 'G'
                                    ball_cord[1] = ball_cord[1]-j
                                    game[ball_cord[0]][ball_cord[1]] = 'o'
                                    ball-=1
                    #win = end_game(game)
                    break
                #-----------WALL HIT CHECK------------------------
                elif game[n-1-i][ball_cord[1]-j] == 'W':
                    #CHANGING DIRECTION
                    for a in range(1,n):
                        if isinstance(game[n-1-i][ball_cord[1]-j+a], int):
                            game = down_trav(game,n-1-i,ball_cord[1]-j+a)
                            #APPENDING NEW BALL CO-ORDINATES
                            if ball_cord[1]-j+a != ball_cord[1]:
                                if game[n-1][ball_cord[1]-j+a] == '_':
                                    if temp_ball == ball:
                                        game[n-1][ball_cord[1]] = '_'
                                        ball_cord[1] = ball_cord[1]-j+a
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball
                                    else: 
                                        game[n-1][ball_cord[1]] = 'G'
                                        ball_cord[1] = ball_cord[1]-j+a
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball
                                else:
                                    if temp_ball == ball and '_' in game[n-1]:
                                        game[ball_cord[0]][ball_cord[1]] = '_'
                                    else:
                                        game[ball_cord[0]][ball_cord[1]] = 'G'
                                    ball_cord[1] = ball_cord[1]-j+a
                                    game[ball_cord[0]][ball_cord[1]] = 'o'
                                    ball-=1    
                            break
                        #WALL HIT POST WALL HIT CHECK -> REPLACE BALL CO-ORDINATE AND DECREMENT BALL COUNT
                        elif game[n-1-i][ball_cord[1]-j+a] == 'W':
                            if temp_ball == ball and '_' in game[n-1]:
                                game[ball_cord[0]][ball_cord[1]] = '_'
                            else:
                                game[ball_cord[0]][ball_cord[1]] = 'G'
                            ball_cord[1] = by
                            game[n-1][ball_cord[1]] = 'o'
                            ball-=1
                        elif game[n-1-i][ball_cord[1]-j+a] == 'B':
                            game = add_base(game)
                            game[n-1-i][ball_cord[1]-j+a] = ' '
                            break
                    break
                #DS AND DE BLOCK IMPLEMENTATION FOR LD TRAVERSAL
                elif game[n-1-i][ball_cord[1]-j] == 'E':
                    for a in range(1, n-1):
                        game[n-1-i][a] = ' '
                    break
                elif game[n-1-i][ball_cord[1]-j] == 'S':
                    x = n-1-i
                    y = ball_cord[1]-j
                    game = ds(x-1,y+1,game)
                    game = ds(x-1,y,game)
                    game = ds(x-1,y-1,game)
                    game = ds(x,y+1,game)
                    game = ds(x,y,game)
                    game = ds(x,y-1,game)
                    game = ds(x+1,y+1,game)
                    game = ds(x+1,y,game)
                    game = ds(x+1,y-1,game)
                    break
                elif game[n-1-i][ball_cord[1]-j] == 'B':
                    game = add_base(game)
                    game[n-1-i][ball_cord[1]-j] = ' '
                    break
        #____________________________RIGHT DIAGONAL TRAVERSAL_________________________
        elif direction == 'RD':
            for i,j in zip(range(n),range(n)):
                if isinstance(game[n-1-i][ball_cord[1]+j], int):
                    #x - i, y - i for left diagonal traversal
                    game = down_trav(game, n-1-i, ball_cord[1]+j)
                    #changing ball co-ord
                    if ball_cord[1]+j != ball_cord[1]:
                                if game[n-1][ball_cord[1]+j] == '_':
                                    if temp_ball == ball:
                                        game[n-1][ball_cord[1]] = '_'
                                        ball_cord[1] = ball_cord[1]+j
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball 
                                    else: 
                                        game[n-1][ball_cord[1]] = 'G'
                                        ball_cord[1] = ball_cord[1]+j
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball
                                else:
                                    if temp_ball == ball and '_' in game[n-1]:
                                        game[ball_cord[0]][ball_cord[1]] = '_'
                                    else:
                                        game[ball_cord[0]][ball_cord[1]] = 'G'
                                    ball_cord[1] = ball_cord[1]+j
                                    game[ball_cord[0]][ball_cord[1]] = 'o'
                                    ball-=1
                    break
                #if it hits the Wall during LD traverse
                elif game[n-1-i][ball_cord[1]+j] == 'W':
                    #changing directions to right 
                    for a in range(1,n):
                        if isinstance(game[n-1-i][ball_cord[1]+j-a], int):
                            game = down_trav(game,n-1-i,ball_cord[1]+j-a)
                            #changing ball co-ord
                            #FIGURED WORKING BALL BASE!!!!!!!!!!! APPLY FOR REST - done
                            if ball_cord[1]+j-a != ball_cord[1]:
                                if game[n-1][ball_cord[1]+j-a] == '_':
                                    if temp_ball == ball:
                                        game[n-1][ball_cord[1]] = '_'
                                        ball_cord[1] = ball_cord[1]+j-a
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball 
                                    else: 
                                        game[n-1][ball_cord[1]] = 'G'
                                        ball_cord[1] = ball_cord[1]+j-a
                                        game[n-1][ball_cord[1]] = 'o'
                                        temp_ball = ball
                                else:
                                    if temp_ball == ball and '_' in game[n-1]:
                                        game[ball_cord[0]][ball_cord[1]] = '_'
                                    else:
                                        game[ball_cord[0]][ball_cord[1]] = 'G'
                                    ball_cord[1] = ball_cord[1]+j-a
                                    game[ball_cord[0]][ball_cord[1]] = 'o'
                                    ball-=1   
                            break
                        elif game[n-1-i][ball_cord[1]+j-a] == 'W':
                            if temp_ball == ball and '_' in game[n-1]:
                                game[ball_cord[0]][ball_cord[1]] = '_'
                            else:
                                game[ball_cord[0]][ball_cord[1]] = 'G'
                            ball_cord[1] = by
                            game[n-1][ball_cord[1]] = 'o'
                            ball-=1
                        elif game[n-1-i][ball_cord[1]+j-a] == 'B':
                            game = add_base(game)
                            game[n-1-i][ball_cord[1]+j-a] = ' '
                            break
                    break
                #RIGHT DIAGONAL DS AND DE IMPLEMENTATION
                elif game[n-1-i][ball_cord[1]+j] == 'E':
                    for a in range(1,n-1):
                        game[n-1-i][ball_cord[1]+j] == ' '
                    break
                elif game[n-1-i][ball_cord[1]+j] == 'S':
                    x = n-1-i
                    y = ball_cord[1]+j
                    game = ds(x-1,y+1,game)
                    game = ds(x-1,y,game)
                    game = ds(x-1,y-1,game)
                    game = ds(x,y+1,game)
                    game = ds(x,y,game)
                    game = ds(x,y-1,game)
                    game = ds(x+1,y+1,game)
                    game = ds(x+1,y,game)
                    game = ds(x+1,y-1,game)
                    break
                elif game[n-1-i][ball_cord[1]+j] == 'B':
                    game = add_base(game)
                    game[n-1-i][ball_cord[1]+j] = ' '
                    break
                elif game[n-1-i][ball_cord[1]+j] == 'B':
                    game = add_base(game)
                    game[n-1-i][ball_cord[1]+j] = ' '
                    break
        for i in range(n):
            print(*game[i])
        print("Ball count: " + str(ball))
        win = end_game(game)
        if win:
            print("HURRAY! You won.")
            break
        elif ball == 0:
            print("You lost. :)")
            break
    
    
        

      





    
        


