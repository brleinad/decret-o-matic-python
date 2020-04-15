WIDTH = 1280
HEIGHT = 720
MASK_POS_X = 0.35 #relative to WIDTH
MASK_POS_Y = 0.4 #relative to HEIGHT
LAST_DAY = 14
MAX_SICK_PPL = 500000
MAX_ACTIONS = 3
DECREES_TEXT_POSITION = WIDTH*0.58, HEIGHT*0.05
DECREES_TEXT_SPACING = 1.5

color = {
    'GREEN' : (0, 255, 0),
    'GREY'  : (150, 150, 150),
    'RED'   : (255, 0, 0),
    'NEON'      : (0, 180, 220),
}

TUTORIAL = """
Un contagiosissimo virus ha infettato il tuo paese.
Per fortuna puoi aiutare Peppe a sconfiggerlo con raziocinio e scienza.
O almeno cercare di tenerlo a bada a tentativi. \
\
\
Clicca sulle caselline per mettere in moto gli ingranaggi della politica.
Emetti il decreto cliccando su Decret-o-matic, assumendotene la piena responsabilità.
Il risultato sarà quello sperato? Lo potrai scoprire solo osservando i contagi del giorno successivo.
Se l'effetto sortito non fosse quello sperato puoi sempre revocare i decreti emessi cliccando su ciò che vuoi cancellare e successivamente sul bidoncino.
Ogni giorno puoi compiere tre azioni: emettere un decreto ti costerà un'azione, revocarlo due azioni.
Non sei obbligato ad esaurire le tue azioni: cliccando su "Giorno" arriverà il domani. \
\
\
Riuscirai a resistere 14 giorni senza superare i 500mila contagi?
"""
