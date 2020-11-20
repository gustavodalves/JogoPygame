#Calebe Ferreira / T.I.A:32088116#
#Gustavo Alves / T.I.A:32081286#
#Mateus de Pasquali / T.I.A:32086997#
#Nicolas Pisndorf / T.I.A: 32036108#

import pygame
import sys
import os

##parte do menu
class widget():
        def __init__(self):
            self.pack = {}
            self.rend = {}
            self.link = {}
            self.ID_num = 0
            self.ID_key = ''
            self.ID_max = 0
       
        def Add(self,Type,name,x,y,w,h,Text = '',Size = 18):
            if self.ID_max == 0:
                self.ID_key = name
                IDfocus = True
            else:
                IDfocus = False
           
                    #  backgound      border       hilight    Text    selected
            color = [(255,255,255),(125,125,125),(220,220,0),(0,0,0),(0,130,0)]
                                                   #   show  mouse focus
            self.pack[name] = [Type,(x,y),(w,h),color,[False,False,IDfocus],
                               self.ID_max]

            self.Render(name,Text,Size,1)
            self.ID_max += 1

        def AddMenu(self,name,Menu,x,y,Size = 25):
            if self.ID_max == 0:
                self.ID_key = name
                IDfocus = True
            else:
                IDfocus = False
                    #  backgound      border       hilight    Text    selected
            color = [(255,255,255),(125,125,125),(220,220,0),(0,0,0),(0,130,0)]

            self.pack[name] = ['menu',(x,y),(0,0),color,[False,False,IDfocus],
                               self.ID_max,len(Menu),0,0]
           
            self.ID_max += 1

            self.RendMenu(name,Menu,Size)

        def RendMenu(self,key,Menu,txtsize):
            Font = pygame.font.Font(None,txtsize)
            self.pack[key][6] = len(Menu)
           
            x,y = self.pack[key][1]
           
            loop = 0
            width = self.pack[key][2][1]
            for mn in Menu:
                size = Font.size(mn)
                if size[0] > width:
                    width = size[0]
                pos = (x - size[0]/2 , y - len(Menu)*txtsize/2 + loop*txtsize)
                Rect = pygame.Rect(pos,size)
               
                NormTxt = Font.render(mn,1,self.pack[key][3][0])
                HiTxt = Font.render(mn,1,self.pack[key][3][2])
                OffTxt = Font.render(mn,1,self.pack[key][3][1])
                SelTxt = Font.render(mn,1,self.pack[key][3][4])

                if loop == 0:
                    self.rend[key] = [(OffTxt,NormTxt,HiTxt,SelTxt,pos,Rect,loop)]
                else:
                    self.rend[key].append((OffTxt,NormTxt,HiTxt,SelTxt,pos,Rect,loop))
                loop += 1

            height = len(Menu)*txtsize
            self.pack[key][2] = (width,height)
           
        def Render(self,key,text,txtsize,curpos):
            Rect = pygame.Rect(self.pack[key][1],self.pack[key][2])
            Font = pygame.font.Font(None,txtsize)
           
            size = Font.size(text)
            x,y = self.pack[key][1]
            w,h = self.pack[key][2]
            rtxt = text
           
            if self.pack[key][0] == 'button':
                pos = (x +((w -size[0])/2),y +((h - size[1])/2))
               

        def SetColor(self,key,code,color):
            # code = 0 - 4
            self.pack[key][3][code] = color

        def SetLink(self,key,Link,var1 = None,var2 = None,Append = False):
            if Append == False:
                self.link[key] = [(Link,var1,var2)]
            else:
                self.link[key].append((Link,var1,var2))

        def DoLink(self,code = 0):
            lk = self.link[self.ID_key]
            if not lk[code][2] == None:
                lk[code][0](lk[code][1],lk[code][2])
            elif not lk[0][1] == None:
                lk[code][0](lk[code][1])
            else:
                lk[code][0]()

        def Draw(self,key,canvas):

                if self.pack[key][0] == 'menu':
                        if self.pack[key][4][2] == True:
                            xcolor = 1
                            peek = 2
                        elif self.pack[key][4][1] == True:
                            xcolor = 2
                            peek = 1
                        else:
                            xcolor = 0
                            peek = 0
                for num in range(0,self.pack[key][6]):
                    if self.pack[key][7] == num:
                        canvas.blit(self.rend[key][num][3],
                                    self.rend[key][num][4])
                    elif self.pack[key][8] == num:
                        canvas.blit(self.rend[key][num][peek],
                                    self.rend[key][num][4])
                    else:
                        canvas.blit(self.rend[key][num][xcolor],
                                    self.rend[key][num][4])

        def MouseOver(self,evt):
            Keys = self.pack.keys()
            x,y = evt.pos
            for key in Keys:
                kx , ky = self.pack[key][1]
                kw , kh = self.pack[key][2]
                if self.pack[key][0] == 'menu':
                    kx -= kw/2
                    ky -= kh/2

                if x > kx and x < kx + kw:
                    if y > ky and y < ky + kh:
                        self.pack[key][4][1] = True
                        if self.pack[key][0] == 'menu':
                            for mn in self.rend[key]:
                                rr = mn[5]
                                if x > rr[0] and x < rr[0] + rr[2]:
                                    if y > rr[1] and y < rr[1] + rr[3]:
                                        self.pack[key][8] = mn[6]
                    else:
                        self.pack[key][4][1] = False
                else:
                    self.pack[key][4][1] = False

        def MouseSelect(self,evt):
            if evt.button == 1:
                Keys = self.pack.keys()
                x,y = evt.pos
                for key in Keys:
                    kx , ky = self.pack[key][1]
                    kw , kh = self.pack[key][2]
                    if self.pack[key][0] == 'menu':
                        kx -= kw/2
                        ky -= kh/2

                    if x > kx and x < kx + kw:
                        if y > ky and y < ky + kh:
                            self.SetFocus(self.pack[key][5])
                            if self.pack[self.ID_key][0] == 'button':
                                self.DoLink()
                            elif self.pack[key][0] == 'menu':
                                for mn in self.rend[key]:
                                    rr = mn[5]
                                    if x > rr[0] and x < rr[0] + rr[2]:
                                        if y > rr[1] and y < rr[1] + rr[3]:
                                            self.pack[key][7] = mn[6]
                                            self.DoLink(self.pack[key][7])
               
        def Event(self,evt):
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_TAB:
                    self.ID_num += 1
                    self.ID_num %= self.ID_max
                    self.SetFocus(self.ID_num)

                elif self.pack[self.ID_key][0] == 'menu':
                    if evt.key == pygame.K_UP:
                        self.pack[self.ID_key][8] -= 1
                        if self.pack[self.ID_key][8] < 0:
                            self.pack[self.ID_key][8] = self.pack[self.ID_key][6] -1
                    elif evt.key == pygame.K_DOWN:
                        self.pack[self.ID_key][8] += 1
                        self.pack[self.ID_key][8] %= self.pack[self.ID_key][6]
                    elif evt.key == pygame.K_RETURN:
                        self.pack[self.ID_key][7] = self.pack[self.ID_key][8]
                        self.DoLink(self.pack[self.ID_key][7])
                   
            elif evt.type == pygame.MOUSEBUTTONDOWN:
                self.MouseSelect(evt)
           
            elif evt.type == pygame.MOUSEMOTION:
                self.MouseOver(evt)

        def Update(self,canvas):
            Keys = self.pack.keys()
            for key in Keys:
                self.Draw(key,canvas)

        def key_event(self,key,evt):
            letter = None
            if evt.key == pygame.K_BACKSPACE:
                Tx,cr = self.rend[key][0] , self.rend[key][5][0]
                Tx = Tx[:cr-2] + Tx[cr-1:]
                cr -= 1
                if cr < 1:
                    cr = 1
                self.Render(key,Tx,self.rend[key][5][1],cr)

            if evt.key == pygame.K_DELETE:
                self.Render(key,'',self.rend[key][5][1],1)

            if evt.key > 96 and evt.key < 123:
                letter = chr(evt.key)

            if evt.key > 47 and evt.key < 58:
                letter = chr(evt.key)

            if evt.key == pygame.K_SPACE:
                letter = " "

            if not letter == None:
                Tx,cr = self.rend[key][0] , self.rend[key][5][0]
                Tx = Tx[:cr-1] + letter + Tx[cr-1:]
                cr += 1   
                self.Render(key,Tx,self.rend[key][5][1],cr)
                                                     
        def SetFocus(self,ID):
            self.ID_num = ID
            Keys = self.pack.keys()
            for key in Keys:
                if ID == self.pack[key][5]:
                    self.pack[key][4][2] = True
                    self.ID_key = key
                else:
                    self.pack[key][4][2] = False                                                 

