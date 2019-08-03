#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module vid�o
## Copyright 2008-2010  St�phan GU�RIN
## contact : setthe@gmail.com
##
## Ce logiciel est un programme informatique destin� aux �lectriciens et 
## permettant de calculer rapidement la section d'un c�ble, de r�aliser des
## conversions d'unit�s �lectriques, etc.... 
##
## Ce logiciel est r�gi par la licence CeCILL soumise au droit fran�ais et
## respectant les principes de diffusion des logiciels libres. Vous pouvez
## utiliser, modifier et/ou redistribuer ce programme sous les conditions
## de la licence CeCILL telle que diffus�e par le CEA, le CNRS et l'INRIA 
## sur le site "http://www.cecill.info".
##
## En contrepartie de l'accessibilit� au code source et des droits de copie,
## de modification et de redistribution accord�s par cette licence, il n'est
## offert aux utilisateurs qu'une garantie limit�e.  Pour les m�mes raisons,
## seule une responsabilit� restreinte p�se sur l'auteur du programme,  le
## titulaire des droits patrimoniaux et les conc�dants successifs.
##
## A cet �gard  l'attention de l'utilisateur est attir�e sur les risques
## associ�s au chargement,  � l'utilisation,  � la modification et/ou au
## d�veloppement et � la reproduction du logiciel par l'utilisateur �tant 
## donn� sa sp�cificit� de logiciel libre, qui peut le rendre complexe � 
## manipuler et qui le r�serve donc � des d�veloppeurs et des professionnels
## avertis poss�dant  des  connaissances  informatiques approfondies.  Les
## utilisateurs sont donc invit�s � charger  et  tester  l'ad�quation  du
## logiciel � leurs besoins dans des conditions permettant d'assurer la
## s�curit� de leurs syst�mes et ou de leurs donn�es et, plus g�n�ralement, 
## � l'utiliser et l'exploiter dans les m�mes conditions de s�curit�. 
##
## Le fait que vous puissiez acc�der � cet en-t�te signifie que vous avez 
## pris connaissance de la licence CeCILL, et que vous en avez accept� les
## termes.
##
##----------------------------------------------------------------------------------------------

import wx
from math import pi, atan


############################################################################
##                                                                        ##
##                            Module vid�o                                ##
##                                                                        ##
##                                                                        ##
############################################################################

version = "0.1.3"


# variables globales

statusText = u"Calcul d'un champ de vision en fonction d'une distance"
listeFocale = ['2.6','2.8','3','3.5','3.6','3.7','4','4.2','4.5','4.8','5','5.5','5.7','5.8','6','6.2','6.3',
               '6.5','7.5','8','8.5','9','9.5','10','12','12.5','15','16','25','38','40','48','50','58','60','75',
               '87','90','100','120','128','140','144','180','240']
listeCapteur = [' 1/4"',' 1/3"',' 1/2"',' 2/3"']




