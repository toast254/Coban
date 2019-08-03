#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module sonorisation
## Copyright 2008-2010  Stéphan GUÉRIN
## contact : setthe@gmail.com
##
## Ce logiciel est un programme informatique destiné aux électriciens et 
## permettant de calculer rapidement la section d'un câble, de réaliser des
## conversions d'unités électriques, etc.... 
##
## Ce logiciel est régi par la licence CeCILL soumise au droit français et
## respectant les principes de diffusion des logiciels libres. Vous pouvez
## utiliser, modifier et/ou redistribuer ce programme sous les conditions
## de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA 
## sur le site "http://www.cecill.info".
##
## En contrepartie de l'accessibilité au code source et des droits de copie,
## de modification et de redistribution accordés par cette licence, il n'est
## offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
## seule une responsabilité restreinte pèse sur l'auteur du programme,  le
## titulaire des droits patrimoniaux et les concédants successifs.
##
## A cet égard  l'attention de l'utilisateur est attirée sur les risques
## associés au chargement,  à l'utilisation,  à la modification et/ou au
## développement et à la reproduction du logiciel par l'utilisateur étant 
## donné sa spécificité de logiciel libre, qui peut le rendre complexe à 
## manipuler et qui le réserve donc à des développeurs et des professionnels
## avertis possédant  des  connaissances  informatiques approfondies.  Les
## utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
## logiciel à leurs besoins dans des conditions permettant d'assurer la
## sécurité de leurs systèmes et ou de leurs données et, plus généralement, 
## à l'utiliser et l'exploiter dans les mêmes conditions de sécurité. 
##
## Le fait que vous puissiez accéder à cet en-tête signifie que vous avez 
## pris connaissance de la licence CeCILL, et que vous en avez accepté les
## termes.
##
##----------------------------------------------------------------------------------------------

import wx
from math import log10, pow
from modcoban import ValidDigitPoint, testFloat



############################################################################
##                                                                        ##
##                       Module Sonorisation                              ##
##                                                                        ##
##                                                                        ##
############################################################################