def Quit():
        pygame.display.quit()

def menutouch(txt):
    font = pygame.font.SysFont(None, 55)
    if txt == 'Start':
        jogoDaVelha()
    else:
        Quit()

    



def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


##Parte do jogo
def draw_board(surface):
    width = surface.get_width()
    height = surface.get_height()
    white = (255, 255, 255)

    # Draw border
    pygame.draw.line(surface, white, (0, 0), (width, 0))
    pygame.draw.line(surface, white, (0, 0), (0, height))
    pygame.draw.line(surface, white, (width - 1, 0), (width - 1, height))
    pygame.draw.line(surface, white, (0, height - 1), (width, height - 1))

    # Draw vertical lines
    pygame.draw.line(surface, white, (width / 3, 0), (width / 3, height))
    pygame.draw.line(surface, white, (2 * width / 3, 0), (2 * width / 3, height))

    # Draw horizontal lines
    pygame.draw.line(surface, white, (0, height / 3), (width, height / 3))
    pygame.draw.line(surface, white, (0, 2 * height / 3), (width, 2 * height / 3))

def draw_x(surface, row, col):
    width = surface.get_width()
    height = surface.get_height()
    posx = int((width / 3) * col + width / 6)
    posy = int((height / 3) * row + height / 6)

    white = (255, 255, 255)
    pygame.draw.line(surface, white, (posx - 5, posy - 5), (posx + 5, posy + 5))
    pygame.draw.line(surface, white, (posx + 5, posy - 5), (posx - 5, posy + 5))

