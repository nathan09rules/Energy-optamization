class loc():
    def __init__(self , poi , prod , dem , store , type ):
        self.prod = prod
        self.dem = dem
        self.type = type
        self.poi = poi
        self.store = store
        self.net_ex = 0
        self.grid_lines = {}
        self.center = "CENTER"
        self.color = 0
    
    @property
    def net(self):
        net = int(self.prod - self.dem + self.net_ex)
        #(self.type ,  "has a net value of" , net , "kW")
        return net

    @net.setter
    def net(self , value):
        c = self.net
        self.net_ex += int(value - c)

    @property
    def cap(self): # amke store greater than net
        cap =  int(self.net - self.store) 
        return cap

    def rep(self):
        type = self.type
        if type == "hospital":
            return 8
        elif type == "house":
            return 2
        else:
            return 1       

def all_net(loc : [loc]):
    sum = 0
    for l in loc:
        sum += l.net
    return sum

def poi(loc : [loc] , table):
    for l in loc:
        for poi in l.poi:
            table[poi[1]][poi[0]] = l.rep()
    
    return table

def ptable(table):
    for x in table:
        pass

def closest_net(self , loc , loss_of_energy ):
    closest_net = 0
    c_dis = float("inf")
    # return an array with [loc , energy , wasted]
    all = []
    for l in loc:
        if l.type != self.type:
            t_dis = abs(self.poi[0][0] - l.poi[0][0]) + abs(self.poi[0][1] - l.poi[0][1])
            supply = ( l.net * (1 + (1 - loss_of_energy) ** t_dis ))
            waste = l.net - supply
            all.append([ l , supply , waste , t_dis])
    # return an array with [loc , energy , wasted]
    return sorted(all , key = lambda x : x[1])

def energy_opt(queue , ENERGY_BOOK , loss_of_energy):
    ENERGY_MET = True

    defecet = []
    surplus = []

    for l  in queue:
        net = l.net
        if net < 0:
            defecet.append(l)
        if net > 0:
            surplus.append(l)

    ()
    for d in defecet:
        close = closest_net( d , surplus, loss_of_energy)
        close.sort(key = lambda x : (- x[1] / (x[2] + 1) , x[1]))
        
        for c in close:
            s ,  energy , waste , dis = c
            supply = min( energy , - d.net )

            d.net += supply 
            s.net -= supply * ( 1 + loss_of_energy ** dis) 

            ENERGY_BOOK.append([supply , s , d])
        

            if s.net <= 0:
                surplus.remove(s)

            if d.net >= 0:
                break
        
        if d.net < 0:
            #("there is not enough energy , there is a defecet of" , d.net , " for" , d.type)
            ENERGY_BOOK.append([d.net , "FAILED" , "NET"])
            ENERGY_MET = False

    print(len(ENERGY_BOOK))
    if ENERGY_MET==True:
        ENERGY_BOOK.append(["PASS" , "PASS" , "NET"])
        #("\n , all were supplyed energy now moving to storage" , "\n")

        exceeding = []
        storable = []

        for q in queue:
            if q.cap > 0:
                exceeding.append(q)
            elif q.cap < 0:
                storable.append(q) #if s = 0 its already removed in the part above
        
        print([(l.type) for l in exceeding])
        print([(l.type) for l in storable])
        
        return storage_opt(exceeding , storable , ENERGY_BOOK , loss_of_energy)
    
    return ENERGY_BOOK

def closest_store(self , loc , loss_of_energy):
    c_dis = float("inf")
    # return an array with [loc , energy , wasted]
    all = []
    for l in loc:
        if l != self:
            # suppose 2 percent lost per unit
            t_dis = abs(self.poi[0][0] - l.poi[0][0]) + abs(self.poi[0][1] - l.poi[0][1])
            supply = ( (l.cap) * (1 + (1 - loss_of_energy) ** t_dis ))
            waste = l.cap - supply
            all.append([ l , supply , waste , t_dis])
    # return an array with [loc , energy , wasted , dis]

    return sorted(all , key = lambda x : x[1])

