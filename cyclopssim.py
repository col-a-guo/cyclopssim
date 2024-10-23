#Hero Variables
build_id = 0
level = 1
gold = 300
skilllag = 0.3
skillcds = [[8.5 for i in range(6)], [14-i*0.8 for i in range(6)], [43 for i in range(3)]]
skilllevels = [[1,1,1,1,1,2,2,2,2,3,3,3,4,5,6],[0,1,2,2,3,3,4,4,5,5,6,6,6,6,6],[0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]]

multihit = [2,5,1] #number hit for cdr reasons
skilldmg = [[275+25*i for i in range(6)], [200+30*i for i in range(6)], [550,715,880]]
skillscaling = [.6, .5, 2.2]
AoE = [3, 4.108, 1] #number hit per cast; 4.108 represents 22% damage falloff after first hit

skillcount = [100000,100000,100000]
castcount = [0,0,0]

#Build Variables
base_cdr = [0.05, 0.10]
base_mp = [30, 30]
base_mpen = [10, 5]

#cd boots-book-lightning truncheon-genius wand-concentrated energy-holy crystal-magic pot
#vs
#cd boots-book-book of sages-genius wand-concentrated energy-holy crystal-divine glaive-magic pot
itemthresholds = [[710, 1870, 2250, 2000, 2020, 3000, 1500], [710, 1870, 450, 2000, 2020, 3000, 1730, 1500]]
itemMP1 = [[0, 50, 75, 75, 70, 185, 30],[0, 50, 8, 75, 70, 185, 52, 30]]
itemCD = [[0.10, 0.20, 0.10, 0, 0, 0, 0], [0.10, 0.20, 0.05, 0, 0, 0, -0.05, 10]]
itemnames = [["CDboots", "CDbook", "LT", "GW", "CE", "HC", "Mpot"],["CDboots", "CDbook", "BoS", "GW", "CE", "HC", "DG", "Mpot"]]

items_toggled = []

magicdamagemult = 1
mmultindex = 0 #for Concentrated Energy
LTcooldown = 0 #for Lightning Truncheon
six_hit_count_conc_energy = 0

damage_total = 0
healing = 0

update_flag = True

for milli in range(200000):
    #check for purchases
    LTcooldown -= 1
    for itemid, threshold in enumerate(itemthresholds[build_id]):
        goldcost = 0
        goldcost += itemthresholds[build_id][itemid]
        if gold > goldcost:
            magicpower += itemMP1[itemid]
            cdr += itemCD[itemid]
            if itemnames[itemid] not in items_toggled:
                items_toggled.append(itemnames[itemid])
                update_flag = True
    #check for levels
    if (milli+1)%6000 == 0:
        level+=1
        update_flag = True
    #update variables
    if update_flag == True:
        enemy_hp = level*100+2500
        enemy_mr = level*2.5+10
        mpen = base_mpen[build_id]
        cdr = base_cdr[build_id]
        magicpower = base_mp[build_id]+six_hit_count_conc_energy*5
        if "HC" in items_toggled:
            magicpower *= (1+.21+.01*level)
        if "GW" in items_toggled:
            mpen += 10
            mreduce = level*.9+9
        if "DG" in items_toggled:
            enemy_mr = enemy_mr*(.6-.001*enemy_mr)-mreduce
        update_flag = False
    for j in range(3):
        skillcount[j]+=1
        skilllevel = skilllevels[j]
        if skillcount[j] > skillcds[j][skilllevel]*1000*(1-cdr)+skilllag*1000:
            castcount[j] += 1
            if "DG" in items_toggled and LTcooldown <= 0:
                damage_total += 120*magicpower*120/(120+enemy_mr-mpen)*2
            else:
                LTcooldown = 6000
            if six_hit_count_conc_energy > 5:
                magicdamagemult = 1.12
                six_hit_count_conc_energy = 0
                mmultindex = 0
            if "CE" in items_toggled:
                if magicdamagemult == 1:
                    if j==2:
                        six_hit_count_conc_energy+=1
                    if j==1:
                        six_hit_count_conc_energy+=3
                    else:
                        six_hit_count_conc_energy+=2
                else:
                    mmultindex += 1

            skillcount[j] = 0
            damage_total += (skilldmg[j][skilllevel]+skillscaling[j]*magicpower)*120/(120+enemy_mr-mpen)*AoE[j]
            for skilli in range(3):
                for hit in range(multihit[j]):
                    skillcount[skilli] += 500
    if mmultindex > 5000:
        magicdamagemult = 1


print(castcount)
print(damage_total)
