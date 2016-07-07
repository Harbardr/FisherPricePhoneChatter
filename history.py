#! /usr/lib/python

from tts import *
import time

class history(object):

    def __init__(self):

        self.history = {"Title":"Une coccinelle assoiffée","Text":"C’est un bel après-midi de printemps. L’air est frais, rempli par le bourdonnement des insectes et le chant des oiseaux. Sous le ciel bleu, une verte prairie inondée de lumière danse, cajolée par les caresses du vent. Une coccinelle se pose sur un brin d’herbe qui ploie aussitôt sous son poids. L’animal a soif. La goute d’eau qui brille au bout de la tige verte capte son attention. La bête à bon Dieu s’en approche pour se désaltérer. Le brin d’herbe sur lequel elle marche tremble, se plie davantage à chaque pas. Craignant de tomber, elle ralentit l’allure. Aussi prudente soit elle, plus elle approche de la goutte d’eau, plus le plancher de verdure penche vers le sol. Alors qu’elle la touche presque, la goutte d’eau finit par se détacher et tomber. Libéré de cette masse, le brin d’herbe se redresse brusquement et catapulte la coccinelle. Tout se passe si vite, et sa déception est si grande, que la bestiole n’a pas le temps d’ouvrir ses ailes. Sa chute l’entraîne dans une flaque d’eau. L’insecte se débat un moment en éclaboussant autour de lui puis, fatigué, s’arrête afin de reprendre son souffle. Un brin d’herbe, courbé juste au dessus de l’eau, capte alors son attention. Elle décide de s’en approcher pour l’attraper et échapper ainsi à la noyade."}
    
    def new(self, history):
        self.history = history

    def read(self,lang):
        say(self.history["Title"],lang)
        text = self.history["Text"].split(".")
        foreach sentence in text:
            say(sentence,lang)
            time.sleep(0.25)
    def text(self):
        return self.history["Title"], self.history["Text"]