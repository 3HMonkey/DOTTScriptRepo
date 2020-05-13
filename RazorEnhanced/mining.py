#mining macro - currently only tested on orc cave rail
#init modules and vars
#
import math
import datetime
#do you want to work smithing at same time? if yes, then true.
smithing = False
#runebook serial
runebook = 0x4102c6ae
#runebook bank rune gump location, use inspector to find
townrunebookgump = 11
#runebook mining rune gump location, use inspector to find
miningrunebookgump = 5
#bank bag serial
bankbag = 0x40e9e4e1
#bank reg bag
bankregbag = 0x4205b75d

#mine tile youre standing on
def mine(shovel):
    Journal.Clear()
    while True:
        smelt()
        if Player.Weight > 360:
            break
        Items.UseItem(shovel)
        Target.WaitForTarget(5000)
        Target.TargetExecute(Player.Position.X, Player.Position.Y, Player.Position.Z)
        Misc.Pause(1500)
        if Journal.Search("There is no metal here to mine") or Journal.Search("You have worn out your tool!"):
            Journal.Clear()
            break
        if Player.IsGhost:
            dead()

#move to next location
def move(cloc, loc):
    x = int(loc.strip("\n()").replace(" ", "").split(",")[0])
    y = int(loc.strip("\n()").replace(" ", "").split(",")[1])
    z = int(loc.strip("\n()").replace(" ", "").split(",")[2])
    localcloc = cloc
    retrycount = 0
    #check current location against requested location
    while str(localcloc) != str(loc):
        localcloc = str(Player.Position)
        Player.PathFindTo(x, y, z)
        Misc.Pause(1000)
        retrycount = retrycount + 1
        #dont get stuck trying to get there forever
        if retrycount > 5:
            break

#smelt ore to save weight
def smelt():
    findore()
    while Items.BackpackCount(0x19b9, -1) != 0:
        ore = Items.FindByID(0x19b9, -1, Player.Backpack.Serial)
        Items.UseItem(ore)
        Misc.Pause(750)
        if Journal.Search("You are not near a forge"):
            Journal.Clear()
            break

#makes move shovels and kits
def kit(tool):
    Misc.SendMessage("getting tool", 0)
    #find kit
    kit = Items.FindByID(0x1eb8, -1, Player.Backpack.Serial)
    #make kit if running low
    while Items.BackpackCount(0x1EB8, -1) < 3:
        Misc.SendMessage("making kit", 0)
        Items.UseItem(kit)
        Gumps.WaitForGump(949095101, 700)
        Gumps.SendAction(949095101, 8)
        Gumps.WaitForGump(949095101, 700)
        Gumps.SendAction(949095101, 23)
        Misc.Pause(1500)
        Gumps.SendAction(949095101, 0)
        Gumps.SendAction(949095101, 0)
        if Player.IsGhost:
            dead()
    Gumps.SendAction(949095101, 0)
    #make shovel
    if tool == "shovel":
        while Items.BackpackCount(0xf39) < 2:
            Misc.SendMessage("making shovel", 0)
            Items.UseItem(kit)
            Gumps.WaitForGump(949095101, 700)
            Gumps.SendAction(949095101, 8)
            Gumps.WaitForGump(949095101, 700)
            Gumps.SendAction(949095101, 72)
            Misc.Pause(1500)
            Gumps.SendAction(949095101, 0)
            Gumps.SendAction(949095101, 0)
            if Player.IsGhost:
                dead()
        return Items.FindByID(0xf39, -1, Player.Backpack.Serial)
    Gumps.SendAction(949095101, 0)
    #make tongs
    if tool == "tongs":
        while Items.BackpackCount(0xfbb) < 2:
            Misc.SendMessage("making tongs", 0)
            Items.UseItem(kit)
            Gumps.WaitForGump(949095101, 700)
            Gumps.SendAction(949095101, 8)
            Gumps.WaitForGump(949095101, 700)
            Gumps.SendAction(949095101, 86)
            Misc.Pause(1500)
            Gumps.SendAction(949095101, 0)
            Gumps.SendAction(949095101, 0)
            if Player.IsGhost:
                dead()
        return Items.FindByID(0xfbb, -1, Player.Backpack.Serial)
    Gumps.SendAction(949095101, 0)

