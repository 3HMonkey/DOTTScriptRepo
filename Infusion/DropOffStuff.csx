using System.Collections.Generic;


public static class DropOffStuff
{
    
    public static List<ModelId> StuffToDrop = new List<ModelId>()
    {
        0x1b72, // BronzeShields
        0x1b73, // Buckler
        0x1b7b, // MetalShield
        0x1b74, // Metal Kite Shield
        0x1b79, // Tear Kite Shield
        0x1b7a, // WoodenShield
        0x1b76, // HeaterShield
        //Platemail
        0x1408, // Close Helmet
        0x1410, // Platemail Arms
        0x1411, // Platemail Legs
        0x1412, // Plate Helm
        0x1413, // Plate Gorget
        0x1414, // Platemail Gloves
        0x1415, // Plate Chest
        0x140a, // Helmet
        0x140c, // Bascinet
        0x140e, // Norse Helm
        //Chainmail
        0x13bb, // Chainmail Coif
        0x13be, // Chainmail Leggins
        0x13bf, // Chainmail Tunic
        //Ringmail
        0x13ee, // Ringmail Sleeves
        0x13eb, // Ringmail Gloves
        0x13ec, // Ringmail Tunic
        0x13f0, // Ringmail Leggins
        //Studded
        0x13da, // Studded Leggings
        0x13db, // Studded Tunic
        0x13d5, // Studded Gloves
        0x13d6, // Studded Gorget
        0x13dc, // Studded Sleeves
        //Leather
        0x13c6, // Leather Gloves
        0x13cd, // Leather Sleeves
        0x13cc, // Leather Tunic
        0x13cb, // Leather Pants
        0x13c7, // Leather Gorget
        0x1db9, // Leather Cap
        //Female Armor
        0x1c04, // Female Plate
        0x1c0c, // Female Studded Bustier
        0x1c02, // Female Studded Armor
        0x1c00, // Female Leather Shorts
        0x1c08, // Female Leather Skirt
        0x1c06, // Female Leather Armor
        0x1c0a, // Female Leather Bustier
        //Fencing
        0xf62,  // Spear
        0x1403, // Short Spear
        0xe87,  // Pitchfork
        0x1405, // Warfork
        0x1401, // Kryss
        0xf52,  // Dagger
        //Macing
        0x13b0, // War axe
        0xdf0,  // Black Staff
        0x1439, // War Hammer
        0x1407, // War Mace
        0xe89,  // Quarter Staff
        0x143d, // Hammer Pick
        0x13b4, // Club
        0xe81,  // Shepherds Crook
        0x13f8, // Gnarled Staff
        0xf5c,  // Mace
        0x143b, // Maul
        //Swords
        0x13b9, // Viking Sword
        0xf61,  // Longsword
        0x1441, // Cutlass
        0x13b6, // Scimitar
        0xec4,  // Skinning Knife
        0x13f6, // Butcher Knife
        0xf5e,  // Broadsword
        0x13ff, // Katana
        0xec3,  // Cleaver
        //Axes
        0xf43, // Hatchet
        0xf45, // Executioners Axe
        0xf4d, // Bardiche
        0xf4b,  // Double Axe
        0x143e, // Halberd
        0x13fb, // Large Battle Axe
        0x1443, // Two Handed Axe
        0xf47,  // Battle Axe
        0xf49,  // Axe
        0xe85,  // Pickaxe
        0xe86,  // Pickaxe
        //Bows
        0x13fd, // HeavyXbow
        0xf50,  // Xbow
        0x13b2, // bow
        0x26c2, // compbow
        //====================
        0x1081, // Leather
        0x26B4  // Scales
     };

    public static void Run()
    {
        //Promts a cursor and sets the container variable
        var containerToDrop = Items.AskForItem();
        //Sets player backpack as from container
        var fromContainer = Player.Backpack;

        //Do following for each item in backpack
        foreach (var item in Items.CurrentItems.InBackPack(true))
        {
            //Checks if list contains the current item
            if (StuffToDrop.Contains(item.Type))
            {
                //Moves item to target container
                Items.TryMoveItem(item, containerToDrop);
                Misc.Wait(50);
            }

        }
    }



}

Commands.RegisterCommand("dropoff", DropOffStuff.Run);