#! /usr/lib/python
# -*- coding: latin-1 -*-

class i8n(object):

    def __init__(self):
        self.sentence  = {  
                            "INIT_EN":"Initialization",
                            "INIT_FR":"Initialisation",
                            "CHATTER_PHONE_FR":"=== CHATTER PHONE ===",
                            "CHATTER_PHONE_EN":"=== CHATTER PHONE ===",
                            "INPUT_FR":"En attente d'une entrée",
                            "INPUT_EN":"Waiting your input",
                            "DATE_FR":"Aujourd'hui nous sommes le {}!",
                            "DATE_EN":"Today it's the {}!",
                            "HELLO_FR":"Salut {}!",
                            "HELLOWORLD_FR":"Bonjour tout le monde!",
                            "STORYTITLE_FR":"Read history : {}",
                            "STORYTEXT_FR":"Text : {}",
                            "MSG_FR":"ENZO! Tu as: {} messages non lus.",
                            "NOLABEL_FR":'No labels found.',
                            "ALWAYSHERE_FR":'Encore là!',
                            "BACKTOTHEFUTUR_FR":"Je suis la voiture de retour vers le futur!",
                            "VALIDATION_FR":"Je suis la voiture de retour vers le futur!",
                            "TERMINATOR_FR":"Au revoir, bébé",
                            "TERMINATOR_EN":"Hasta la vista, baby",
                            "GMAIL_LABELS_FR":"Labels",
                            "GMAIL_LABELS_EN":"Labels",
                            "MENU_EN":"Press 1 for emails, 2 for a story and 3 to quit.",
                            "MENU1_EN":"[1] Read emails",
                            "MENU5_EN":"[2] Tell me a story for children\n",
                            "MENU2_EN":"[3] Print hello world!",
                            "MENU3_EN":"[4] Back To The Futur Car",
                            "MENU4_EN":"[5] Wink eyes",
                            "MENU6_EN":"[6] i2c Blink test\n",
                            "MENUV_EN":"[V] Validation test\n",
                            "MENUQ_EN":"\n[q] Quit\n",
                            "MENU_FR":"Appui sur 1 pour lire les emails, 2 pour une histoire et 3 pour quitter.",
                            "MENU1_FR":"[1] Lire les emails",
                            "MENU5_FR":"[2] Raconte moi une histoire",
                            "MENU2_FR":"[3] Bonjour tout le monde!",
                            "MENU3_FR":"[4] La voiture de Retour Vers Le Futur",
                            "MENU4_FR":"[5] Bouge les yeux",
                            "MENU6_FR":"[6] i2c clignote test",
                            "MENUV_FR":"[V] Validation test",
                            "MENUQ_FR":"[q] Quitter",
                            "BUS_WRITE_FR":"Ecriture sur le bus {}",
                            "BUS_WRITE_EN":"Writing on bus {}",
                            "BREAK_FR":"Break",
                            "BREAK_EN":"Break",
                            "BYPASS_FR":"ByPass",
                            "BYPASS_EN":"ByPass",
                            "GMAIL_MENUN_FR":"Suivant",
                            "GMAIL_MENUN_EN":"Next",
                            "GMAIL_MENUS_FR":"Supprimer",
                            "GMAIL_MENUS_EN":"Suppress"
                            }
    
    def dico(self, lang='FR'):
        dicoLang = {}
        for key, value in self.sentence.items():
            #print key
            if key[-3:]=="_{}".format(lang):
                dicoLang[key[:-3]]=value

        return dicoLang
    
    def menu(self, lang='FR'):
        import operator
        dicoMenu = {}
        for key, value in self.sentence.items():
            #print key
            if key[-3:]=="_{}".format(lang) and key[0:4]=="MENU":
                dicoMenu[key[:-3]]=value
        dicoMenu = sorted(dicoMenu.items(), key=operator.itemgetter(0))

        return dicoMenu
