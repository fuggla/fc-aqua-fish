# Aqua Fish

Experience what it's like to watch fish eat carrots! The latest release can be found [here](https://github.com/owlnical/fc-aqua-fish/releases).

A simulator by Furniture Corp.

## Roadmap

### v.1.x
- [ ] Introfilm?

### v1.0

- [ ] Någon form av exekverbar fil eller bibliotek för allmänheten ([såhär](http://arcade.academy/examples/pyinstaller.html) till win på något sätt?)
- [ ] Skippbar splashscreen med logga
- [ ] Fiskarna lägger rom som blir nya fiskar
- [ ] Fiskar kan äta upp andra fiskar
- [ ] Hitta balans mellan nyfödda fiskar och uppätna fiskar
- [ ] Styr en fisk och gör det som fiskarna gör?
- [ ] Alternativt mer interaktion med fiskarna?
- [ ] Menyer i form av valar som simmar in?

### v0.8
- [ ] Barnfiskar kläcks ur äggen. Växer upp efter ett tag
- [ ] Herrarna och damerna måste pussas innan damerna kan lägga ägg
  - [ ] De blir puss-redo när de är mätta
  - [ ] Någon form av animation då
  - [ ] Slumpad chans för ägg när de pussas
- [ ] Bubbla, slå eller putta fiskarna så att de ändrar riktning
- [ ] Snyggare muspekare?
- [ ] Ett system för att styra vilka föremål som visuellt är framför/bakom varandra

### v0.7
- [x] System för köttätande fisk
  - [x] En ny typ av fisk som äter andra fiskar
  - [x] Bytesfiskarna blir rädda och flyt när de är nära den
  - [x] Bytesfiskarna blir uppätna av hungriga köttätande fiskar
- [ ] Föremål i akvariet
  - [ ] Slumpat valda och utplacerade
  - [ ] Fruktväxt som det växer mat på
- [x] System för äggläggning 
  - [x] Fiskarna lägger ägg ifall de ätit mycket
  - [x] Tydliga ägg för blå och lila fiskarna (olika storlek)
  - [x] Endast damerna lägger ägg
  - [x] En ny fisk kläcks efter ett tag
- [ ] Mer info om fisken man köper
- [ ] Någon form av stack för meddelanden ("X dog av svält" etc)

### v0.6
- [x] Ätanimation
- [x] Dödsanimation
- [x] Snygga till sättet maten försvinner på
- [x] Namn på fiskar
- [x] Fiskarna påverkas av mat
  - [x] Fiskarna blir hungriga av att inte äta
  - [x] Fiskarna dör ifall de inte äter
- [x] Testa laddningstiden i setup
- [x] Luftbubblor
- [x] Fler knappar för att köpa fiskar och morötter
- [x] Resize av bakgrunden till skärmstorleken? (skulle bli snyggare på mina datorer)

### v0.5

- [x] Fiskar som simmar i stim
- [x] Hela programmet har en gemensam framerate (Fanns hela tiden)
- [x] Överklassfisk
- [x] Flera typer av fiskar
- [x] Flera möjligheter att sätta parametrar på nya fiskar
  - [x] Lägg in fiskarnas grundegenskaper i "vars"
  - [x] Möjlighet att skapa fisk och ställa in personlighet
  - [x] Möjlighet att skapa fisk och ställa in utseende
- [x] Överklassruta (kanske)
- [x] Fullscreen
- [x] Förslag: random färg på fisk (lägger in dem som input till fisken)
- [x] Bakgrundsbild

### v0.4

- [x] Slumpmässig spawn av maten
- [x] Maten sjunker i vattnet tills den når botten
- [x] Sand i botten
- [x] Maten droppas in ovanifrån
- [x] Fiskarna äter upp maten
- [x] Fiskarna riktar in sig mot maten
- [x] Klass för "flytande" fönster
- [x] Lägg pausmeny i eget fönster
- [x] Stäng fönster med `X`
- [x] Flytta fönster med musen?
- [x] Testa a merga en branch
- [x] Ett till fönster med andra funktioner?
  - [x] Köp fisk
  - [x] Köp FPS-räknare (mycket nödvändigt)
- [x] Ändra rörelsebeteendet från accelerationsbaserat till kraftbaserat

### v0.3

- [x] Game state (Running, Paused osv)
- [x] Pausemeny istället för knappar hela tiden
- [x] Ändra fiskarnas animation utifrån hastighet
- [x] Skapa ett objekt som fiskarna vill simma mot (bra till framtida behov)
- [x] Ändra rörelsemönster från hastighetsbasserat till accelerationsbaserat
- [x] Gör om pfish rörelsefunktion till en metod i update
- [x] Lägg till animering till "purple_fish"
- [x] Flytta klasser till separat fil

### v0.2
- [x] Gör om Pfish kod i main till en klass
- [x] Få fisken att röra sig inom skärmen
- [x] Fixa fiskens orientering (vänd mot rörelsens x-riktning)
- [x] Få fisken att röra sig någorlunda trovärdigt
- [x] Lägg till flera (likadana) fiskar
- [x] En knapp som gör något
  - [x] Någon form av klickbar knapp
  - [x] Trigga funktion vid klick (New Game? Exit?)
  - [x] Göra en klass för knappar

### v0.1

- [x] Påbörja readme
- [x] Skapa .gitignore för pythonprojekt
- [x] Importera mall från arcade library
- [x] Ändra färg påbakgrund
- [x] Visa en fisk
- [x] Funktion för att avsluta (tex tryck på `esc` eller liknande)

### pre v0.1

- [x] Få det att fungera på Johns jobb
- [x] Pilla med det här istället för att rätta prov
- [x] Kolla på tutorial(s) för arcade

## Tutorials / Dokumentation

Länkar till material om Python, Arcade Library mm.

### Video

- [Easy 2D Game Creation With Arcade](https://www.youtube.com/watch?v=8InKwiysVIk)

### Text

- [How to create a 2D game with Python and the Arcade library](https://opensource.com/article/18/4/easy-2d-game-creation-python-and-arcade)
- [Learn Python With Arcade Academy](https://arcade-book.readthedocs.io/en/latest/)
- [API quick index](http://arcade.academy/quick_index.html)
- [Arcade API](http://arcade.academy/arcade.html)
- [Pycharm: Getting Started](https://confluence.jetbrains.com/display/PYH/Getting+Started+with+PyCharm)
- [Pycharm: Tutorials](https://confluence.jetbrains.com/display/PYH/PyCharm+Tutorials)

## Names

Generated using [mockaroo](https://mockaroo.com/) and stolen from [anishsingh20 and GRRM](https://github.com/anishsingh20/Network-Analysis-of-Game-of-Thrones).
