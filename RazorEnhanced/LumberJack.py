#init vars
TreeStaticID = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]
rscoord = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1],[-2,-2],[-2,2],[2,-2],[2,2]]
#do you want to skill feltching? set to true
Fletch = True
#bag in bank to put logs, can just set to Player.Bank.Serial for root of bank
logbag = 0x4065b7bd
#bag in bank where bow tools are, not needed if not fletching
fletchtool = 0x429BD1EA
#bow serials
xbow = 0x0F50
hxbow = 0x13FD


#chop the wood
def Chop(Axe, x, y, z, tid):
    Target.Cancel()
    Misc.Pause(200)
    Items.UseItem(Axe)
    Target.WaitForTarget(1000,False)
    Target.TargetExecute(x, y, z, tid)
    Misc.Pause(4000)
    Attack()
    Healz()

#find da treez
def FindTile():
    global Axe
    for rec in rscoord:
        x = Player.Position.X + rec[0]
        y = Player.Position.Y + rec[1]
        z = Player.Map
        tile = Statics.GetStaticsTileInfo(x, y, z)
        for f in tile:
            if f.StaticID in TreeStaticID:
                Chop(Axe, x, y, f.StaticZ, f.StaticID)

#equip da Axzor
def EquipAxe():
    if not Player.CheckLayer("LeftHand"):
        #Axe = Items.FindByID(0x0F43, -1, -1)
        Axe = Items.FindByID(0x0F4B, -1, -1)
        Player.EquipItem(Axe)
        Misc.Pause(1000)
        return Axe
    else:
        Axeitem = Player.GetItemOnLayer("LeftHand")
        Axe = Axeitem.Serial
        return Axe

#I like to move it, move it, MOVE it!
def Pf(cloc, loc):
    x = int(loc.strip("\n()").replace(" ", "").split(",")[0])
    y = int(loc.strip("\n()").replace(" ", "").split(",")[1])
    z = int(loc.strip("\n()").replace(" ", "").split(",")[2])
    localcloc = cloc
    retrycount = 0
    while str(localcloc) != str(loc):
        localcloc = str(Player.Position)
        Player.PathFindTo(x, y, z)
        Misc.Pause(750)
        retrycount = retrycount + 1
        if retrycount > 7:
            break

#smack dat bitch up
def Attack():
    if (Player.Hits < Player.HitsMax):
        fil = Mobiles.Filter()
        fil.Enabled = True
        fil.Name = 'serpent'
        Player.SetWarMode(True)
        Healz()
        Misc.Pause(250)
        while not Items.FindByID(0x2006, -1, -1) and Mobiles.ApplyFilter(fil):
            moblist = Mobiles.ApplyFilter(fil)
            mob = moblist[0]
            Player.Attack(mob)
            Player.PathFindTo(mob.Position.X, mob.Position.Y, mob.Position.Z)
            Misc.Pause(500)
            Healz()
            Misc.Pause(250)
    Misc.Pause(1500)
    loot()

#stayin alive
def Healz():
    if (Player.Hits < Player.HitsMax):
        Items.UseItemByID(0x0E21, -1)
        Misc.Pause(250)
        Target.Self()



#hoard the l00tz
def loot():
    corpse = Items.FindByID(0x2006, -1, -1)
    if corpse is not None:
        Items.UseItem(corpse.Serial)
        Misc.Pause(1000)
        gold = Items.FindByID(0x0eed, -1, corpse.Serial)
        if gold is not None:
            Items.Move(gold.Serial, 0x4065b79e, 0)
            Misc.Pause(1000)
        logs = Items.FindByID(0x1bdd, -1, corpse.Serial)
        if logs is not None:
            Items.Move(logs.Serial, 0x4065b79e, 0)
            Misc.Pause(1000)
    Player.SetWarMode(False)

#make bows
def fletch():
    while Items.BackpackCount(0x1bdd, 0) > 9 and Items.BackpackCount(0x1022, 0) > 0:
        Attack()
        tool = Items.FindByID(0x1022, -1, Player.Backpack.Serial)
        if Player.GetSkillValue('Fletching') < 80:
            Items.UseItem(tool)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 15)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 9)
            Gumps.SendAction(949095101, 0)
        else:
            Items.UseItem(tool)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 15)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 23)
            Gumps.SendAction(949095101, 0)
    Gumps.SendAction(949095101, 0)
    drop()

#lose weight fatty
def drop():
    while Items.BackpackCount(xbow, 0) > 0:
        bow = Items.FindByID(xbow, -1, Player.Backpack.Serial)
        if bow is not None:
            Items.MoveOnGround(bow, 1, Player.Position.X + 1, Player.Position.Y, Player.Position.Z)
            Misc.Pause(500)
        bow = Items.FindByID(xbow, -1, Player.Backpack.Serial)
        if bow is not None:
            Items.MoveOnGround(bow, 1, Player.Position.X, Player.Position.Y + 1, Player.Position.Z)
            Misc.Pause(500)
    while Items.BackpackCount(hxbow, 0) > 0:
        bow = Items.FindByID(hxbow, -1, Player.Backpack.Serial)
        if bow is not None:
            Items.MoveOnGround(bow, 1, Player.Position.X + 1, Player.Position.Y, Player.Position.Z)
            Misc.Pause(500)
        bow = Items.FindByID(hxbow, -1, Player.Backpack.Serial)
        if bow is not None:
            Items.MoveOnGround(bow, 1, Player.Position.X, Player.Position.Y + 1, Player.Position.Z)
            Misc.Pause(500)

#restock the tools and hoard the warez
def bank():
    global logbag, fletchtool, Fletch
    Player.ChatSay(0, 'bank')
    while Items.BackpackCount(0x1bdd, -1) != 0:
        log = Items.FindByID(0x1bdd, -1, Player.Backpack.Serial)
        Items.Move(log.Serial, logbag, 0)
        Misc.Pause(500)
    while Items.BackpackCount(0x0eed, -1) != 0:
        gold = Items.FindByID(0x0eed, -1, Player.Backpack.Serial)
        Items.Move(gold.Serial, Player.Bank, 0)
        Misc.Pause(500)
    while Items.BackpackCount(0x0e21, -1) < 20:
        aid = Items.FindByID(0x0e21, -1, Player.Bank.Serial)
        Items.Move(aid.Serial, Player.Backpack.Serial, 20 - Items.BackpackCount(0x0e21, -1))
        Misc.Pause(500)
    if Fletch:
        Items.UseItem(fletchtool)
        while Items.BackpackCount(0x1022, -1) < 5 and Items.ContainerCount(fletchtool, 0x1022, -1) != 0:
            tool = Items.FindByID(0x1022, -1, fletchtool)
            Items.Move(tool.Serial, Player.Backpack.Serial, 1)
            Misc.Pause(750)
    if Items.BackpackCount(0x1022, -1) == 0:
        Fletch = False


#Main script
#load rail
with open('tree_locs_moon2.txt', 'r') as file:
    loclist = file.read().splitlines()
file.close()

#run program
while not Player.IsGhost:
    linecount = 0
    for line in loclist:
        linecount = linecount + 1
        cloc = str(Player.Position)
        loc = line
        Axe = EquipAxe()
        Misc.SendMessage(str(linecount)+ ". " + line, 0)
        Pf(cloc, loc)
        FindTile()
        Misc.Pause(500)
        Attack()
        if Player.GetSkillValue('Fletching') == 100:
            Fletch = False
        if Fletch:
            fletch()
    bank()
