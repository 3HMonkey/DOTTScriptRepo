using System.Collections.Generic;
using System.Linq;

public static class HealPets
{
    //SETUP AREA
    //===========================================================
    //===========================================================
    static int Delay = 4500; // Delay in Milliseconds
    //===========================================================
    static ObjectId[] PetList = new ObjectId[]{
        0x0007DE2F, //META DRAGON serial
        0x0014A8F9 //White Wyrm serial
    };
    //=========================================================== 
    //===========================================================

    private static List<Mobile> MyPets = new List<Mobile>();

    public static void Run()
    {
        //loops until toggled or error
        while (true)
        {
            Misc.Wait(200);

            //Adding each pet which we defined above to the MyPet-list.
            foreach (var element in PetList)
            {
                MyPets.Add(Mobiles.CurrentMobiles.Get(element));
            }

            //Check if we have damaged pets and save them in the variable "damagedPets"
            var damagedPets = MyPets.FindAll(x => x.CurrentHealth < x.MaxHealth);
            //Check if "damagedPets" variable count is higher than 0
            if (damagedPets.Count > 0)
            {
                // Gets the most damaged pet out of the damaged pet list by calculating their percentages from high to low
                var mostdamagedPet = damagedPets.OrderByDescending(x => (x.CurrentHealth / x.MaxHealth)).FirstOrDefault();

                //Gets all bandages in backpack
                var potencialBandages = Items.CurrentItems.Matching(Items.Item.Bandage).InBackPack(true);
                //If there are no bandages stop script
                if (!potencialBandages.Any())
                {
                    Misc.ClientPrint("Heal pet disabled! No Bandages found", Misc.Colors.Red);
                    UO.CommandHandler.Terminate("healpet");
                }

                var bandages = potencialBandages.First();

                //If bandages < 10 then print a message above character.
                if (bandages != null && bandages.Amount < 10)
                {
                    Misc.ClientPrint($"Care bandages amount is: {bandages.Amount}", Player.Self, Misc.Colors.Yellow);
                }

                //Checks the distance and tells you to stay closer to the pet if > 2
                if (Player.Self.GetDistance(mostdamagedPet) > 2)
                {
                    Misc.ClientPrint($"Please stay closer to the pet: {mostdamagedPet.Name}!", Player.Self, Misc.Colors.Yellow);
                }

                //HEAL-ROUTINE
                //==================
                Player.TryUse(Items.Item.Bandage);
                Targets.WaitTargetObject(mostdamagedPet);
                //==================

                Misc.Wait(Delay);

            }
            MyPets.Clear();

        }


    }

    public static void Enable()
    {
        Misc.ClientPrint("Heal pet enables!", Misc.Colors.Green);
        UO.CommandHandler.Invoke("healpet");

    }

    public static void Disable()
    {
        Misc.ClientPrint("Heal pet disabled!", Misc.Colors.Red);
        UO.CommandHandler.Terminate("healpet");
    }

    public static void Toggle()
    {
        if (UO.CommandHandler.IsCommandRunning("healpet"))
            Disable();
        else
            Enable();
    }





}

//IGNORE THIS 
Commands.RegisterBackgroundCommand("healpet", HealPets.Run);
//JUST USE THE COMMAND BELOW AND SET A HOTKEY ON SAY "#healpet-toggle".
//Means pushing it enables the routine and pushing it again disables the routine
Commands.RegisterCommand("healpet-toggle", HealPets.Toggle);
