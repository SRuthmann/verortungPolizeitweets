# verortungPolizeitweets
Bei dem hier beschriebenen Programm handelt es sich um eine Anwendung, die Tweets räumlich verortet und auf einer Karte darstellt. Dafür wird der Text auf Eigennamen untersucht, die anschließend mithilfe eines Geocoders abgefragt werden. Wenn es sich um einen Ort handelt, werden die Koordinaten gespeichert und anschließend auf einer Karte sichtbar.

In der folgenden Dokumentation werden zunächst die Programmstruktur und die Ein-bindung externer Dienste, Programme und Bibliotheken erläutert. Anschließend wird die Installation der Anwendung beschrieben. Nach den Erklärungen zum Starten des Pro-gramms werden die Funktionen im Quellcode ausgeführt. 

## Installation
Da für die Anwendung die Programmiersprache Python verwendet wurde, muss diese auf dem Computer installiert sein. Auf der folgenden Internetseite kann die Version Python 3.7.3 heruntergeladen werden:<br/>
`https://www.python.org/downloads/`<br/>
Um zu überprüfen, ob Python bereits installiert ist, kann in der Eingabeaufforderung der folgende Befehl gestellt werden. Damit wird die Version angezeigt, die auf dem Compu-ter eingerichtet ist.<br/>
`python -V`<br/>
Um die verwendeten Bibliotheken herunterzuladen, wird empfohlen einen Package-Manager zu installieren. Der für Python am häufigsten verwendete ist Pip. Zur Installati-on wird das folgende Dokument heruntergeladen: <br/>
https://bootstrap.pypa.io/get-pip.py<br/>
Anschließend kann in der Eingabeaufforderung der Befehl <br/>
`python get-pip.py`<br/>
ausgeführt werden. Um zu erkennen, welche Version heruntergeladen wurde, kann eben-falls mit dem Befehl <br/>
`pip -V`<br/>
die Version zurückgegeben werden. Sobald Pip erfolgreich installiert ist, können die Bib-liotheken heruntergeladen werden.
Tweepy ist eine Bibliothek, die den Zugriff auf die Twitter-API mit Python schnell und einfach ermöglicht. Zum Herunterladen wird der Befehl <br/>
`pip install tweepy`<br/>
in der Eingabeaufforderung ausgeführt. <br/>
Um die Tweets zu analysieren, müssen sie zuerst bearbeitet werden. Dafür werden Emoticons und URLs entfernt. Um das auf einem einfachen Weg durchführen zu können, wird der Tweet-Preprocessor verwendet. Dieser wird mithilfe des Befehls <br/>
`pip install tweet-preprocessor`<br/>
installiert. <br/>

Zur Ermittlung der Eigennamen wird das Programm spaCy verwendet. Es ist in Python geschrieben und zur Verarbeitung natürlicher Sprache entwickelt. Zur Installation für die Verwendung in deutscher Sprache müssen folgende Befehle ausgeführt werden.<br/>
`pip install -U spacy<br/>
python -m spacy download de<br/>
python -m spacy download de_core_news_sm`<br/>
Für den Zugriff auf die Datenbank PostgreSQL wird die am meisten verbreitete Biblio-thek in Kombination mit Python psycopg2 verwendet. Mit <br/>
`pip install psycopg2`<br/>
kann sie installiert werden.<br/>
Für den Zugriff auf HERE wird ebenfalls eine Bibliothek verwendet. Sie heißt herepy und stellt eine Verbindung zur REST-API von HERE her. Herepy wird mit dem Befehl <br/>
`pip install herepy`<br/>
installiert.

