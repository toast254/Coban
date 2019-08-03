#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module de conversion AWG
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
        
        ############## Cr�ation du panel #########################
        
        panel =  wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## Cr�ation de statusbar #####################
        
        self.CreateStatusBar()
        self.SetStatusText("AWG = American Wire Gauge")
        
        ############## cr�ation des widgets #####################

        # cr�e la self.listeAwg de 0000 � 40 (format 'str')
        self.listeAwg = []
        listeZero = ['00','000','0000']
        self.liste1 = range(41) #cr�e une liste de 0 � 40
        for elem in listeZero: # ajoute les valeurs de listZero � self.liste1
            self.liste1.insert(0, elem)
        for elem in self.liste1 :
            self.listeAwg.append(str(elem))
        
        # ListBox de s�lection de l'AWG
        labelSectAwg = wx.StaticText(panel, -1, "Section en AWG :", (15, 50))
        self.lb1 = wx.ListBox(panel, 60, (100, 50), (90, 120), self.listeAwg, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.onConvAwgMm, self.lb1)
        
        # r�sultats diam�tre
        labelDiamMm = wx.StaticText(panel, -1, u"Diam�tre : ", style=wx.ALIGN_RIGHT)
        self.diamMm = wx.StaticText(panel, -1, "... mm")
        self.diamMm.SetForegroundColour('red')
        self.diamMm.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # r�sultats section
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
        
        # Affichage des r�sultats
        self.diamMm.SetLabel("%s mm"%diam)
        self.sectMm.SetLabel("%s mm2"%section)  
    

    
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnConvAwg.Enable(True)
        self.parent.menuModuleConvAwg.Enable(True)
        self.Destroy()
    