def draw_o(surface, row, col):
    width = surface.get_width()
    height = surface.get_height()
    white = (255, 255, 255)
    posx = int((width/3) * col + width/6)
    posy = int((height / 3) * row + height/6)
    pygame.draw.circle(surface, white, [posx, posy], 7, 1)

def draw_symbol(surface, symbol, row, col):
    if symbol == 'x':
        draw_x(surface, row, col)
        effect.play()
    else:
        draw_o(surface, row, col)
        effect.play()


def check_victory_horizontal_lines(symbol, board):
    for line in board:
        if line.count(symbol) == 3:
            return True

def check_victory_vertical_lines(symbol, board):
    counter_by_line = 0
    for col in range(3):
        for line in board:
            if line[0] == symbol:
                counter_by_line += 1
                if counter_by_line == 3:
                    return True
            else:
                counter_by_line = 0
                break

def check_victory_diagonal_lines(symbol, board):
    index = 0
    counter = 0

    for line in board:
        if line[index] == symbol:
            counter += 1
            index += 1
            if counter == 3:
                return True
        else:
            counter = 0
            index = 2
            break

    for line in board:
        if line[index] == symbol:
            counter += 1
            index -= 1
            if counter == 3:
                return True
        else:
            break

    return False

def check_victory(xturn, board):
    symbol = 'x' if xturn else 'o'
    return check_victory_horizontal_lines(symbol, board) or \
           check_victory_vertical_lines(symbol, board) or \
           check_victory_diagonal_lines(symbol, board)

def check_tie(board):
    for line in board:
        if 0 in line:
            return False
    return True




def jogoDaVelha():
    global effect
    if __name__ == "__main__":
        pygame.init()

        board = [[0,0,0],[0,0,0],[0,0,0]]

        xturn = True;

        size = width, height = 600, 600
        screen = pygame.display.set_mode(size)
        victory = False

        pygame.mixer.music.load("data/music/happy.mp3")
        pygame.mixer.music.play(-1)

        vic = pygame.mixer.Sound('data/soundEffects/victory.mp3')
        fail = pygame.mixer.Sound('data/soundEffects/fail.mp3')
        effect = pygame.mixer.Sound('data/soundEffects/effect.wav')
        trophy = pygame.image.load('data/image/trophy.jpg')

        while True:


            draw_board(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:

                    if not victory:

                        pos = pygame.mouse.get_pos()
                        col = int(pos[0] / (width / 3))
                        row = int(pos[1] / (height / 3))

                        if board[row][col] == 0:
                            if xturn:
                                draw_symbol(screen, 'x', row, col)
                                board[row][col] = 'x'
                            else:
                                draw_symbol(screen, 'o', row, col)
                                board[row][col] = 'o'

                            if check_victory(xturn, board):
                                print("VITÓRIA!!!")
                                vic.play()                        
                                pygame.time.wait(4000)                         
                                jogoDaVelha()

                            if check_tie(board):
                                print("VELHA!!!")
                                fail.play()
                                pygame.time.wait(4000)  
                                jogoDaVelha()
                                
                            xturn = not xturn


if __name__ == "__main__":
        width , height = 800 , 600
        clock = pygame.time.Clock()
        pygame.init()
        screen = pygame.display.set_mode((width,height))
       
        item = widget()
        item.AddMenu('mn1',['Start','Quit'],400,280)
        item.SetLink('mn1',menutouch,'Start')
        item.SetLink('mn1',menutouch,'Quit',None,True)



        Run = True
        while Run:
            screen.fill((0,150,250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Run = False
                item.Event(event)

            item.Update(screen)
           
            pygame.display.flip()
            clock.tick(15)
        Quit()