#find shovel
def shovel():
    if Items.BackpackCount(0xf39, -1) == 0:
        shovel = kit("shovel")
        return shovel
    else:
        shovel = Items.FindByID(0xf39, -1, Player.Backpack.Serial)
        return shovel

#bank loot when getting full
def bank(x, y):
    global townrunebookgump, miningrunebookgump
    #recall to bank
    if Player.Position.X != 1435 and Player.Position.Y != 1679:
        while Player.Position.X == x and Player.Position.Y == y:
            Items.UseItem(runebook)
            Gumps.WaitForGump(1431013363, 700)
            Gumps.SendAction(1431013363, townrunebookgump)
            Misc.Pause(1000)
    
    #move warez over
    loots = [0x1bf2, 0xf16, 0xf10, 0xf25, 0xf26, 0xf2d, 0xf21, 0xf15, 0xf19, 0xf13]
    Player.ChatSay(0, 'bank')
    for i in loots:
        while Items.BackpackCount(i, -1):
            item = Items.FindByID(i, -1, Player.Backpack.Serial)
            Items.Move(item.Serial, bankbag, 0)
            Misc.Pause(500)
    while Items.BackpackCount(0xeed, -1) > 0:
        gold = Items.FindByID(0xeed, -1, Player.Backpack.Serial)
        Items.Move(gold.Serial, Player.Bank, 0)
        Misc.Pause(500)
    while Items.BackpackCount(0x141B, -1) > 0:
        helm = Items.FindByID(0x141B, -1, Player.Backpack.Serial)
        Items.Move(helm.Serial, Player.Bank, 0)
        Misc.Pause(500)

    #restock
    regs = [0xf86, 0xf7a, 0xf7b]
    for i in regs:
        while Items.BackpackCount(i, -1) < 6:
            reg = Items.FindByID(i, -1, bankregbag)
            Items.Move(reg.Serial, Player.Backpack.Serial, 4)
            Misc.Pause(500)

    #restock after dead
    if Player.GetItemOnLayer('Head') == None:
        #mask
        while Player.GetItemOnLayer('Head') == None:
            mask = Items.FindByID(0x141B, -1, Player.Bank.Serial)
            Player.EquipItem(mask)
            Misc.Pause(1000)

        #bootstrap tink kit
        while Items.BackpackCount(0x1EB8, -1) == 0:
            kit = Items.FindByID(0x1eb8, -1, bankbag)
            Items.Move(kit, Player.Backpack.Serial, 0)
            Misc.Pause(1000)

        #bootstrap ore
        while Items.BackpackCount(0x1BF2, 0) == 0:
            kit = Items.FindByID(0x1BF2, 0, bankbag)
            Items.Move(kit, Player.Backpack.Serial, 30)
            Misc.Pause(1000)

    #current bank locaiton to check for successful recall
    bx = Player.Position.X
    by = Player.Position.Y
    while Player.Position.X == bx and Player.Position.Y == by:
        Items.UseItem(runebook)
        Gumps.WaitForGump(1431013363, 700)
        Gumps.SendAction(1431013363, miningrunebookgump)
        Misc.Pause(1000)

#find ore on ground(why not, free ore)
def findore():
    fil = Items.Filter()
    fil.Enabled = True
    fil.Name = 'ore'
    fil.RangeMax = 2
    fil.OnGround = 1
    ore = Items.ApplyFilter(fil)
    if ore is not None:
        for o in ore:
            nummoveable = math.floor((Player.MaxWeight - Player.Weight) / 12)
            Items.Move(o, Player.Backpack.Serial, nummoveable)
            Misc.Pause(750)



#not needed now, will add some defence logic later
def fight():
    pass

