# Infusion Scripts

Todo:

- Write readme :)
- add initial scripts

Point these scripts in a "startup.csx" file like:
```
//Load scripts
#load "UOScripts\HealPets.csx"
#load "UOScripts\DropOffStuff.csx"

using System;

Misc.Log("\nWrite ,help and press enter if you want get information about all available commands.\n" +
"Write ,edit and press enter to open the built-in script editor.\n\n" +
"Your character says text that you enter on command line and that doesn't start with a comma.\n\n" +
"In console you can use these keyboard shortcuts:\n" +
 " - esc to clear command line\n" +
 " - page up, page down, ctrl+home, ctrl+end, up, down to scroll the console content\n" +
 " - alt+up, alt+down to navigate command line history\n" +
 " - tab to autocomplete a command on the command line\n\n\n" +
    "For more information about Infusion take a look at " +
    "https://github.com/uoinfusion/Infusion/wiki."
);



UO.ClientFilters.Light.Enable();
UO.ClientFilters.Weather.Enable();
```
