import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt 
import seaborn as sns

dataframe_of_all = pd.read_csv("CollegeBasketballPlayers2009-2021.csv")
dataframe_of_drafted = pd.read_excel("DraftedPlayers2009-2021.xlsx")
players_2022_csv = pd.read_csv("CollegeBasketballPlayers2022.csv")

dataframe_of_all = dataframe_of_all.drop(["team","conf","type"], axis=1)
dataframe_of_all = dataframe_of_all.dropna(axis='columns')

data = pd.DataFrame({"player_name":[],"GP":[],"Min_per":[],"Ortg":[],"usg":[],"eFG":[],"TS_per":[],"ORB_per":[],"DRB_per":[],
"AST_per":[],"TO_per":[],"FTM":[],"FTA":[],"FT_per":[],"twoPM":[],"twoPA":[],"twoP_per":[],"TPM":[],"TPA":[],"TP_per":[],
"blk_per":[],"stl_per":[],"ftr":[],"porpag":[],"adjoe":[],"pfr":[],"year":[],"pid":[]})

colunm_list = ["GP","Min_per","Ortg","usg","eFG","TS_per","ORB_per","DRB_per","AST_per","TO_per","FTM",
"FTA","FT_per","twoPM","twoPA","twoP_per","TPM","TPA","TP_per","blk_per","stl_per","ftr","porpag","adjoe",
"pfr","pid","year"]

drafted_players_name = []
drafted_players_year = []
drafted_players_overallPick = []
for i in range(1,781):    #appends drafted players name/year/overall to lists
    drafted_players_name.append(dataframe_of_drafted["PLAYER"][i])
    drafted_players_year.append(dataframe_of_drafted["YEAR"][i])
    drafted_players_overallPick.append(dataframe_of_drafted["OVERALL"][i])

drafted_players_overallPick_sorted = []
for i in range(61060):    #creates new dataframe that has only drafted players statistics
    p_name=dataframe_of_all["player_name"][i]
    p_year=int(dataframe_of_all["year"][i])
    for j in range(len(drafted_players_name)):
        if p_name == drafted_players_name[j] and p_year == int(drafted_players_year[j]):       
            data = pd.concat([data, dataframe_of_all.loc[i]], ignore_index = True, axis = 1)
            drafted_players_overallPick_sorted.append(drafted_players_overallPick[j])
            break

data = data.swapaxes("index", "columns")  #swaps index/colunms
data = data.dropna(axis = "index")

fact = 6
correlation_coefficient_list = []
for i in colunm_list:                     #calculates correlation
    temp_list = []
    for j in range(28,630):
        temp_list.append(data[i][j])
    
    df = pd.DataFrame({
        "a":drafted_players_overallPick_sorted,  
        "b":temp_list 
        })
    sxy = df.cov()["a"]["b"]
    sx = df["a"].std()
    sy = df["b"].std()
    rxy = -(sxy/(sx*sy))*fact
    correlation_coefficient_list.append([i,rxy])

players_2022_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
for i in range(3978):        #appends 2022's player names
    players_2022_list[0].append(players_2022_csv["player_name"][i])
count = 0
for i in colunm_list:        #appends 2022's player statistics
    count+=1
    for j in range(3978):
        players_2022_list[count].append(players_2022_csv[i][j]) 

mean_list_2022 = []
for i in range(1,len(players_2022_list)):  #appends 2022's player statistics mean
    nplist = np.array(players_2022_list[i])
    mean_list_2022.append(nplist.mean())

correlation_calculated = []  
for i in range(len(correlation_coefficient_list)):  #created a method for better regression results
    we = correlation_coefficient_list[i][1]
    if we < 0:
        sign = -1
    else:
        sign = +1
    correlation_calculated.append(we*we*sign)

mean_calculated_2022 = []
for i in range(3978):    #player statistics / player statistics mean
    temp_list_ = []
    for j in range(27):
        t = mean_list_2022[j]
        t1 = players_2022_list[j+1][i]
        if t1 > t:
            qw = t1/t
        else:
            qw = (t1/t)-1
        temp_list_.append(qw)
    mean_calculated_2022.append(temp_list_)

player_scores = []
for i in range(3978):  #regression calculation
    count = 0
    for j in range(27):
        count += mean_calculated_2022[i][j] * correlation_calculated[j]
    player_scores.append(count)

count = 0
x = 0
print("\n___________________________________________2022 RANDOM PLAYER SCORES___________________________________________________\n")
for i in range(144):
    count+=1
    x+= i
    a = random.randint(0,len(player_scores))
    print(round(player_scores[a],2),end="\t|\t")
    if count % 8 == 0:
        print("") 



drafted_2022_list = []
count = 0
print("\n________________________________________2022 GUESSED PLAYER SCORES______________________________________________\n")
for i in range(60):   #picks most scored players from list and appends to another list
    index = player_scores.index(max(player_scores))
    count+=1
    print(f"{count}:",round(player_scores[index],2),end="\t|\t")
    if count % 5 == 0:
        print("")
    player_scores[index] = -99
    drafted_2022_list.append(players_2022_list[0][index])

count = 0                                   
print(" _______________________________________________________________________________________________________________")
print("|                                                                                                               |")
print("|                                        CORRELATION COEFFICENT                                                 |")
print("|_______________________________________________________________________________________________________________|")
for i in correlation_coefficient_list:
    x = round(i[1],2)
    if x >= 0.7:
        a = "high"
    elif x >= 0.3:
        a = "medium"
    elif x >= 0:
        a = "low"
    elif x >= -0.3:
        a = "(-)low"
    elif x >= -0.7:
        a = "(-)medium"
    else:
        a = "(-)high"
    count+=1
    str_listlow = ["GP","ftr","eFG","FTM"]
    str_listhigh = ["Min_per"]
    if i[0] in str_listlow:
        q = "\t\t\t"
    elif i[0] in str_listhigh:
        q = "\t"
    else:
        q = "\t\t"
    print(f"|   ({i[0]}: {x} / {a})",end=q)  
    if count % 3 == 0:
        print("") 
print("|_______________________________________|_______________________________________|_______________________________|")

print("##########\n#############\n##########")

print(" _______________________________________________________________________________________")
print("|                                                                                       |")
print("|                                 2022 DRAFT GUESSES                                    |")
print("|_______________________________________________________________________________________|")
count = 0
for i in drafted_2022_list:
    count+=1
    countlist = [3,19,22,25,28,58,10,16,8,11,14,20,44,53,21,24,30,33,45]
    if count in countlist:
        q = "\t\t|\t"
    else:
        q = "\t|\t"
    print(f"{count}: {i}",end=q)
    if count % 3 == 0:
        print("")       
print("|_______________________|_______________________________|_______________________________|")


plt.figure(figsize = (12,9))
sns.heatmap(dataframe_of_all.corr(), vmax = 0.9, square = True)
plt.title("2009-2021 PLAYERS CORRELATION")
plt.show()