class OngletChamp(wx.Panel):
    """Calcul d'un champ de vision en fonction d'une distance"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## cr�ation des widgets #####################
        
        # spinctrl de choix de la distance
        labelDist = wx.StaticText(self, -1, u"Distance sujet/objectif (en m): ")
        self.distance = wx.SpinCtrl(self, -1, "")
        self.distance.SetRange(1,999)
        self.distance.SetValue(20)
        
        # Choix de s�lection du capteur
        labelCapteur = wx.StaticText(self, -1, u"Format du capteur : ")
        self.lbCapteur = wx.Choice(self, -1, (-1, -1), choices = listeCapteur)
        self.lbCapteur.SetStringSelection(listeCapteur[1])
        
        # ListBox de s�lection de la focale
        labelFocale = wx.StaticText(self, -1, u"Focale (mm): ")
        self.lbFocale = wx.ListBox(self, -1, (10, 10), (90, 120), listeFocale, wx.LB_SINGLE)
        self.lbFocale.SetStringSelection(listeFocale[11])
        
        # R�sultats
        labelLargeur = wx.StaticText(self, -1, u"Largeur x Hauteur visualis� : ")
        self.largeur = wx.StaticText(self, -1, u"... m x ... m")
        self.largeur.SetForegroundColour('blue')
        self.largeur.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelAngle = wx.StaticText(self, -1, u"Angle de vision : ")
        self.angle = wx.StaticText(self, -1, u"....... �")
        self.angle.SetForegroundColour('blue')
        self.angle.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # Bouton calcul
        self.btnCalc = wx.Button(self ,-1, "Calculer")
        self.btnCalc.SetBackgroundColour("yellow")
        self.btnCalc.SetDefault()
        if self.parent.licence == 0:
            self.btnCalc.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
        
        ############### Ajout des wigets au sizer ####################
        self.gbs.Add(labelDist, (1,0))
        self.gbs.Add(self.distance, (1,1))
        self.gbs.Add(labelCapteur, (2,0))
        self.gbs.Add(self.lbCapteur, (2,1))
        self.gbs.Add(labelFocale, (3,0))
        self.gbs.Add(self.lbFocale, (3,1), (3,1), wx.EXPAND)
        self.gbs.Add(labelLargeur, (1,3))
        self.gbs.Add(self.largeur, (2,3))
        self.gbs.Add(labelAngle, (3,3))
        self.gbs.Add(self.angle, (4,3))
        self.gbs.Add(self.btnCalc, (6,0))
        
        self.SetSizerAndFit(self.gbs)
        
    def onCalcul(self, evt):
        """Calcul d'une largeur & focale en fonction de la hauteur � visualiser"""
        # on r�cup�re les valeurs n�cessaires au calcul
        d = self.distance.GetValue()
        capteur = self.lbCapteur.GetStringSelection()
        focale = self.lbFocale.GetStringSelection()
        # on converti la valeur de la focale (str) en entier (int)
        focale = float(focale)
        # on donne les valeurs � la largeur cible (lc) et la hauteur cible (hc) du capteur
        if capteur == listeCapteur[0]:
            lc = 3.6
            hc = 2.7
        if capteur == listeCapteur[1]:
            lc = 4.8
            hc = 3.6
        if capteur == listeCapteur[2]:
            lc = 6.4
            hc = 4.8
        if capteur == listeCapteur[3]:
            lc = 8.8
            hc = 6.6
        
        # Calcul de la largeur visualis�e
        lvisu = round((lc*(d/focale)), 1)
        hvisu = round((3*lvisu/4), 1)
        avisu = round(((2*atan(lvisu/(2*d)))*(180/pi)), 1)
        
        # envoie des r�sultats dans les statictexts
        self.largeur.SetLabel("%s m x %s m" %(lvisu, hvisu))
        #self.hauteur.SetLabel("%s m" %hvisu)
        self.angle.SetLabel(u"%s �" %avisu)
         
        
