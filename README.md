# ARES open data

**tl;dr: Veřejný rejstřík je nově publikován jako jeden balík, není nutné stahovat ho po kusech z API. Je to ale stále XML, tak jsem to překonvertoval do CSV.**

## Úvod

Součástí Administrativního registru ekonomických subjektů ([ARES](http://wwwinfo.mfcr.cz/ares/)) je nově i sekce [otevřených dat](http://wwwinfo.mfcr.cz/ares/ares_opendata.html.cz). Prvotní náhled dat jsem komentoval [na twitteru](https://twitter.com/kondrej/status/946843563765182464), tady je kód, kterým jsem vyextrahoval většinu informací ze zdrojových XML souborů do použitelnějšího CSV.

Všechen kód je v jednom Pythoním souboru, potřebujete základní instalaci Pythonu 3 a balík `lxml`. V kódu je třeba jen upravit složku se vstupy a výstupy hned nahoře (použijte `.`, pokud máte kód a data pohromadě), zbytek by měl běžet jak je.

Skript vytvoří tři soubory:

- `udaje.csv` se základními údaji o podnicích,
- `fosoby.csv` s fyzickými osobami (společníci, jednatelé, prokuristi atd.),
- `posoby.csv` s právnickými osobami.

Berte na paměť, že ačkoliv pojící sloupec mezi soubory je IČO, není to v `udaje.csv` sloupec s unikátními hodnotami, protože podniky mohou mít odštěpné závody, kterým jsem přiřadil stejné IČO (trochu to pak dělá bordel při kombinaci dat, to musím ještě vyřešit).

Data konvertovaná berte jak jsou, neručím bohužel za nic, budu ale rád za reporty jakýchkoliv chyb. 

### Data

Zatím jsem do dat příliš nezabrušoval, to teprve přijde. Alespoň pár základních věcí k *první verzi dat* (prosinec 2017):

#### Zdroje dat

	Obchodní rejstřík                           764708
	Spolkový rejstřík                           136783
	Rejstřík společenství vlastníků jednotek     72964
	Rejstřík obecně prospěšných společností       3178
	Nadační rejstřík                              2708
	Rejstřík ústavů                                888

#### Počet subjektů

98214 právnických osob, z toho 762575 stále existujících.

#### Angažované osoby

4,7 milionu fyzických a 200 tisíc právnických osob (resp. vztahů, nejde o unikátní osoby).

## Kukátko
Trochu jsem to zautomatizoval, takže stačí pustit `proc/load.sh`, což zpracuje data do CSV a zároveň nahází data do SQLite databáze (binárka `sqlite3` potřeba). Pak tam je ještě `serve.py`, což vám na `http://localhost:8089` zobrazí prohlížeč ([video tutaj](https://twitter.com/kondrej/status/949744547185250304)).

Netřeba nic kromě SQLite a Pythonu 3, žádné externí knihovny to nepotřebuje, webappka je jeden HTML soubor bez jakýchkoli závislostí. Přešroubovat na Postgre to půjde snadno, krom `collate nocase` a `.import` v `load.sh` nepoužívám nic specifického pro SQLite.

## Třeba dodělat

Je to zatím první nástřel, pár věcí chybí,

- vazby fyzických a právnických osob na odštěpné závody nejsou jednoznačné
 - vyčlenit je ze seznamu firem pryč - kam pak ale s jejich PO a FO?
 - budem pak udělat PK nad IČO
- přepsat info o formátech z twitteru sem
- spousta firem (zejm. ministerstva) není v OR, ale můžou být vlastníky - takže ty by mělo jít dohledat
- pole vznikFunkce, vznikClenstvi, ZpusobJednani, činnosti
- cross check proti [specce](http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer_vreo/v_1.0.0/ares_answer_vreo.xsd), co vůbec dává smysl přidávat (např. specka má elementy `PravniForma` nebo `StatusVerejneProspesnosti`, ale v datech nejsou, stejně tak data narození, rodná čísla atd.)
- zastoupení právnických osob (zanořený element `Zastoupeni`)

## Kontakt

Stížnosti a tak směřujte na [email](mailto:ondrej.kokes@gmail.com) nebo [twitter](https://twitter.com/kondrej). A nebo rovnou posílejte pull requesty.