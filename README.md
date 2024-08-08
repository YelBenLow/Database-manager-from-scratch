# HU: Adatbázis-kezelő teljesen a nulláról
### (A program 100%-ban python nyelven íródott, a Github hibásan ismeri fel a .exe fájl miatt.)
# EN: Database-Manager from Scratch
### (The program is 100% written in Python, GitHub incorrectly recognizes it due to the .exe file.)

## English version below!!
Ezt a projektet egy régi emlékem inspirálta, amit évekkel ezelőtt konzolos verzióban programoztam le, majd később GUI verzióban, ami ebben a repoban is benne van.

Tehát, ez egy olyan adatbázis-kezelő "szoftver", mely GUI felülettel rendelkezik, és amit teljesen a nulláról írtam meg.

Itt az "adatbázisok" egyenlőek a mappákkal, a "táblák" egyenlőek .txt fájlokkal. (Ezáltal a táblák tartalmát manuálisan is fel lehet tölteni, módosítani.)

A projektemben néhány jelentősebb lib, modul ami felhasználásra került:
- Tkinter, customtkinter
- Pillow
- Shutil
- Subprocess

A kezelőt evidensen a Database.py megnyitásával lehet elindítani.
HA teszt-adatbázisokkal szeretnéd tesztelni a szoftveremet, akkor indítsd el a _generate_test_databases.py fájlt, mely generálni fog neked "random" adatbázisokat.

Ajánlott 1920x1080-as vagy nagyobb monitorral futtatni a kódot a torzulások elkerülése érdekében!

!! Mivel hobbi-projekt és tanulási céllal készítettem ezt a "szoftvert", ezért lesznek a kódban optimalizálatlan, miaf*sz? részek. !!

## NEM FIXÁLT (LOGIKAI) HIBA(-ÁK)
Lekérdezésnél csak előre lehet írni az OR feltételt, majd utána az AND feltételeket.<br>
pl.: Hibát kapsz ennél: (feltétel1 OR feltétel2) AND (feltétel3 OR feltétel4);<br>
De ennél nem: (feltétel1 OR feltétel2 OR feltétel3) AND feltétel4 AND feltétel5;

## ISMERT LIMITEK
1. 9db adatbázis megjelenítésére képes jelenleg a programom.<br>
2. 10db tábla megjelenítésére képes jelenleg a programom, per adatbázis.

### Megjegyzés
Ha több adatbázist, táblát hozol létre mint a limit, nem lesz hiba, csak elcsúszva - esetleg torzulva fog megjelenni a vizualizálás.

## Exe version mappa
Ha nem akarsz bajlódni a libek, modulok telepítgetésével, akkor csak ezt a mappát töltsd le, és ugyanúgy tesztelheted a programom.

# English Version
This project was inspired by an old memory of mine, which I programmed years ago in a console version, and later in a GUI version, which is also included in this repo.

So, this is a database management "software" that has a GUI interface and which I wrote entirely from scratch.

Here, "databases" are equivalent to folders, and "tables" are equivalent to .txt files. (Therefore, the contents of the tables can be manually uploaded and modified.)

Some of the major libraries and modules used in my project include:
- Tkinter, customtkinter
- Pillow
- Shutil
- Subprocess

The database-manager can be started by opening the Database.py file.
If you want to test my software with test databases, you should run the _generate_test_databases.py file, which will generate "random" databases for you.

It is recommended to run the code on a monitor with a resolution of 1920x1080 or larger to avoid distortions!

!! Since this is a hobby project and I created this "software" for learning purposes, there will be unoptimized, "what-the-heck?" parts in the code. !!

## UNFIXED (LOGICAL) BUG(S)
When querying, the OR condition can only be written first, followed by AND conditions.<br>
e.g., You will get an error with this: (condition1 OR condition2) AND (condition3 OR condition4);<br>
But not with this: (condition1 OR condition2 OR condition3) AND condition4 AND condition5;

## KNOWN LIMITATIONS
1. My program currently supports displaying up to 9 databases.<br>
2. My program currently supports displaying up to 10 tables per database.

### Note
If you create more databases or tables than the limit, there won't be an error, but the visualization may appear shifted or distorted.

## Exe version folder
If you don't want to bother with installing the libraries and modules, just download this folder, and you can test my program the same way.
