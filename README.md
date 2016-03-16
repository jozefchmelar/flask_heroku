cesty:

vrati status ci nam sedi meno heslo s udajmi v db
/login/<mail>|<password>

GET : vykresli stranku na pridanie POST :  z formularov si vyberie data a prida uzivatela do db
/person

GET : vrati vsetky person/company/project v json 
/person/all 
/company/all
/project/all

vrati uzivatela podla mailu <pMail>
/person/<pMail>/

vrati projekty uzivatela
/person/<pMail>/projects'

GET: vykrei stranku na pridanie uzivatela ku projektu POST: prida ludi ku projektu
/AddPeople/

GET vykresli stranku na pridanie projektu POST : vytvori novy projekt.
project/

GET : podla cisla projektu vrati prisluchajucih uzivatelov
/project/<number>/users

GET: vrati udaje o firme podla jej mena.
/company/<pName>'

