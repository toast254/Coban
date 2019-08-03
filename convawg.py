#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module de conversion AWG
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
from math import pow, pi


version = 'AWG <-> mm version 0.1'

############################################################################
##                                                                        ##
##                       Module de conversion AWG <-> mm                  ##
##                            Version 0.1                                 ##
##                                                                        ##
##                                                                        ##
##                                                                        ##
############################################################################
    

  
class Awg(wx.Frame):
    """Module de conversion AWG <-> mm2"""
    
    def __init__(self, parent):
        
        wx.Frame.__init__(self, parent, -1, title = version, size=(500,500), 
                          style=wx.DEFAULT_FRAME_STYLE 
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))# | wx.CLOSE_BOX))
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
        self.SetStatusText("AWG = American Wire Gauge")
        
        ############## création des widgets #####################

        # crée la self.listeAwg de 0000 à 40 (format 'str')
        self.listeAwg = []
        listeZero = ['00','000','0000']
        self.liste1 = range(41) #crée une liste de 0 à 40
        for elem in listeZero: # ajoute les valeurs de listZero à self.liste1
            self.liste1.insert(0, elem)
        for elem in self.liste1 :
            self.listeAwg.append(str(elem))
        
        # ListBox de sélection de l'AWG
        labelSectAwg = wx.StaticText(panel, -1, "Section en AWG :", (15, 50))
        self.lb1 = wx.ListBox(panel, 60, (100, 50), (90, 120), self.listeAwg, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.onConvAwgMm, self.lb1)
        
        # résultats diamètre
        labelDiamMm = wx.StaticText(panel, -1, u"Diamètre : ", style=wx.ALIGN_RIGHT)
        self.diamMm = wx.StaticText(panel, -1, "... mm")
        self.diamMm.SetForegroundColour('red')
        self.diamMm.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # résultats section
        labelSectMm = wx.StaticText(panel, -1, u"Section : ", style=wx.ALIGN_RIGHT)
        self.sectMm = wx.StaticText(panel, -1, "... mm2")
        self.sectMm.SetForegroundColour('red')
        self.sectMm.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # bouton "quitter"
        self.btnQuit = wx.Button(panel, -1, "Quitter")
        self.Bind(wx.EVT_BUTTON, self.onQuitter, self.btnQuit)
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        ############### Ajout des wigets au sizer ####################
        
        self.gbs.Add(labelSectAwg, (0,0))
        self.gbs.Add(self.lb1, (0,1))
        self.gbs.Add(labelDiamMm, (1,0))
        self.gbs.Add(self.diamMm, (1,1))
        self.gbs.Add(labelSectMm, (2,0))
        self.gbs.Add(self.sectMm, (2,1))
        self.gbs.Add(self.btnQuit, (3,2))
                
        panel.SetSizerAndFit(self.gbs)
        self.SetClientSize(panel.GetSize())
        
       
        
    def onConvAwgMm (self, evt):
        """Conversion AWG -> mm """
        
        gauge = self.lb1.GetStringSelection()
        if gauge == self.listeAwg[0] : gauge = -3
        if gauge == self.listeAwg[1] : gauge = -2
        if gauge == self.listeAwg[2] : gauge = -1
        gauge = int(gauge)
        diam = round(11.684/(pow(1.122932, gauge+3)), 2)
        section = (pi/4)*pow(diam, 2)
        
        if section > 10.: section = round(section, 2)
        elif section >= 1: section = round(section, 3)
        else : section = round(section, 4)
        
        # Affichage des résultats
        self.diamMm.SetLabel("%s mm"%diam)
        self.sectMm.SetLabel("%s mm2"%section)  
    

    
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnConvAwg.Enable(True)
        self.parent.menuModuleConvAwg.Enable(True)
        self.Destroy()
    