class OngletHauteur(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## cr�ation des widgets #####################
        
        # spinctrl de choix de la distance
        labelDistance = wx.StaticText(self, -1, u"Distance sujet/objectif (en m): ")
        self.distance = wx.SpinCtrl(self, -1, "")
        self.distance.SetRange(1,999)
        self.distance.SetValue(20)
        
        # Choix de s�lection du capteur
        labelCapteur = wx.StaticText(self, -1, u"Format du capteur : ")
        self.lbCapteur = wx.Choice(self, -1, (-1, -1), choices = listeCapteur)
        self.lbCapteur.SetStringSelection(listeCapteur[1])
        
        # spinctrl de choix de la hauteur � visualiser
        labelHauteur = wx.StaticText(self, -1, u"Hauteur � visualiser (en m): ")
        self.hauteur = wx.SpinCtrl(self, -1, "")
        self.hauteur.SetRange(1,100)
        self.hauteur.SetValue(3)
        
        # R�sultats
        labelLargeur = wx.StaticText(self, -1, u"Largeur visualis�e : ")
        self.largeur = wx.StaticText(self, -1, u"....... m")
        self.largeur.SetForegroundColour('blue')
        self.largeur.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelAngle = wx.StaticText(self, -1, u"Angle de vision : ")
        self.angle = wx.StaticText(self, -1, u"....... �")
        self.angle.SetForegroundColour('blue')
        self.angle.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelFocale = wx.StaticText(self, -1, u"Focale id�ale : ")
        self.focale = wx.StaticText(self, -1, u"....... mm")
        self.focale.SetForegroundColour('blue')
        self.focale.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # Bouton calcul
        self.btnCalc = wx.Button(self ,-1, "Calculer")
        self.btnCalc.SetBackgroundColour("yellow")
        self.btnCalc.SetDefault()
        if self.parent.licence == 0:
            self.btnCalc.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
        
        ############### Ajout des wigets au sizer ####################
        self.gbs.Add(labelDistance, (1,0))
        self.gbs.Add(self.distance, (1,1))
        self.gbs.Add(labelCapteur, (2,0))
        self.gbs.Add(self.lbCapteur, (2,1))
        self.gbs.Add(labelHauteur, (3,0))
        self.gbs.Add(self.hauteur, (3,1))
        self.gbs.Add(labelLargeur, (1,3))
        self.gbs.Add(self.largeur, (1,4))
        self.gbs.Add(labelAngle, (2,3))
        self.gbs.Add(self.angle, (2,4))
        self.gbs.Add(labelFocale, (3,3))
        self.gbs.Add(self.focale, (3,4))
        self.gbs.Add(self.btnCalc, (4,1))
        
        self.SetSizerAndFit(self.gbs)
        
    def onCalcul(self, evt):
        # on r�cup�re les valeurs n�cessaires au calcul
        d = self.distance.GetValue()
        capteur = self.lbCapteur.GetStringSelection()
        h = self.hauteur.GetValue()
        # on donne les valeurs � la largeur cible (lc) et la hauteur cible (hc) du capteur
        if capteur == listeCapteur[0]:
            lc = 3.6
            hc = 2.7
        if capteur == listeCapteur[1]:
            lc = 4.8
            hc = 3.6
        if capteur == listeCapteur[2]:
            lc = 6.4
            hc = 4.8
        if capteur == listeCapteur[3]:
            lc = 8.8
            hc = 6.6
        
        # Calcul de la largeur visualis�e
        lvisu = round((4*h/3), 1)
        avisu = round(((2*atan(lvisu/(2*d)))*(180/pi)), 1)
        focal = round((d*(hc/h)), 1)
        
        # envoie des r�sultats dans les statictexts
        self.largeur.SetLabel("%s m" %lvisu)
        self.angle.SetLabel(u"%s �" %avisu)
        self.focale.SetLabel("%s mm" %focal)


class OngletLargeur(wx.Panel):
    """Calcul d'une hauteur & focale en fonction de la largeur � visualiser"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## cr�ation des widgets #####################
        
        # spinctrl de choix de la distance
        labelDistance = wx.StaticText(self, -1, u"Distance sujet/objectif (en m): ")
        self.distance = wx.SpinCtrl(self, -1, "")
        self.distance.SetRange(1,999)
        self.distance.SetValue(20)
        
        # Choix de s�lection du capteur
        labelCapteur = wx.StaticText(self, -1, u"Format du capteur : ")
        self.lbCapteur = wx.Choice(self, -1, (-1, -1), choices = listeCapteur)
        self.lbCapteur.SetStringSelection(listeCapteur[1])
        
        # spinctrl de choix de la largeur � visualiser
        labelLargeur = wx.StaticText(self, -1, u"Largeur � visualiser (en m): ")
        self.largeur = wx.SpinCtrl(self, -1, "")
        self.largeur.SetRange(1,100)
        self.largeur.SetValue(5)
        
        # R�sultats
        labelHauteur = wx.StaticText(self, -1, u"Hauteur visualis�e : ")
        self.hauteur = wx.StaticText(self, -1, u"....... m")
        self.hauteur.SetForegroundColour('blue')
        self.hauteur.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelAngle = wx.StaticText(self, -1, u"Angle de vision : ")
        self.angle = wx.StaticText(self, -1, u"....... �")
        self.angle.SetForegroundColour('blue')
        self.angle.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelFocale = wx.StaticText(self, -1, u"Focale id�ale : ")
        self.focale = wx.StaticText(self, -1, u"....... mm")
        self.focale.SetForegroundColour('blue')
        self.focale.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # Bouton calcul
        self.btnCalc = wx.Button(self ,-1, "Calculer")
        self.btnCalc.SetBackgroundColour("yellow")
        self.btnCalc.SetDefault()
        if self.parent.licence == 0:
            self.btnCalc.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
        
        ############### Ajout des wigets au sizer ####################
        self.gbs.Add(labelDistance, (1,0))
        self.gbs.Add(self.distance, (1,1))
        self.gbs.Add(labelCapteur, (2,0))
        self.gbs.Add(self.lbCapteur, (2,1))
        self.gbs.Add(labelLargeur, (3,0))
        self.gbs.Add(self.largeur, (3,1))
        self.gbs.Add(labelHauteur, (1,3))
        self.gbs.Add(self.hauteur, (1,4))
        self.gbs.Add(labelAngle, (2,3))
        self.gbs.Add(self.angle, (2,4))
        self.gbs.Add(labelFocale, (3,3))
        self.gbs.Add(self.focale, (3,4))
        self.gbs.Add(self.btnCalc, (4,1))
        
        self.SetSizerAndFit(self.gbs)
        
    def onCalcul(self, evt):
        # on r�cup�re les valeurs n�cessaires au calcul
        d = self.distance.GetValue()
        capteur = self.lbCapteur.GetStringSelection()
        l = float(self.largeur.GetValue())
        # on donne les valeurs � la largeur cible (lc) et la hauteur cible (hc) du capteur
        if capteur == listeCapteur[0]:
            lc = 3.6
            hc = 2.7
        if capteur == listeCapteur[1]:
            lc = 4.8
            hc = 3.6
        if capteur == listeCapteur[2]:
            lc = 6.4
            hc = 4.8
        if capteur == listeCapteur[3]:
            lc = 8.8
            hc = 6.6
        
        # Calcul de la largeur visualis�e
        hvisu = round((3*l/4), 1)
        avisu = round(((2*atan(l/(2*d)))*(180/pi)), 1)
        focal = round((d*(lc/l)), 1)
        
        # envoie des r�sultats dans les statictexts
        self.hauteur.SetLabel("%s m" %hvisu)
        self.angle.SetLabel(u"%s �" %avisu)
        self.focale.SetLabel("%s mm" %focal)
        
        


class OngletZoom(wx.Panel):
    """Calcul d'un champ mini/maxi en fonction d'un objectif"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## cr�ation des widgets #####################
        
        # spinctrl de choix de la distance
        labelDistance = wx.StaticText(self, -1, u"Distance sujet/objectif (en m): ")
        self.distance = wx.SpinCtrl(self, -1, "")
        self.distance.SetRange(1,999)
        self.distance.SetValue(20)
        
        # Choix de s�lection du capteur
        labelCapteur = wx.StaticText(self, -1, u"Format du capteur : ")
        self.lbCapteur = wx.Choice(self, -1, (-1, -1), choices = listeCapteur)
        self.lbCapteur.SetStringSelection(listeCapteur[1])
        
        # Choix de s�lection de la focale mini
        labelFocaleMini = wx.StaticText(self, -1, u"Focale mini (mm): ")
        self.lbFocaleMini = wx.Choice(self, -1, (-1, -1), choices = listeFocale)
        self.lbFocaleMini.SetStringSelection(listeFocale[0])
        
        # Choix de s�lection de la focale maxi
        labelFocaleMaxi = wx.StaticText(self, -1, u"Focale maxi (mm): ")
        self.lbFocaleMaxi = wx.Choice(self, -1, choices = listeFocale)
        self.lbFocaleMaxi.SetStringSelection(listeFocale[21])
        
        # R�sultats
        labelHauteurMini = wx.StaticText(self, -1, u"Champ mini (l x h): ")
        self.hauteurMini = wx.StaticText(self, -1, u"... m x ... m")
        self.hauteurMini.SetForegroundColour('red')
        self.hauteurMini.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        labelHauteurMaxi = wx.StaticText(self, -1, u"Champ maxi (l x h): ")
        self.hauteurMaxi = wx.StaticText(self, -1, u"... m x ... m")
        self.hauteurMaxi.SetForegroundColour('blue')
        self.hauteurMaxi.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        labelAngleMini = wx.StaticText(self, -1, u"Angle de vision mini : ")
        self.angleMini = wx.StaticText(self, -1, u"... �")
        self.angleMini.SetForegroundColour('red')
        self.angleMini.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        labelAngleMaxi = wx.StaticText(self, -1, u"Angle de vision maxi : ")
        self.angleMaxi = wx.StaticText(self, -1, u"... �")
        self.angleMaxi.SetForegroundColour('blue')
        self.angleMaxi.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # Bouton calcul
        self.btnCalc = wx.Button(self ,-1, "Calculer")
        self.btnCalc.SetBackgroundColour("yellow")
        self.btnCalc.SetDefault()
        if self.parent.licence == 0:
            self.btnCalc.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
        
        ############### Ajout des wigets au sizer ####################
        self.gbs.Add(labelDistance, (1,0))
        self.gbs.Add(self.distance, (1,1))
        self.gbs.Add(labelCapteur, (2,0))
        self.gbs.Add(self.lbCapteur, (2,1))
        self.gbs.Add(labelFocaleMini, (3,0))
        self.gbs.Add(self.lbFocaleMini, (3,1))
        self.gbs.Add(labelFocaleMaxi, (4,0))
        self.gbs.Add(self.lbFocaleMaxi, (4,1))
        
        self.gbs.Add(self.btnCalc, (5,1))
        
        self.gbs.Add(labelHauteurMini, (1,3))
        self.gbs.Add(self.hauteurMini, (2,3))
        self.gbs.Add(labelHauteurMaxi, (3,3))
        self.gbs.Add(self.hauteurMaxi, (4,3))
        self.gbs.Add(labelAngleMini, (5,3))
        self.gbs.Add(self.angleMini, (5,4))
        self.gbs.Add(labelAngleMaxi, (6,3))
        self.gbs.Add(self.angleMaxi, (6,4))
        
        
        self.SetSizerAndFit(self.gbs)
        
    def onCalcul(self, evt):
        # on r�cup�re les valeurs n�cessaires au calcul
        d = self.distance.GetValue()
        capteur = self.lbCapteur.GetStringSelection()
        focMini = float(self.lbFocaleMini.GetStringSelection())
        focMaxi = float(self.lbFocaleMaxi.GetStringSelection())
        # on donne les valeurs � la largeur cible (lc) et la hauteur cible (hc) du capteur
        if capteur == listeCapteur[0]:
            lc = 3.6
            hc = 2.7
        if capteur == listeCapteur[1]:
            lc = 4.8
            hc = 3.6
        if capteur == listeCapteur[2]:
            lc = 6.4
            hc = 4.8
        if capteur == listeCapteur[3]:
            lc = 8.8
            hc = 6.6
        
        # Calcul des largeurs visualis�es
        lMinVisu = round((lc*d/focMaxi), 1)
        lMaxVisu = round((lc*d/focMini), 1)
        # Calcul des hauteurs visualis�es
        hMinVisu = round((3*lMinVisu/4), 1)
        hMaxVisu = round((3*lMaxVisu/4), 1)
        # Calculs des angles
        aMinVisu = round(((2*atan(lMinVisu/(2*d)))*(180/pi)), 1)
        aMaxVisu = round(((2*atan(lMaxVisu/(2*d)))*(180/pi)), 1)
        
        # r�sultats 
        self.hauteurMini.SetLabel("%sm x %sm" %(lMinVisu, hMinVisu))
        self.hauteurMaxi.SetLabel("%sm x %sm" %(lMaxVisu, hMaxVisu))
        self.angleMini.SetLabel(u"%s �" %aMinVisu)
        self.angleMaxi.SetLabel(u"%s �" %aMaxVisu)



class Video(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=u"Vid�o %s"%version, 
                          style=wx.DEFAULT_FRAME_STYLE 
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent = parent
        
        ################### pour windows ###################
        self.licence = self.parent.licence_ok
        ####################################################
        
         # Ajout d'une barre d'�tat
        self.CreateStatusBar()
        self.SetStatusText(statusText)    
        
        # Cr�ation d'un panel pour y placer les Widgets
        panel = wx.Panel(self)
        
        # Cr�ation d'un sizer pour organiser les widgets
        sizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        # Ajout du notebook au panel
        self.nb = wx.Notebook(panel)#, size=(500,500))
        ##### pour windows ###########
        self.nb.licence = self.licence
        ##############################
        
        # Cr�ation des onglets
        self.page1 = OngletChamp(self.nb)
        self.page2 = OngletHauteur(self.nb)
        self.page3 = OngletLargeur(self.nb)
        self.page4 = OngletZoom(self.nb)
        
        # Ajout des onglets au notebook
        self.nb.AddPage(self.page1, "Champ de vision")
        self.nb.AddPage(self.page2, u"Largeur et focale")
        self.nb.AddPage(self.page3, u"hauteur et focale")
        self.nb.AddPage(self.page4, "Zoom")
        # d�finition de l'onglet par d�faut
        self.nb.ChangeSelection(3)
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.chgOnglet, self.nb)
        
        # Bouton quitter
        btnQuit = wx.Button(panel, wx.ID_CLOSE, "Quitter")
        self.Bind(wx.EVT_BUTTON, self.onQuitter, btnQuit)
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        # Ajout des Widgets au sizer
        sizer.Add(self.nb, (0,0),border=2)
        sizer.Add(btnQuit, (1,0))
        
        # Ajout du sizer au panel
        panel.SetSizerAndFit(sizer)
        self.SetClientSize(panel.GetSize())
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
    def chgOnglet(self, evt):
        # mettre une aide en foncion de l'onglet dans la statusbar
        numOnglet = self.nb.GetSelection()
        if numOnglet == 0 :
            self.SetStatusText(statusText)
        if numOnglet == 1 :
            self.SetStatusText(u"Calcul de la largeur et de la focale en fonction de la hauteur � visualiser")
        if numOnglet == 2 :
            self.SetStatusText(u"Calcul de la hauteur et de la focale en fonction de la largeur � visualiser")
        if numOnglet == 3 :
            self.SetStatusText(u"Calcul d'un champ mini/maxi en fonction d'un objectif")
        
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnVideo.Enable(True)
        self.parent.menuModuleVideo.Enable(True)
        self.Destroy()
