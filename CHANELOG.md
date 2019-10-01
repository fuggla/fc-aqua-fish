
### 1.1

- Added font credits
- Added splash screen source files
- Moved csv files to assets

### v1.0
- [x] Någon form av exekverbar fil eller bibliotek för allmänheten
  - [x] Testa exe-fil
- [x] Skippbar splashscreen med logga
  - [x] Något ljud så att första ljudlagget undviks

### v0.9
- [x] Ljudeffekter
  - [x] Äggkläckning
  - [x] Fisk äts upp
  - [x] Puss
  - [x] Fiskar och morötter faller ner i akvariet
  - [x] Plocka upp fisk
  - [x] Bakgrundsljud
  - [x] Ställ in volym
- [x] Metspö som kan fiska upp fiskarna
  - [x] Skapa en krok med popcorn med slumpat djup
  - [x] Skapa fiskelina
  - [x] Köp det i "store"
  - [x] När vi dör blir våra kroppar till popcorn
  - [x] Fiskarna äter popcornet
  - [x] Hajarna jagar popcornet
  - [x] Kroken dras upp ifall fiskarna inte fastnar
  - [x] Fiskarna kan fastna och dras då upp
  - [x] Event för fisket
- [x] Förbättra prestanda
  - [x] Ladda in texturer en gång istället för varje gång en fisk skapas
  - [x] Lägre updateringsfrekvens för fiskinfo (F1)
  - [x] Lägre updateringsfrekvens för informationsdispay
- [x] En rad som säger "Press space"
- [x] Funktion för att visa statistik
  - [x] När användaren håller i fisken?
  - [x] Specifik statistik per fisk
- [x] Exit när credits är slut
  - [x] Användaren kan inte stänga av credits! (nästan)
  - [x] Endast "Q" fungerar för att stoppa
  - [x] En text "Press Q to Exit" kommer efter 90 sekunder

### v0.8
- [x] Barnfiskar kläcks ur äggen. Växer upp efter ett tag
- [x] System för kärlek mellan fiskarna
  - [x] Herrarna och damerna måste pussas innan damerna kan lägga ägg
  - [x] De blir puss-redo när de är mätta
  - [x] Någon form av pussanimation
  - [x] Slumpad chans för graviditet när de pussas (herr + dam)
  - [x] Fiskarna simmar ner och lägger endast ägg på marken
- [x] Snyggare muspekare?
- [x] Flytta runt fiskar med muspekarten
  - [x] Kaska fiskarna
- [x] Spara statistik
  - [x] Haj kills
  - [x] Fisk livstid
  - [x] Antal ätna morötter
  - [x] Antal ätna blåbär
  - [x] Antal lagda ägg
  - [x] Antal pussar
- [x] Fixa sprites för pfish som är andra färger
- [x] Se till att alla bilder kan användas och har länkar till källan
- [x] Startmeny (något separat från paus som bara visas när spelet startas)
- [x] Credits
  - [x] Lång lista på vilka som gjort vad

### v0.7
- [x] System för köttätande fisk
  - [x] En ny typ av fisk som äter andra fiskar
  - [x] Bytesfiskarna blir rädda och flyt när de är nära den
  - [x] Bytesfiskarna blir uppätna av hungriga köttätande fiskar
- [x] Ett system för att styra vilka föremål som visuellt är framför/bakom varandra
- [x] Föremål i akvariet
  - [x] Slumpat valda och utplacerade
  - [x] Fruktväxt som det växer mat på
  - [x] Flera bär på varje planta
- [x] System för äggläggning
  - [x] Fiskarna lägger ägg ifall de ätit mycket
  - [x] Tydliga ägg för blå och lila fiskarna (olika storlek)
  - [x] Endast damerna lägger ägg
  - [x] En ny fisk kläcks efter ett tag
- [x] Mer info om fisken man köper
- [x] Någon form av stack för meddelanden ("X dog av svält" etc)
- [x] Tona in spel vid start

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
