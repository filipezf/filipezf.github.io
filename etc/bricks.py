# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:33:00 2019

@author: u4ft
"""
import itertools 
import math
import numpy as np
import random

'''
The program lists how many shapes can be generated from a set of rectangular 'lego' blocks.
It receives the list of blocks, generate all combinations using all or less pieces and their permutations

Then , (for each permutation), starting from a free position at the origin, add blocks in that order, 
generating a set of configurations

Finally, for all the configurations, calculate hashes that are the same for configurations that occupy the same shape:
The combinations below are considered the same because both occupy a 2x2 vertical square.
The hash considers as equivalent shapes which can be rotated or mirrored on each other.

[][]       [  ]      xx   
[  ]  and  [][]   =  xx  

It should be easy to adapt the hash function to differentiate the above situtations or mirrored configurations, 
or even non-rectangular blocks.

The size of the set of hashes is the total of configurations.

'''


pieces = [(1,1)]*2  +[(1,1)]*1 + [(2,2)]*1   # two 1x1 blocks, 1 1x2 blocks and one 2x2 block
pieces = [(1,1)]*2  +[(3,3)]*1
#pieces = [(1,1), (2,1), (3,1), (4,2)]
pieces = [(2,1)]*6

#calculate all combinations of these pieces, remove repeated combinations and transform to list
powerset = itertools.chain.from_iterable(itertools.combinations(pieces, r) for r in range(len(pieces)+1))
powerset = set(powerset)
powerset = list(powerset)

# sort from less to more blocks
powerset.sort(key =lambda a: len(a))

#get all permutations for each combination
perm = [ itertools.permutations(s) for  s in powerset]

perm = perm[-1:]   #uncomment if you only want the last item => (last item = permutations that use ALL the blocks)

    
hashes = set()



def hashlist(lst):
    rb=0
    q =0
    for a,b in lst:
        q += 1
        rb += 1.1** (a+b) * 1.2 ** (a*b) *1.3**q
    
    return int(1e8*rb)

def hashpos(lst):
    rb=0
    for x,y,z in lst:
        rb += 1.1** x * 1.2 ** y *1.3**z
    
    return int(1e8*rb)
    


#calculates a unique value for each shape:
calc_hash_buf = {}   
def calc_hash(aa):

    if len(aa) ==0:
        return None
    
  #  if aa in calc_hash_buf:
   #     return calc_hash_buf(aa)
    
    
    a = np.array(list(aa))

    # generates canonical tranalation and rotation for the 3d shape:
    # 3D Shape Descriptor Based on 3D Fourier Transform - D. V. Vranic and D. Saupe

        # calculates center of mass and subtract: invariance over translation
    am = np.mean(a, axis=0)
    a = a - am 
    sign = lambda x: 1 if x>=0 else -1

    
        # rotate to canonical position along x and y axis

        # the function 1.1** abs(x)* 1.2**abs(y)*1.3**z  is unique for each tuple (x,y,z) (up to reflection)
    
    def r(i): return np.round(i,3) # 
    
    x,y,z = r(a[:,1]), r(a[:,2]), r(a[:,0])
    fx= np.sum( np.sign(x)* 1.1** abs(x)* 1.2**abs(y)*1.3**z )
    fy= np.sum( np.sign(y)* 1.1** abs(y)* 1.2**abs(x)*1.3**z )
    x *= sign(fx)
    y *= sign(fy)
    if abs(fy) > abs(fx):
         x,y = y,x

    ''' 
        -x--    --x-    ----    ----     AABB  compare for y>=0 if left quadrant (A) > right quadrant (B)  
        ---- vs ---- vs x--- vs ---x  -> AABB  using the canonical tuple comparing function 
        ----    ----    ---x    x---     ----
        --x-    -x--    ----    ----     ----  symmetry along x=0 axis
        
        x-  vs  -x                     
        -x      x-
        
        -xx-    ----    ---    -x-       -B--  compare for y>=0 and x>=0 if octant A > octant B  x-y >0
        ---- vs x--x    x-x vs ---    -> A---  using again the canonical tuple comparing function 
        ----    x--x    ---    -x-       ----
        -xx-    ----                     ----   symmetry along x=y axis       
        
    '''
    
    if   abs(fx)<0.01 and abs(fy)<0.01:   
        fxy = np.sum( np.sign(x)*np.heaviside(y, 1)*1.1** abs(x)* 1.2**abs(y)*1.3**z )
        if fxy<0:         
           x = -x
        fxy2 = np.sum( np.sign(x-y)*np.heaviside(x, 1)*np.heaviside(y, 1)*1.1** abs(x*y)*1.3**z )
        if fxy2 < 0:         
            x,y = y,x    


    # now that we are on a canonical position, the hash is the sum (invariant ove permutations) over all positions
    # each position (tuple (x,y,z) ) generates a unique value: 1.1**x * 1.2**y * 1.3**z
    # we try to generate incomensurable values to avoid collisions - there is a test below 
    # we estimate that for up to 100000 different shapes the  chance of having two different shapes with the same hash is lowet than 1% 

    ret = np.sum( 1.1**x * 1.2**y * 1.3**z ) 
    ret = int(1e10*ret)
    
#    calc_hash_buf[aa] = ret
    return  ret    #truncates to int

    '''
    if ret not in hashes:
        mx, my,mz = np.min(x), np.min(y), np.min(z)
        (values,counts) = np.unique(z,return_counts=True)
        ind=np.argmax(counts)
        z33 = values[ind]
        for i in range(x.size):
            if z[i] != z33:
                print( int(round(x[i]-mx-1)), int(round(y[i]-my-1)), int(round(z[i]-mz)))

        #print(values[ind], len(hashes))    
        print()    
       # print (x -np.min(x),y-np.min(y),z-np.min(z))'''
   


    '''
    #Alternative return concatenting positions guaranteed to avoid collision

    N = a.shape[0]
    def r2(i): return str(i)+ ','
    k = ['']*N
    for i in range( N):
        k[i] = r2(z[i]) + r2(y[i]) + r2(x[i])
    k.sort()
    return '  '.join(k)
    '''


'''test hash uniqueness'''

if False:
    def r(i): return np.trunc(i*1000)/1000 # + np.sign(i)/1000)
    def hash1( x,y,z):
        x,y,z = np.array(x),np.array(y),np.array(z)
        ret = np.sum( 1.1**r(x) * 1.2**r(y) * 1.3**r(z) ) 
        return ret 

    table = {}
    sums = set()    
    for j in range(int(1e6)):
        if j%10000 ==0:
            print(j)
            
        N = random.randint(3,3)
        x,y,z = np.zeros(N), np.zeros(N), np.zeros(N)
        for i in range(N):
            x[i] = random.randint(-5,5)
            y[i] = random.randint(-5,5)
            z[i] = random.randint(-5,5)
        h = hash1(x,y,z)
        h = int(1e10*h)
        
        if h in table:
            print (x,y,z)
            print (table[h])
            print()
        else:
            table[h] = (x,y,z)    






'''Add one block

   lst = list of bricks to add
   added = already added bloks
   free_points = where we can attach new bricks
   occupied - postions occupied by bricks '''

considered = set() # already considered values
def add(lst, added, free_points, occupied):

    # check if we already considered this occupied position and future blocks
    
    #ch2 =( hashlist(lst), hashpos( free_points), hashpos(occupied))
    ch2 =( hashlist(lst), frozenset(occupied))
    if  ch2 in considered:
        return              # don't need to calculate again
    else:
        considered.add (ch2)
    
    if len(lst)==0:                 # no more blocks to add: add the hash of this configuration to the set
    
        hashes.add( calc_hash(occupied) )

    else:    
       piece = lst[0]
       
       tested_positions = set()     
       for pos in free_points:      # for each free attchable point:           
           h, posx, posy = pos
          
           if h < 0:
               continue
           def addBlock(px, py, h, dx,dy): # add a block that occupies height h,one corner at px,py and size dx,dy
               
                #check if this block would clash with al already occupied position
               for p,q in itertools.product(range(px, px+dx),range( py, py+dy)):
                   if (h,p,q) in occupied:
                       return
            
               free_points1 = free_points.copy()  
               occupied1 =  occupied.copy()    
               added1 = added.copy()   

                # add the block's shape to the list of occupied positions 
                # and its top and bottom to the list of free (Attachable) positions
                
               for p,q in itertools.product(range(px, px+dx),range( py, py+dy)):                   
                   free_points1.add( (h+1, p,q) )
                   free_points1.add( (h-1, p,q) )
                   occupied1.add((h, p,q))  
                  
               added1.append((px+dx/2,py+dy/2, dx,dy,h))                    

                #ad the next block
               add(lst[1:], added1, free_points1, occupied1)
           

          # add a block  in all the possible positions at the free point, in both orientations ( AxB and BxA)  

           if len(occupied)==0: # first block fixed position
               addBlock(0, 0, h,piece[0], piece[1])
           else:     
               for p,q in itertools.product(range(posx-(piece[0]-1), posx+1), range(posy-(piece[1]-1), posy+1)):
                   if (p,q,h,0) not in tested_positions:    # check if is a new position
                       tested_positions.add((p,q,h,0))
                       addBlock(p, q, h,piece[0], piece[1]) 
               for p,q in itertools.product(range(posx-(piece[1]-1), posx+1), range(posy-(piece[0]-1), posy+1)):
                   if (p,q,h,1) not in tested_positions:
                       tested_positions.add((p,q,h,1))
                       addBlock(p, q, h,piece[1], piece[0])
    
                     
# start with one useable position at the origin 0,0,0 and add the first block of the permutation
# the add function will recursively add the other blocks
def calc(perm1):               
    for i in set(perm1):
        lst = [ (0,0,0)]
        add(list(i), [], set(lst), set())   


for perm1 in perm:    #for each permutation set
    z = set(perm1)   #remove repeated
    n = len(hashes)  
    calc(z)           #generate shapes
    print (len(hashes)-n, list(z)[0])   # print how many hashed added

#print the total of hashes (occupied shapes)
print (len(hashes))

