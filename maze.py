#!/usr/bin/python
from random import choice
from random import random as rand

class progress:
    count = 0
    def __init__(self, func,startmsg=''):
        self.func   = func
        self.msg    = startmsg
    def __lt__(self,x):     return x > self.count
    def __gt__(self,x):     return x < self.count
    def __eq__(self,x):     return x==self.count
    def __ge__(self,x):     return x<=self.count
    def __gl__(self,x):     return x>=self.count
    def __repr__(self):     return repr(self.count)
    def update(self):
        if (self.count == 0): print self.msg+'.',
        self.count = self.count + 1
        if self.func(self.count): print '.',

class cell:
    n=s=e=w = True
    visited = False
    searched = False
    
class maze:
    def __init__(self,width,height=None, start=None, end=None):
        if (height == None):    height = width
        if (start==None):       start = (0,0)
        if (end==None):         end = (width-1,height-1)
            
        self.height = height
        self.width  = width
        self.start  = start
        self.end    = end
        self.cells  = [[cell() for x in xrange(height)] for y in xrange(width)]

    def reset(self):
        self.cells  = [[cell() for x in xrange(self.height)] for y in xrange(self.width)]    

    def dispcells(self):
        tf = lambda x: chr(102+(x*14))
        for x in self.cells:
            a=''
            for y in x:
                a = a+tf(y.visited)+tf(y.searched)+':'+tf(y.w)+tf(y.n)+tf(y.s)+tf(y.e)+' '
            print a
            
    def setcell(self,(x,y),n=None,s=None,e=None,w=None):
        width = self.width
        height = self.height
      
        if not(n==None):
            self.cells[x][y].n = n
            if x >= 1:
                self.cells[x-1][y].s = n

        if not(s==None):
            self.cells[x][y].s   = s
            if x < width-1:
                self.cells[x+1][y].n = s

        if not(e==None):
            self.cells[x][y].e = e
            if y < height-1:
                self.cells[x][y+1].w = e
                
        if not(w==None):
            self.cells[x][y].w   = w
            if y >= 1: 
                self.cells[x][y-1].e = w

    def disp(self):
        print
        b = ' '
        
        for x in self.cells[0]:
            if x.n: b=b+'_ '
            else:   b=b+'  '
        b=b+'\n'
        for x in self.cells:
            for y in x:
                if y.w: b=b+'|'
                else:   b=b+' '               
                if y.s: b=b+'_'
                else:   b=b+' '
            if y.e: b=b+'|'
            else:   b=b+' '
            b=b+'\n'

        print b

    def novisit(self,(x,y)):
        a=self.neighbours((x,y))
        b=[]
        for c,d in a:
            if self.cells[c][d].visited == False:
                b.append((c,d))

        return b

    def iswall(self, (x1,y1),(x2,y2)):
        if x1==x2:
            if y1<y2:   return (self.cells[x1][y1].e)
            else:       return (self.cells[x1][y1].w)
        elif y1==y2:
            if x1<x2:   return (self.cells[x1][y1].s)
            else:       return (self.cells[x1][y1].n)
        else:
            return False

    def beensearched(self,(x,y)):
        return self.cells[x][y].searched

    def canvisit(self,(x,y)):
        a=self.neighbours((x,y))

        for b in a[:]:
            if self.iswall((x,y),b) or self.beensearched(b):
                a.remove(b)
                
        return a

    def breakwalls(self,(x1,y1),(x2,y2)):
        if x1==x2:
            if y1<y2:   self.setcell((x1,y1),e=False)
            else:       self.setcell((x1,y1),w=False)
        elif y1==y2:
            if x1<x2:   self.setcell((x1,y1),s=False)
            else:       self.setcell((x1,y1),n=False)
                                     
    def neighbours(self,(x,y)):
        a=[]
        if 0 < x < self.width-1:    a.extend( [(x-1,y), (x+1,y)] )
        elif x <= 0:                a.append( (x+1,y) )
        else:                       a.append( (x-1,y) )
                     
        if 0 < y < self.height-1:   a.extend( [(x,y-1), (x,y+1)] )
        elif y <= 0:                a.append( (x,y+1) )
        else:                       a.append( (x,y-1) )

        return a

    def backgen(self, cell=None):
        if cell==None: cell=self.start
        stack=[]
        size = self.width*self.height
        p = progress(lambda x:not((float(x)/size)*100)%10,'Generating')
    
        while (p < size):
            x,y=cell
            self.cells[x][y].visited = True
            novisit = self.novisit(cell)
            
            if not(novisit==[]):
                p.update()
                stack.append(cell)
                next = choice(novisit)
                self.breakwalls(cell,next)
                cell = next
            else:
                if stack == []: p.update()
                else: cell=stack.pop(int(rand()*len(stack)))
                
    def backsolve(self, cell=None):
        if cell==None: cell=self.start
        stack=[]
        p=progress(lambda x:not((100*(float(x)/(self.width*self.height))%10)),'Solving')
        
        for x in self.cells:
            for y in x:
                y.searched = False
        
        while not(cell == self.end):
            p.update()
            x,y = cell
            self.cells[x][y].searched = True
            canvisit = self.canvisit(cell)
            if not(canvisit==[]):
                stack.append(cell)
                next = choice(canvisit)
                cell = next
            else:
                cell = stack.pop()
        
        stack.append(self.end)
        return stack
        
    def gen(self):
        self.reset()
        self.backgen()

        for a in self.start, self.end:
            x,y = a
            if x == 0:              self.setcell(a,n = False)
            elif y==0:              self.setcell(a,w = False)
            elif x==self.width-1:   self.setcell(a,s = False)
            elif y==self.height-1:  self.setcell(a,e = False)


def main():
    import sys
    if len(sys.argv) == 3:
        x, y = max(2,int(sys.argv[1])), max(2,int(sys.argv[2]))
        m=maze(x,y)
    else:
        m=maze(20,20)
    m.gen()
    m.disp()


if __name__ == '__main__':
    main()
