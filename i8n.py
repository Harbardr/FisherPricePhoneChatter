#! /usr/lib/python
# -*- coding: latin-1 -*-

class i8n(object):

    def __init__(self):
        self.sentence  = {  "CHATTER_PHONE_FR":"=== CHATTER PHONE ===",
                            "CHATTER_PHONE_EN":"=== CHATTER PHONE ===",
                            "INPUT_FR":"En attente d'une entrée",
                            "INPUT_EN":"Waiting your input",
                            "HELLO_FR":"Bonjour {}, comment vas tu?",
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
                            "MENU1_EN":"[1] Read {} emails\n",
                            "MENU2_EN":"[2] Print hello world!\n",
                            "MENU3_EN":"[3] Back To The Futur Car\n",
                            "MENU4_EN":"[4] Wink eyes\n",
                            "MENU5_EN":"[5] Tell me a story for children\n",
                            "MENU6_EN":"[6] i2c Blink test\n",
                            "MENUV_EN":"[V] Validation test\n",
                            "MENUQ_EN":"\n[q] Quit\n",
                            "MENU1_FR":"[1] Lire les emails de {}\n",
                            "MENU2_FR":"[2] Bonjour tout le monde!\n",
                            "MENU3_FR":"[3] La voiture de Retour Vers Le Futur\n",
                            "MENU4_FR":"[4] Bouge les yeux\n",
                            "MENU5_FR":"[5] Raconte moi une histoire\n",
                            "MENU6_FR":"[6] i2c clignote test\n",
                            "MENUV_FR":"[V] Validation test\n",
                            "MENUQ_FR":"\n[q] Quitter\n",
                            "BUS_WRITE_FR":"Ecriture sur le bus {}",
                            "BUS_WRITE_EN":"Writing on bus {}",
                            "BREAK_FR":"Break",
                            "BREAK_EN":"Break",
                            "BYPASS_FR":"ByPass",
                            "BYPASS_EN":"ByPass"
                            }
    
    def dico(self, lang='FR'):
        dicoLang = {}
        for key, value in self.sentence.items():
            print key
            if key[-3:]=="_{}".format(lang):
                dicoLang[key[-3]]=value

        return dicoLang