Um die Datenbank auf dem Computer verwenden zu können, wird Docker eingesetzt. Dadurch können Anwendungen in sogenannten Containern laufen. Um Docker verwen-den zu können, muss zuerst ein Account angelegt und anschließend Docker Desktop heruntergeladen werden. Das kann auf folgender Internetseite durchgeführt werden.<br/>
https://www.docker.com/get-started<br/>
Docker Desktop ist ausreichend, um Docker zu verwalten. Um eine bessere Übersicht und Verwaltung der Anwendungen zu bekommen, kann Portainer verwendet werden. Das Programm wird selbst in einen Container in Docker geladen. Nähere Informationen gibt es auf der Internetseite <br/>
https://www.portainer.io/<br/>
Zum Installieren müssen folgende Befehle in der Eingabeaufforderung ausgeführt wer-den: <br/>
`docker volume create portainer_data<br/>
docker run -d -p 8000:8000 -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portain-er/portainer`<br/>
Um die Datenbank PostgreSQL laufen lassen zu können, muss ebenfalls erst ein Image angelegt werden, welches dann in einem Container gestartet werden kann. Dafür müssen die Sternchen (***) mit dem jeweiligen Inhalt ersetzt werden.<br/>
`docker volume create postgres_data<br/>
docker run -d -e POSTGRES_PASSWORD=*** --name PostgresDB -p 5432:5432 --restart=always -v postgres_data:/var/lib/postgresql/data postgres`<br/>
Um mit der Datenbank arbeiten zu können, wird zuletzt noch pgAdmin in einem Do-cker-Container installiert.<br/>
`docker run -p 90:80 -e "PGADMIN_DEFAULT_EMAIL=***" -e "PGAD-MIN_DEFAULT_PASSWORD=***" -d dpage/pgadmin4`<br/>
Zuletzt muss die Datei InsertDatabase.sql in die Datenbank eingelesen und die Datei au-thentification.py mit den Zugangsberechtigungen für Twitter, HERE und die Datenbank ergänzt werden.   

## Quick Start
Mit den bisherigen Installationen funktioniert der Python-Code. Um das Programm star-ten zu können, braucht es aufgrund der Programmiersprache PHP noch eine Serverum-gebung. Dorthin müssen die einzelnen Dateien geladen werden. Anschließend wird die HTML-Datei startseite.html in einem Browser gestartet. Sobald der Benutzer die Einga-ben zum Account und der Anzahl der maximal verwendeten Tweets durchgeführt hat, kann mit Klicken auf den Button „Zur Karte“ das Programm gestartet werden. Nachdem die Skripte durchgeführt wurden, erscheint eine neue Seite, die eine Karte anzeigt. Je nach Anzahl der gefundenen Orte werden diese durch Marker auf der Karte visualisiert und unterhalb der Karte in einer Tabelle aufgeführt.

## Beschreibung der Funktionen
### GetTweets.py
Für die Pythondatei GetTweets.py werden im Folgenden die Funktionen näher ausge-führt. Der Ablauf der gesamten Datei ist in Kapitel 4.4 näher erläutert und durch ein Ablaufdiagramm dargestellt. Darin ist der Aufruf der einzelnen Funktionen zu sehen. <br/>
Klasse: TwitterAuthenticator()<br/>
__Funktion: authenticate_twitter_app()__<br/>
Führt die Authentifizierung für die Twitter-API durch.<br/>
Parameter: /<br/>
Rückgabe: auth ist das Ergebnis der Authentifizierung zur Verwendung der Twitter-API.<br/>

Klasse: TwitterClient()<br/>
__Funktion: init()__<br/>
Führt die Funktion authenticate_twitter aus und stellt die Verbindung zu Twitter her.<br/>
Parameter: / <br/>
Rückgabe: / <br/>

__Funktion: get_user_timeline_tweets(user, num_tweets)__<br/>
Speichert eine definierte Anzahl an Tweets eines bestimmten Accounts<br/>
Parameter: user Account, von dem die Tweets geladen werden sollen.<br/>
num_tweets Anzahl an Tweets, die geladen werden sollen.<br/>
Rückgabe: tweets gibt eine Liste mit Tweets zurück.<br/>

Klasse: TweetPreprocessor()<br/>
__Funktion: preprocessor(tweet)__<br/>
Verarbeitet den Text eines Tweets vor, sodass er analysiert werden kann. Dabei werden Umlaute ersetzt und Symbole entfernt.<br/>
Parameter: tweet ist der Text, der vorverarbeitet werden soll.<br/>
Rückgabe: tweet ist der bearbeitete Text.<br/>

Klasse: TweetAnalyzer()<br/>
__Funktion: tweetsArray(tweets)__<br/>
Speichert die Informationen der Tweets, die für den weiteren Verlauf des Programms benötigt werden, in einer Liste ab. Dazu gehören der Text, das Erscheinungsdatum, der Autor und die Koordinaten. Der Text wird mit der Funktion preprocessor(tweet) bearbeitet. <br/>
Parameter: tweets ist die Liste mit Tweets.<br/>
Rückgabe: tweetsarray ist die Liste mit Tweets, die ausschließlich die benötigten Informa-tionen enthalten.<br/>

