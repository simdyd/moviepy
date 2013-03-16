moviepy
=======

movie Catalog made in Django
ipotizzo cartella base di installazione /opt/website/
scaricando da git viene create la cartella 'moviepy'
rimangono sotto moviepy le cartelle:
logs			: log di attivita varie
media_movie 	: cartella dove stanno le immagini scaricate da internet

Creazione cartella tmp sotto moviepy/pymovie/ una cartella di transito per le letture dai vari siti 

una volta fatto questo si passa al file di settings, duplicate il file settings_sample e chiamatelo settings, se non installato nella cartella indicata ci sono le path da cambiare, 
vanno anche modificati le connesioni al db.


Nel caso in cui si voglia abilitare il download da wikipedia, nel file di settings mettere USE_WIKIPEDIA=True e nel file apache/django.wsgi 
bisogna indicare la path del pacchetto pywikipedia.


direi che è tutto...