#work your blacksmithing
#didnt write this script till after GM so I dont
#have the skill breakpoints for lower than 100
def smith():
    skill = Player.GetSkillValue('Blacksmith')
    if skill < 106.4:
        makegump = 16
        ingotcost = 10
    if skill >= 106.4 and skill < 108.9:
        makegump = 9
        ingotcost = 12
    if skill >= 108.9 and skill < 116.3:
        makegump = 2
        ingotcost = 18
    if skill >= 116.3 and skill < 118.8:
        makegump = 23
        ingotcost = 20
    if skill >= 118.8:
        makegump = 30
        ingotcost = 25
    while Items.BackpackCount(0x1bf2, 0) >= ingotcost + 10:
        startingot = Items.BackpackCount(0x1bf2, 0)
        tongs = kit(tool="tongs")
        Misc.SendMessage("found tongs, making " + str(makegump), 0)
        Items.UseItem(tongs)
        Gumps.WaitForGump(949095101, 3000)
        Gumps.SendAction(949095101, 22)
        Gumps.WaitForGump(949095101, 3000)
        Gumps.SendAction(949095101, makegump)
        Misc.Pause(2500)
        Gumps.SendAction(949095101, 0)
        if Player.IsGhost:
            dead()
        #not near a forge/anvil, dont get stuck forever
        if startingot == Items.BackpackCount(0x1bf2, 0):
            break
        #recycle your items, still need item IDs for all levels, gorget, gloves and arms so far.
        bsitems = [0x1413, 0x1414, 0x1410, 0x1411, 0x1415]
        for i in bsitems:
            while Items.BackpackCount(i, -1) > 0:
                if Player.IsGhost:
                    dead()
                startingot = Items.BackpackCount(0x1bf2, 0)
                tongs = kit(tool="tongs")
                Items.UseItem(tongs)
                Gumps.WaitForGump(949095101, 3000)
                Gumps.SendAction(949095101, 14)
                Misc.Pause(1000)
                Target.TargetExecute(Items.FindByID(i, -1, -1))
                Misc.Pause(1000)
                if startingot == Items.BackpackCount(0x1bf2, 0):
                    break
                Gumps.SendAction(949095101, 0)
    Gumps.SendAction(949095101, 0)
    Gumps.SendAction(949095101, 0)

#dead
def dead():
    if Player.IsGhost:
        file = "tree_locs_moon2.txt"
        f = open(file, "a")
        f.write(datetime.datetime.now() +"\n")
        f.close()
    while Player.IsGhost:
        linecount = 0
        while Gumps.CurrentGump() == 523845830:
            Gumps.SendAction(523845830, 1)
            Misc.Pause(500)
        for line in loclist_od:
            linecount = linecount + 1
            cloc = str(Player.Position)
            loc = line
            Misc.SendMessage(str(linecount)+ ". " + line, 0)
            move(cloc, loc)
            Gumps.SendAction(2957810225, 1)
            while Player.Position.Y == 1611:
                Gumps.SendAction(2957810225, 1)
                for f in range(2):
                    Player.Walk('West')
                for f in range(2):
                    Player.Walk('East')
                while not Player.IsGhost:
                    linecount = 0
                    for line in loclist_ob:
                        linecount = linecount + 1
                        cloc = str(Player.Position)
                        loc = line
                        Misc.SendMessage(str(linecount)+ ". " + line, 0)
                        move(cloc, loc)
                    bank(Player.Position.X, Player.Position.Y)
                    break


#Main script
#load rail
with open('orc_cave.txt', 'r') as file:
    loclist = file.read().splitlines()
file.close()

with open('orc_cave_dead.txt', 'r') as file:
    loclist_od = file.read().splitlines()
file.close()

with open('brit_portal_dead.txt', 'r') as file:
    loclist_ob = file.read().splitlines()
file.close()

#run program
#while not Player.IsGhost:
while True:
    linecount = 0
    for line in loclist:
        if Player.IsGhost:
            dead()
        linecount = linecount + 1
        cloc = str(Player.Position)
        loc = line
        if Player.Weight > 330 and Items.BackpackCount(0x19b9, -1) == 0:
            bank(Player.Position.X, Player.Position.Y)
        if Player.Position.X == 1435 and Player.Position.Y == 1679:
            bank(Player.Position.X, Player.Position.Y)
        Misc.SendMessage(str(linecount)+ ". " + line, 0)
        move(cloc, loc)
        mine(shovel=shovel())
        if smithing:
            smith()