Klasse: TextWriter()<br/>
__Funktion: JSONFile(tweetsarray)__<br/>
Bringt die Informationen aus der Liste in ein JSON-Format und schreibt sie in die Datei tweets.txt.<br/>
Parameter: tweetsarray ist die Liste mit Tweets, mit den benötigten Informationen.<br/>
Rückgabe: „True“ gibt an, dass das Abspeichern der Tweets in der Datei funktioniert hat.<br/>

### DetectPositionGerman.py<br/>
Die Datei DetectPositionGerman.py enthält nur eine Funktion, die hier beschrieben wird. Der weitere Ablauf ist in Kapitel 4.5.2 detailliert erläutert. 

Klasse: Housenumber()<br/>
__Funktion: add_housenumber(location, text)__<br/>
Sucht den Text nach einer Zahl hinter dem Attribut location ab. Wenn dort eine Zahl existiert, wird diese zu dem Attribut location hinzugefügt.<br/>
Parameter: location ist der Eigenname, den spaCy ermittelt hat.<br/>
			 text ist der Text eines Tweets, in dem der Eigenname ermittelt wurde. <br/>
Rückgabe: location gibt die Ortsangabe mit Hausnummer zurück.<br/>

### DetectCoordinates.py
Im Folgenden werden die Funktionen der Datei DetectCoordinates.py ausgeführt. Der Ablauf des Quellcodes ist in Kapitel 4.6.4 beschrieben. Dort sind auch die Funktionswei-sen der komplexen Funktionen im Detail aufgeführt. 

Klasse: CityPreprocessor()<br/>
__Funktion: preprocessor(city)__<br/>
Ersetzt die Umlaute, damit der Geocoder den Stadtnamen erkennen kann.<br/>
Parameter: city ist der Name einer Location. <br/>
Rückgabe: city ist der bearbeitete Name der Location.<br/>

Klasse: DatabaseAuthenification()<br/>
__Funktion: dbConnection()__<br/>
Stellt die Verbindung zur Datenbank her.<br/>
Parameter: /<br/>
Rückgabe: connection gibt die Informationen zur erfolgreichen Verbindung mit der Da-tenbank zurück.<br/>

Klasse: DatabaseQuery()<br/>
__Funktion: queryDatabase(namedEntity)__<br/>
Überprüft, ob der Eigenname eine Abkürzung eines Ortsnamens von einem KFZ-Kennzeichen abgeleitet ist. In diesem Fall wird die Abkürzung durch den ausgeschriebe-nen Namen ersetzt.<br/>
Parameter: namedEntity ist der Eigenname, der überprüft werden soll.<br/>
Rückgabe: /<br/>

Klasse: LocationToJSON()<br/>
__Funktion: locToJSON(response, index)__<br/>
Entnimmt die relevanten Informationen aus der Rückgabe von HERE und wandelt sie mit Weiteren in ein JSON-Format um.<br/>
Parameter: response ist die Rückgabe von HERE. <br/>
index ist die Nummer des Objekts in der Liste lines.<br/>
Rückgabe: /<br/>

Klasse: Locationcombination() <br/>
__Funktion: combine_locations(locations, namedEntity, numLine)__<br/>
Kombiniert zwei Eigennamen und fragt sie mit dem Dienst von HERE ab. Das Ergebnis wird an die Funktion locToJson übergeben. Ist die Kombination eine Ortsangabe, werden die verwendeten Eigennamen vermerkt und das JSON-Objekt in der Datei coordinates.txt gespeichert.<br/>
Parameter: locations ist die Liste mit allen Eigennamen zu einem Tweet.<br/>
			 namedEntity ist der erste Eigenname des nächsten Tweets.<br/>
			 numLine ist die Nummer des Objekts in der Liste lines.<br/>
Rückgabe: namedEntity["text"] ist der Text des nächsten Tweets.<br/>

Klasse: DeleteLocation()<br/>
__Funktion: delete_comloc(combinations)__<br/>
Löscht die in einer Kombination gespeicherten Eigennamen, damit sie einzeln nicht er-neut abgefragt werden.<br/>
Parameter: combinations ist die Liste mit Nummern der Objekte, die als Kombination eine Ortsangabe ergeben haben.<br/>
Rückgabe: combinations ist die geordnete Liste mit Nummern der Objekte, die als Kom-bination eine Ortsangabe ergeben haben.<br/>