def storage_opt(exceeding , storable ,  ENERGY_BOOK , loss_of_energy):
    STORAGE_MET = False

    for st in storable:
        close = closest_store(st , exceeding , loss_of_energy)
        close.sort(key = lambda x : ( - x[1] / (x[2] + 1) ,x[1]))

        for c in close:
            e , supply , waste , dis = c

            st.net += supply  * ((1 - loss_of_energy) ** dis)  
            print(loss_of_energy)
            print(supply , supply  * (1 - loss_of_energy) ** dis)
            e.net -= supply
            ENERGY_BOOK.append([supply ,st , e])

            if st.cap >= 0:
                break

            if e.cap <= 0:
                exceeding.remove(e)
        
        if st.cap < 0:
            #("not eneough space")
            ENERGY_BOOK.append([st.cap , "FAILED" , "STORE"])
            STORAGE_MET = False
            break

    for st in exceeding:
        if st.cap >= 0:
            ENERGY_BOOK.append(["PASS" , "PASS" , "STORE"])
        else:
            ENERGY_BOOK.append([st.cap , "FAILED" , "STORE"])

    return ENERGY_BOOK

def distance_m(start , goals , map):
    height , width = len(map) , len(map[0])
    queue = [start]
    run = True
    map = ([[1 for x in range(width + 2)]] + [([1] + map[y] + [1]) for y in range(height)] + [[1 for x in range(width + 2)]]).copy() 
    ptable(map)
                
def depth_first_search(poi , n , map, queue):
    poi_i = []
    if map[poi[1] + 1][poi[0]] == 0:
        map[poi[1] + 1][poi[0]] = n
        queue.append([poi[0],poi[1] + 1])
    if map[poi[1] - 1][poi[0]] == 0:
        map[poi[1] - 1][poi[0]] = n
        queue.append([poi[0],poi[1] - 1])
    if map[poi[1]][poi[0] + 1] == 0:
        map[poi[1]][poi[0] + 1] = n
        queue.append([poi[0] + 1,poi[1]])
    if map[poi[1]][poi[0] - 1] == 0:
        map[poi[1]][poi[0] - 1] = n
        queue.append([poi[0] - 1,poi[1]])
    
    elif map[poi[1] + 1][poi[0]] != 1:
        map[poi[1] + 1][poi[0]] = n
    elif map[poi[1] - 1][poi[0]] != 1:
        map[poi[1] - 1][poi[0]] = n
    elif map[poi[1]][poi[0] + 1] == 1:
        map[poi[1]][poi[0] + 1] = n
    elif map[poi[1]][poi[0] - 1] == 1:
        map[poi[1]][poi[0] - 1] = n
    


def map(width , height , all_loc):
    map = [[0 for x in range(width)] for y in range(height)]
    for l in all_loc:
        for poi in l.poi:
            map[poi[1]][poi[0]] = l
    return map
# code
def run(width , height , all_loc , ENERGY_BOOK):
    table = [[0 for x in range(width)] for y in range(height)]

    queue = sorted(all_loc ,key = lambda loc : -loc.rep())

    """
    #("sum of all values is" , all_net(all_loc) , "\n")
    ptable(poi(all_loc,table))
    #("\n", queue)
    """
    # temp
    loss_of_energy = 0.9 # 98 % remains

    energy_opt(queue , ENERGY_BOOK , loss_of_energy)
    return ENERGY_BOOK


# remove this later
"""
house1 = loc([[3,2]] , 0 , 100 , 0 , "house")
hos1 = loc([[6,3]] , 0 , 10 , 100 , "hospital")

solar1 = loc([[5,5]] , 10 , 1 , 1 , "solar")
hydro = loc([[4,5]], 1 , 100 , 1 , "hydro")

store = loc([[8,1]] , 0 , 10 , 100, "store")

all_loc = [house1 , solar1 , hos1 , hydro , store]

map = map(10 , 10 , all_loc)
distance([0,0], [5,3], map)

print()

"""