version = "0.1.2"

  
class Sono(wx.Frame):
    """Module de calcul de sonorisation"""
       
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title = 'Sono version %s'%version,# size=(500,550), 
                          style=wx.DEFAULT_FRAME_STYLE 
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent = parent
        
        
        ############## Création du panel #########################
        
        panel =  wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        ############## création du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## Création de statusbar #####################
        
        self.CreateStatusBar()
        self.SetStatusText("Consultez l'aide pour plus d'informations")
        
        ############## création des widgets #####################
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        labelDonnee = wx.StaticText(panel, -1, u'Données du projet')
        labelDonnee.SetFont(font)
        # Choix de la surface
        labelDim = wx.StaticText(panel, -1, u'Dimensions en mètres\nlargeur x Longueur x HSP :')
        self.long = wx.TextCtrl(panel, -1, "", size=(60,-1), validator=ValidDigitPoint())
        x1 = wx.StaticText(panel, -1, 'x')
        self.larg = wx.TextCtrl(panel, -1, "", size=(60,-1), validator=ValidDigitPoint())
        x2 = wx.StaticText(panel, -1, 'x')
        self.hsp = wx.TextCtrl(panel, -1, "2.8", size=(60,-1), validator=ValidDigitPoint())
        # Choix du type de diffusion :
        self.lstTypeDif = ["Minimale", "Optimale", "Excellente"]
        lblTypeDiff = wx.StaticText(panel, -1, u'Type de diffusion :')
        self.typeDiff = wx.Choice(panel, -1, (-1,-1), choices = self.lstTypeDif)
        self.typeDiff.SetStringSelection(self.lstTypeDif[1])
        # Choix sensibilité de HP
        labelSensHP = wx.StaticText(panel, -1, u'Sensibilité du HP\n (en db/W à 1m) :')
        self.sensHP = wx.SpinCtrl(panel, -1, "", size=(50,-1))
        self.sensHP.SetRange(60,130)
        self.sensHP.SetValue(88)
        # Choix bruit ambiant 
        labelBruit = wx.StaticText(panel, -1, u'Niveau sonore ambiant\n (en db) :')
        self.bruit = wx.SpinCtrl(panel, -1, "", size=(50,-1))
        self.bruit.SetRange(40,105)
        self.bruit.SetValue(65)
        # séparation
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 5)
        # Résultats
        self.btnCalc = wx.Button(panel, -1, "Calculer")
        self.btnCalc.SetDefault()
        self.btnCalc.SetBackgroundColour('yellow')
        self.Bind(wx.EVT_BUTTON, self.onCalc, self.btnCalc)
        labelResult = wx.StaticText(panel, -1, u"Résultats :")
        labelResult.SetFont(font)
        # résultat distance entre chaque HP
        labelDist = wx.StaticText(panel, -1 ,"Distance maximale\nentre chaque HP :")
        self.dist = wx.StaticText(panel, -1 ,"... m")
        self.dist.SetForegroundColour("blue")
        # résultat nb HP nécessaire
        labelNbHP = wx.StaticText(panel, -1 ,u"Nombre de HP nécessaire :")
        self.nbHP = wx.StaticText(panel, -1 ,"...")
        self.nbHP.SetForegroundColour("blue")
        # résultat puissance réglage de chaque HP
        labelPHP = wx.StaticText(panel, -1 ,u"Puissance de réglage des HP :")
        self.PHP = wx.StaticText(panel, -1 ,"... W")
        self.PHP.SetForegroundColour("blue")
        # bouton "quitter"
        self.btnQuit = wx.Button(panel, -1, "Quitter")
        self.Bind(wx.EVT_BUTTON, self.onQuitter, self.btnQuit)
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        ############### Ajout des wigets au sizer ####################
        self.gbs.Add(labelDonnee, (0,0), span=(1,6), flag=wx.EXPAND)
        self.gbs.Add(labelDim, (1,0))
        self.gbs.Add(self.long, (1,1))
        self.gbs.Add(x1, (1,2))
        self.gbs.Add(self.larg, (1,3))
        self.gbs.Add(x2, (1,4))
        self.gbs.Add(self.hsp,(1,5))
        self.gbs.Add(lblTypeDiff, (2,0))
        self.gbs.Add(self.typeDiff,(2,1), span=(1,4))
        self.gbs.Add(labelSensHP, (3,0))
        self.gbs.Add(self.sensHP, (3,1), span=(1,4))
        self.gbs.Add(labelBruit, (4,0))
        self.gbs.Add(self.bruit, (4,1), span=(1,4))
        self.gbs.Add(self.btnCalc, (5,1), span=(1,4))
        self.gbs.Add(sep, (6,0), (1,6), wx.EXPAND)
        self.gbs.Add(labelResult, (7,0), span=(1,4), flag=wx.EXPAND)
        self.gbs.Add(labelDist, (8,0))
        self.gbs.Add(self.dist, (8,1))
        self.gbs.Add(labelNbHP, (9,0))
        self.gbs.Add(self.nbHP, (9,1), span=(1,4))
        self.gbs.Add(labelPHP, (10,0))
        self.gbs.Add(self.PHP, (10,1))
        self.gbs.Add(self.btnQuit, (11,1), span=(1,5))
        
        panel.SetSizerAndFit(self.gbs)
        self.SetClientSize(panel.GetSize())
        
       
    def onCalc(self, evt):
        long = testFloat(self.long) #<- longueur (float) 0 si erreur
        larg = testFloat(self.larg) #<- largeur (float) 0 si erreur
        hsp = testFloat(self.hsp) #<- hsp (float) 0 si erreur
        sens = self.sensHP.GetValue() #<- sensibilité en db
        bruitAmb = self.bruit.GetValue() #<- bruit ambiant en db
        
        if self.typeDiff.GetStringSelection() == self.lstTypeDif[0]:
            diffdb = 10 #<- db à rajouter (10, 15 ou 25)
            k = 2 #<- coef multiplicateur de hspo pour l'écartement des HP
        elif self.typeDiff.GetStringSelection() == self.lstTypeDif[1]:
            diffdb = 15
            k = 2
        else : 
            diffdb =25
            k = 1.5
        
        dbhp = bruitAmb+diffdb+20*log10(hsp)
        puissHP = round((pow(10,((dbhp-sens)/10))), 2)
        distHPmax = k*hsp
        
        #-----------------------------------------------------------------
        nbHPx = int(long/distHPmax)
        nbHPy = int(larg/distHPmax)
        if nbHPx == 0: nbHPx = 1
        if nbHPy == 0: nbHPy= 1
        nbHP = nbHPx*nbHPy
        #-----------------------------------------------------------------
        
        self.PHP.SetLabel('%s Watts'%puissHP)
        self.dist.SetLabel(u'%s mètres'%distHPmax)
        self.nbHP.SetLabel(u'%s HP préconisés (x=%s  y=%s)'%(nbHP, nbHPx, nbHPy))
        
    
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnSono.Enable(True)
        self.parent.menuModuleSono.Enable(True)
        self.Destroy()
    