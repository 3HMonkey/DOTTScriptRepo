#Add this script to razorenhanced and bind it to a hot key.
#You can then run the rail you want to record and press
#the hotkey to record a point. This script is setup to
#append to a file, so you can add to an existing file
#if you start recording where you rail left off.
#
#name of rail file you want to write to
file = "tree_locs_moon2.txt"

f = open(file, "a")
f.write(str(Player.Position) +"\n")
f.close()
