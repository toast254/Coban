#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module de calcul de section de cable
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
import  wx.wizard
import os, pickle
from math import pow
from modcoban import testFich

version = u'Section de câble 0.2'

############################################################################
##                                                                        ##
##              Module de calcul de section de câble                      ##
##                                                                        ##
############################################################################

sectCu = ' 1.5 2.5 4 6 10 16 25  35 50 70 95 120 150 185 240 300 400 500 630'.split()
sectAlu = '10 16 25 35 50 70 95 120 150 185 240 300 400 500 630'.split()

def calcSect(section, calibre, f0, coef1, exposant1, coef2, exposant2):
    """ 
    Calcule la section adaptée au calibre du disjoncteur
    --> Paramètres :
    section = sectCu ou sectAlu 
    calibre = calibre du disjoncteur
    f0 = coef appliqué à la méthode (tableau BD et BE NFC 15-105)
    coef1 = coef du tableau A5 ou A6 NFC 15-500 pour une section =< 16mm²
    exposant1 = exposant du tableau A6 NFC 15-500 pour une section =< 16mm²
    coef2 = coef du tableau A5 ou A6 NFC 15-500 pour une section >= 25mm²
    exposant2 = exposant du tableau A6 NFC 15-500 pour une section >= 25mm²
    --> retourne une liste [section, Imax]
    """
    
    for sect in section :
        if float(sect) <= 16 :
            I = int((coef1*pow(float(sect), exposant1))*f0)
            if I >= calibre :
                break
        else :
            I = int((coef2*pow(float(sect), exposant2))*f0)
            if I >= calibre :
                break
            
    return [sect, I]

        
class TitledPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        titleText.SetFont(
                 wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0,
                wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0,
                wx.EXPAND | wx.ALL, 5)

        
class Section(wx.wizard.Wizard):
    def __init__(self, parent):
        wx.wizard.Wizard.__init__(self, parent, -1, title=version)
        self.parent = parent

        #-------------- Création des pages ------------------------
        self.page1 = TitledPage(self, u"Données")
        self.page2 = TitledPage(self, u"Mode de pose")
        self.page3 = TitledPage(self, u"Coefficients")
        self.page4 = TitledPage(self, u"Résultats")

        
        #-------------- Polices -----------------------------------
        
        fontTitre = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        fontMemo = wx.Font(8, wx.SWISS, wx.NORMAL,wx.NORMAL)
        fontResult = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        fontResult2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        #-------------- Page 1 ------------------------------------

        # Choix du calibre du disjoncteur
        lblDisj = wx.StaticText(self.page1, -1, u'Calibre du disjoncteur (en Ampères)')
        lblDisj.SetFont(fontTitre)
        self.disj = wx.SpinCtrl(self.page1, -1, '')
        self.disj.SetRange(1,630)
        self.disj.SetValue(125)
        # Choix du type de circuit (mono ou tri)
        lblCircuit = wx.StaticText(self.page1, -1, u'Type de circuit')
        lblCircuit.SetFont(fontTitre)
        lstCircuit = [u'Monophasé',
                      u'Triphasé']
        self.circuit = wx.Choice(self.page1, -1, choices=lstCircuit)
        self.circuit.SetSelection(1)
        #Choix du type de câble
        lblConducteur = wx.StaticText(self.page1, -1, u"Type de câble :")
        lblConducteur.SetFont(fontTitre)
        lstConducteur = [u'Câble U-1000 R2V multiconducteur',
                         u'Câble U-1000 R2V monoconducteur',
                         u'Câble AR2V multiconducteur',
                         u'Câble AR2V monoconducteur',
                         u'Câble H-07 RNF multiconducteur',
                         u'Câble H-07 RNF monoconducteur',
                         u'Fil H-07 V-U, V-R ou V-K',
                      ]
        self.conducteur = wx.Choice(self.page1, -1, choices=lstConducteur)
        self.conducteur.SetSelection(0)
        # Aide
        sep1 = wx.StaticText(self.page1, -1, u'')
        lblAide = wx.StaticText(self.page1, -1, 
                              u"Aide :\n"
                              u"U-1000 R2V : Câble rigide conducteur Cuivre\n"
                              u"AR2V : Câble rigide conducteur Aluminium\n"
                              u"H07 RNF : Câble souple conducteur Cuivre\n"
                              u"Fil : fil souple ou rigide simple isolation\n")
        lblAide.SetFont(fontMemo)
        
        
        self.page1.sizer.Add(lblDisj)
        self.page1.sizer.Add(self.disj)
        self.page1.sizer.Add(lblCircuit)
        self.page1.sizer.Add(self.circuit)
        self.page1.sizer.Add(lblConducteur)
        self.page1.sizer.Add(self.conducteur)
        self.page1.sizer.Add(sep1)
        self.page1.sizer.Add(lblAide)

        #-------------- Page 2 -----------------------------------
        
        # résumé des choix de la page 1
        lblresum = wx.StaticText(self.page2, -1, u'Résumé :')
        sep1 = wx.StaticText(self.page2, -1, u'')
        self.resCalibre = wx.StaticText(self.page2, -1, u'')
        self.resCalibre.SetFont(fontMemo)
        self.ResCircuit = wx.StaticText(self.page2, -1 ,u'')
        self.ResCircuit.SetFont(fontMemo)
        self.resCable = wx.StaticText(self.page2, -1, u'')
        self.resCable.SetFont(fontMemo)
        sep2 = wx.StaticText(self.page2, -1, u'')
         
        
        # Choix du mode de pose
        lblPose = wx.StaticText(self.page2, -1, u'Mode de pose :')
        lblPose.SetFont(fontTitre)
        self.lstModeDePose=[]
        self.Pose = wx.Choice(self.page2, -1, choices=[], size=(400,-1))
        
        self.page2.sizer.Add(lblresum)
        self.page2.sizer.Add(sep1)
        self.page2.sizer.Add(self.resCalibre)
        self.page2.sizer.Add(self.ResCircuit)
        self.page2.sizer.Add(self.resCable)
        self.page2.sizer.Add(sep2)
        self.page2.sizer.Add(lblPose)
        self.page2.sizer.Add(self.Pose)
        
        #-------------- Page 3 ------------------------------------
        
        # résumé des choix de la page 1 et 2
        lblresum = wx.StaticText(self.page3, -1, u'Résumé :')
        self.resCalibre2 = wx.StaticText(self.page3, -1, u'')
        self.resCalibre2.SetFont(fontMemo)
        self.ResCircuit2 = wx.StaticText(self.page3, -1 ,u'')
        self.ResCircuit2.SetFont(fontMemo)
        self.resCable2 = wx.StaticText(self.page3, -1, u'')
        self.resCable2.SetFont(fontMemo)
        self.resModePose = wx.StaticText(self.page3, -1, u'')
        self.resModePose.SetFont(fontMemo)
        
        sep1 = wx.StaticText(self.page3, -1, u'')
        sep2 = wx.StaticText(self.page3, -1, u'')
        
        self.lblTemp = wx.StaticText(self.page3, -1, u'')
        self.lblTemp.SetFont(fontTitre)
        temp = u'10°C 15°C 20°C 25°C 30°C 35°C 40°C 45°C 50°C 55°C 60°C 65°C 70°C 75°C 80°C'.split()
        self.choixTemp = wx.Choice(self.page3, -1, choices=temp)
        
        self.page3.sizer.Add(lblresum)
        self.page3.sizer.Add(sep1)
        self.page3.sizer.Add(self.resCalibre2)
        self.page3.sizer.Add(self.ResCircuit2)
        self.page3.sizer.Add(self.resCable2)
        self.page3.sizer.Add(self.resModePose)
        self.page3.sizer.Add(sep2)
        self.page3.sizer.Add(self.lblTemp)
        self.page3.sizer.Add(self.choixTemp)
        
        
        #-------------- Page 4 ------------------------------------
        
        # résumé des choix de la page 1 et 2
        lblresum = wx.StaticText(self.page4, -1, u'Résumé :')
        self.resCalibre3 = wx.StaticText(self.page4, -1, u'')
        self.resCalibre3.SetFont(fontMemo)
        self.resCircuit3 = wx.StaticText(self.page4, -1 ,u'')
        self.resCircuit3.SetFont(fontMemo)
        self.resCable3 = wx.StaticText(self.page4, -1, u'')
        self.resCable3.SetFont(fontMemo)
        self.resModePose3 = wx.StaticText(self.page4, -1, u'...')
        self.resModePose3.SetFont(fontMemo)
        self.resTemp3 = wx.StaticText(self.page4, -1, u'')
        self.resTemp3.SetFont(fontMemo)
        
        sep1 = wx.StaticText(self.page3, -1, u'')
        sep2 = wx.StaticText(self.page3, -1, u'')
        
        
        # Résultats 
        lblSection = wx.StaticText(self.page4, -1, u'Section calculée :')
        lblSection.SetFont(fontTitre)
        self.section = wx.StaticText(self.page4, -1, u'')
        self.section.SetFont(fontResult)
        self.section.SetForegroundColour('blue')
        self.Imax = wx.StaticText(self.page4, -1, '')
        self.Imax.SetFont(fontResult2)

        sep3 = wx.StaticText(self.page4, -1, u'')
        
        self.page4.sizer.Add(lblresum)
        self.page4.sizer.Add(sep1)
        self.page4.sizer.Add(self.resCalibre3)
        self.page4.sizer.Add(self.resCircuit3)
        self.page4.sizer.Add(self.resCable3)
        self.page4.sizer.Add(self.resModePose3)
        self.page4.sizer.Add(self.resTemp3)
        self.page4.sizer.Add(sep2)
        self.page4.sizer.Add(lblSection)
        self.page4.sizer.Add(self.section)
        self.page4.sizer.Add(sep3)
        self.page4.sizer.Add(self.Imax)
        

        
        #-------------- Chainage des pages -------------------------
        
        wx.wizard.WizardPageSimple_Chain(self.page1, self.page2)
        wx.wizard.WizardPageSimple_Chain(self.page2, self.page3)
        wx.wizard.WizardPageSimple_Chain(self.page3, self.page4)
        
        #-------------- Taille du wizard --------------------------
        
        self.FitToPage(self.page1)
        
        #-------------- Binds ------------------------------------
        
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnWizPageChanging)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnWizPageChanged)
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        #-------------- Fin du Wizard -------------------------------
        
        if self.RunWizard(self.page1):
            # si le wizard finit correctement
            wx.MessageBox(u"Pensez à vérifier la CHUTE DE TENSION à l'extrémité du câble\n"
                          u"(Consultez l'aide pour plus d'informations)", 
                          u"ATTENTION !!!!!",
                          wx.ICON_EXCLAMATION)
            self.Destroy()
        else :
            # si le wizard ne va pas jusqu'au bout
            self.Destroy()
            
    def OnWizPageChanged(self, evt):
        texts= (('< &Back','< &Retour'),('&Next >','&Suivant >'),('&Cancel','&Annuler'),('&Finish','&Fin'))
        for o in self.GetChildren():
            if 'Button' in str(type(o)):
                for tEng,tFr in texts:
                    if o.GetLabel() == tEng:
                        o.SetLabel(tFr)
        if evt.GetDirection():
            dir = "forward"
        else:
            dir = "backward"
            
    def OnWizPageChanging(self, evt):
        
        #-------------------------- récupération de la page -------------------------------------------
        
        page = evt.GetPage()       
        
        #-------------------------- Appui sur le bouton "NEXT" PAGE 1 ---------------------------------
        
        if evt.GetDirection(): 
            
            #============ Appui sur le bouton "NEXT" PAGE 1  ===================
            # Crée la page 2 en fonction du type de câble
        
            if page is self.page1 :  
                # résumé de la page 1
                self.resCable.SetLabel("Conducteur : %s"%self.conducteur.GetStringSelection())
                self.resCalibre.SetLabel("Calibre : %s A"%self.disj.GetValue())
                self.ResCircuit.SetLabel("Circuit : %s"%self.circuit.GetStringSelection())
                # si le conducteur est un fil
                if self.conducteur.GetSelection() == 6:
                    self.lstModeDePose = [u'Sous conduit encastré dans des parois thermiquement isolantes',
                                          u'Sous conduit en montage apparent',
                                          u'Sous conduit encastré dans des parois'
                                          ]
                    self.Pose.SetItems(self.lstModeDePose)
                    self.Pose.SetSelection(0)
                    
                    self.cond = "fil"
                    self.isolant = "PVC"
                    self.ame = "cuivre"
                    
                #sinon le conducteur est un câble
                else :
                    self.lstModeDePose = [u'Sous conduit encastré dans des parois thermiquement isolantes',
                                          u'Sous conduit en montage apparent',
                                          u'Sous conduit encastré dans des parois',
                                          u'Sur chemin de câble perforé',
                                          u'Sur chemin de câble filaire',
                                          u'Enterré sous fourreau ou conduit',
                                          u'Enterré',
                                          u'Suspendu'
                                          ]
                    self.Pose.SetItems(self.lstModeDePose)
                    self.Pose.SetSelection(1)
                    
                    self.cond = "cable"
                    
                    # si RO2V multi
                    if self.conducteur.GetSelection() == 0 :
                        self.typeCond = "multi"
                        self.isolant = "PR"
                        self.ame = "cuivre"
                        
                    # si R02V mono
                    elif self.conducteur.GetSelection() == 1 : 
                        self.typeCond = "mono"
                        self.isolant = "PR"
                        self.ame = "cuivre"
                        
                    # si AR2V multi
                    elif self.conducteur.GetSelection() == 2 :
                        self.typeCond = "multi"
                        self.isolant = "PR"
                        self.ame = "alu"
                        
                    # si AR2V mono
                    elif self.conducteur.GetSelection() == 3 :
                        self.typeCond = "mono"
                        self.isolant = "PR"
                        self.ame = "alu"
                        
                    # si H07RNF multi
                    elif self.conducteur.GetSelection() == 4 :
                        self.typeCond = "multi"
                        self.isolant = "PVC"
                        self.ame = "cuivre"
                        
                    # si H07RNF mono
                    else :
                        self.typeCond = "mono"
                        self.isolant = "PVC"
                        self.ame = "cuivre"
                
                
                        
                        
                        
                    
            #=========== Appui sur le bouton "NEXT" PAGE 2 =======================
            # Crée la page 3 en fonction du mode de pose

            if page is self.page2 :
                
                # résumé de la page 1 et 2               
                self.resCable2.SetLabel("Conducteur : %s"%self.conducteur.GetStringSelection())
                self.resCalibre2.SetLabel("Calibre : %s A"%self.disj.GetValue())
                self.ResCircuit2.SetLabel("Circuit : %s"%self.circuit.GetStringSelection())
                self.resModePose.SetLabel("Pose : %s"%self.Pose.GetStringSelection())
                
                # teste si le conducteur est un câble ou un fil                
                # si conducteur est un cable
                if self.cond == "cable" :                  
                    # teste si le câble est mono ou multiconducteur
                    
                    # si cable monoconducteur :
                    if self.typeCond == "mono" :
                        
                        # si le conducteur est suspendu
                        if self.Pose.GetSelection() == 7 :
                            self.methode = "F"
                            self.f0 = 1
                            self.f1 = "BF1"
                   
                        # si le conducteur est enterré
                        if self.Pose.GetSelection() == 6 :
                            self.methode = "D"
                            self.f0 = 1
                            self.f1 = "BF2"
                        
                        # si le cond est enterré sous conduit
                        if self.Pose.GetSelection() == 5 :
                            self.methode = "D"
                            self.f0 = 0.8
                            self.f1 = "BF2"
        
                        # Sur chemin de câble filaire
                        if self.Pose.GetSelection() == 4 :
                            self.methode = "F"
                            self.f0 = 1
                            self.f1 = "BF1"
                            
                        # Sur chemin de câble perforé
                        if self.Pose.GetSelection() == 3 :
                            self.methode = "F"
                            self.f0 = 1
                            self.f1 = "BF1"
                        
                        # Sous conduit encastré dans des parois
                        if self.Pose.GetSelection() == 2 :
                            self.methode = "B"
                            self.f0 = 0.9
                            self.f1 = "BF1"
                        
                        # Sous conduit en montage apparent
                        if self.Pose.GetSelection() == 1 :
                            self.methode = "B"
                            self.f0 = 0.9
                            self.f1 = "BF1"
                            
                        # Sous conduit encastré dans des parois thermiquement isolantes
                        if self.Pose.GetSelection() == 0 :
                            self.methode = "B"
                            self.f0 = 0.7
                            self.f1 = "BF1"
                            
                    # si cable multiconducteur :
                    else :
                        # si le conducteur est suspendu
                        if self.Pose.GetSelection() == 7 :
                            self.methode = "E"
                            self.f0 = 1
                            self.f1 = "BF1"
                   
                        # si le conducteur est enterré
                        if self.Pose.GetSelection() == 6 :
                            self.methode = "D"
                            self.f0 = 1
                            self.f1 = "BF2"
                        
                        # si le cond est enterré sous conduit
                        if self.Pose.GetSelection() == 5 :
                            self.methode = "D"
                            self.f0 = 0.8
                            self.f1 = "BF2"
        
                        # Sur chemin de câble filaire
                        if self.Pose.GetSelection() == 4 :
                            self.methode = "E"
                            self.f0 = 1
                            self.f1 = "BF1"
                            
                        # Sur chemin de câble perforé
                        if self.Pose.GetSelection() == 3 :
                            self.methode = "E"
                            self.f0 = 1
                            self.f1 = "BF1"
                        
                        # Sous conduit encastré dans des parois
                        if self.Pose.GetSelection() == 2 :
                            self.methode = "B"
                            self.f0 = 0.9
                            self.f1 = "BF1"
                        
                        # Sous conduit en montage apparent
                        if self.Pose.GetSelection() == 1 :
                            self.methode = "B"
                            self.f0 = 0.9
                            self.f1 = "BF1"
                            
                        # Sous conduit encastré dans des parois thermiquement isolantes
                        if self.Pose.GetSelection() == 0 :
                            self.methode = "B"
                            self.f0 = 0.7
                            self.f1 = "BF1"
                            
                            
                        
                # sinon le conducteur est un fil
                else :
                    # Sous conduit encastré dans des parois
                    if self.Pose.GetSelection() == 2 :
                        self.methode = "B"
                        self.f0 = 1
                        self.f1 = "BF1"
                    
                    # Sous conduit en montage apparent
                    if self.Pose.GetSelection() == 1 :
                        self.methode = "B"
                        self.f0 = 1
                        self.f1 = "BF1"
                    
                    # Sous conduit encastré dans des parois thermiquement isolantes
                    if self.Pose.GetSelection() == 0 :
                        self.methode = "B"
                        self.f0 = 0.77
                        self.f1 = "BF1"                
                
                
                
                #----------------- Choix de la température ambiante en fonction du mode de pose : ---------------
                
                # si mode de pose enterré 
                if self.methode == "D" :
                    self.lblTemp.SetLabel(u'Température du sol :')
                    
                    # si l'isolant est PVC
                    if self.isolant == "PVC":
                        temp = u'10°C 15°C 20°C 25°C 30°C 35°C 40°C 45°C 50°C 55°C 60°C'.split()
                        self.choixTemp.SetItems(temp)
                        # valeur par défaut : 20°C
                        self.choixTemp.SetSelection(2)
                    # si l'isolant est PR
                    else :
                        temp = u'10°C 15°C 20°C 25°C 30°C 35°C 40°C 45°C 50°C 55°C 60°C 65°C 70°C 75°C 80°C'.split()
                        self.choixTemp.SetItems(temp)
                        # valeur par défaut : 20°C
                        self.choixTemp.SetSelection(2)
                    
                # Si autre mode de pose
                else :
                    self.lblTemp.SetLabel(u'Température ambiante :')
                    
                    # si l'isolant est PVC
                    if self.isolant == "PVC":
                        temp = u'10°C 15°C 20°C 25°C 30°C 35°C 40°C 45°C 50°C 55°C 60°C'.split()
                        self.choixTemp.SetItems(temp)
                        # valeur par défaut : 30°C
                        self.choixTemp.SetSelection(4)
                        
                    # sinon si l'isolant est PR
                    else :
                        temp = u'10°C 15°C 20°C 25°C 30°C 35°C 40°C 45°C 50°C 55°C 60°C 65°C 70°C 75°C 80°C'.split()
                        self.choixTemp.SetItems(temp)
                        # valeur par défaut : 30°C
                        self.choixTemp.SetSelection(4)
                        
            #=========== Appui sur le bouton "NEXT" PAGE 3 =======================
            # Crée la page 4 en fonction du mode de pose
            
            if page is self.page3 :
                
                # résumé des pages 1,2 et 3               
                self.resCable3.SetLabel("Conducteur : %s"%self.conducteur.GetStringSelection())
                self.resCalibre3.SetLabel("Calibre : %s A"%self.disj.GetValue())
                self.resCircuit3.SetLabel("Circuit : %s"%self.circuit.GetStringSelection())
                self.resModePose3.SetLabel("Pose : %s"%self.Pose.GetStringSelection())
                self.resTemp3.SetLabel(u'Température: %s' %self.choixTemp.GetStringSelection())
                
                
                # récupération du calibre du disjoncteur et calcul de l'intensité avec le coef f0
                cal = self.disj.GetValue()
                phase = self.circuit.GetSelection()
                
                # récupération de la température et détermination du coef f1
                tempSelect = self.choixTemp.GetSelection()
                # si mode de pose enterré 
                if self.methode == "D" :
                    # si l'isolant est PVC
                    if self.isolant == "PVC":
                        listF1 = [1.10, 1.05, 1.0, 0.95, 0.89, 0.84, 0.77, 0.71, 0.63, 0.55, 0.45]
                        f1 = listF1[tempSelect]
                    # si l'isolant est PR
                    else :
                        listF1 = [1.07, 1.04, 1.0, 0.96, 0.93, 0.89, 0.85, 0.80, 0.76, 0.71, 0.65, 0.6, 0.53, 0.46, 0.38]
                        f1 = listF1[tempSelect]
                        
                # Si autre mode de pose
                else :
                    self.lblTemp.SetLabel(u'Température ambiante :')
                    
                    # si l'isolant est PVC
                    if self.isolant == "PVC":
                        listF1 = [1.22, 1.17, 1.12, 1.06, 1.0, 0.94, 0.87, 0.79, 0.71, 0.61, 0.50]
                        f1 = listF1[tempSelect]
                        
                    # sinon si l'isolant est PR
                    else :
                        listF1 = [1.15, 1.12, 1.08, 1.04, 1.0, 0.94, 0.91, 0.87, 0.82, 0.76, 0.71, 0.65, 0.58, 0.50, 0.41]
                        f1 = listF1[tempSelect]
                
                #------------ Calcul final en fonction de tous les paramètres ------------------------------------
                
                #coef f = f0 x f1
                f = self.f0*f1
                
                # si méthode D --------------------
                if self.methode == "D":
                    # si monophasé
                    if phase == 0 :
                        # si PVC (forcémént cuivre)
                        if self.isolant == "PVC" :
                            result = calcSect(sectCu, cal, f, 25.14, 0.551, 25.14, 0.551)
                            self.section.SetLabel(u'%s mm²'%result[0])
                            self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 29.71, 0.548, 29.71, 0.548)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 22.57, 0.550, 22.57, 0.550)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                    # si triphasé :
                    else :
                        # si PVC (forcémént cuivre)
                        if self.isolant == "PVC" :
                            result = calcSect(sectCu, cal, f, 20.86, 0.550, 20.86, 0.550)
                            self.section.SetLabel(u'%s mm²'%result[0])
                            self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 24.71, 0.549, 24.71, 0.549)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 19., 0.551, 19., 0.551)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                
                # si méthode B --------------------------------------------------------
                if self.methode == "B":
                    # si monophasé
                    if phase == 0 :
                        # si PVC 
                        if self.isolant == "PVC" :
                            # forcément cuivre
                                result = calcSect(sectCu, cal, f, 13.5, 0.625, 12.4, 0.635)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 17.8, 0.623, 16.4, 0.637)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 13,7, 0.623, 12.6, 0.635)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                    # si triphasé :
                    else :
                        # si PVC (forcémént cuivre)
                        if self.isolant == "PVC" :
                            result = calcSect(sectCu, cal, f, 11.84, 0.628, 11.84, 0.628)
                            self.section.SetLabel(u'%s mm²'%result[0])
                            self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 15.0, 0.625, 15.0, 0.625)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 11.6, 0.625, 10.55, 0.640)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                                
                # si méthode C --------------------------------------------------------
                if self.methode == "C":
                    # si monophasé
                    if phase == 0 :
                        # si PVC 
                        if self.isolant == "PVC" :
                            # forcément cuivre
                                result = calcSect(sectCu, cal, f, 15.0, 0.625, 15.0, 0.625)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 18.77, 0.628, 17.0, 0.650)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 14.8, 0.625, 12.6, 0.648)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                    # si triphasé :
                    else :
                        # si PVC (forcémént cuivre)
                        if self.isolant == "PVC" :
                            result = calcSect(sectCu, cal, f, 13.5, 0.625, 12.4, 0.635)
                            self.section.SetLabel(u'%s mm²'%result[0])
                            self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 16.8, 0.620, 15.4, 0.635)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 12.8, 0.627, 11.5, 0.639)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                
                                
                                
                                
                # si méthode E --------------------------------------------------------
                if self.methode == "E":
                    # si monophasé
                    if phase == 0 :
                        # si PVC 
                        if self.isolant == "PVC" :
                            # forcément cuivre
                                result = calcSect(sectCu, cal, f, 16.8, 0.620, 15.4, 0.635)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 20.5, 0.623, 18.6, 0.646)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 16.0, 0.625, 13.4, 0.649)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                    # si triphasé :
                    else :
                        # si PVC (forcémént cuivre)
                        if self.isolant == "PVC" :
                            result = calcSect(sectCu, cal, f, 14.3, 0.620, 12.9, 0.640)
                            self.section.SetLabel(u'%s mm²'%result[0])
                            self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 17.8, 0.623, 16.4, 0.637)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 13.7, 0.623, 12.6, 0.635)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                
                # si méthode F --------------------------------------------------------
                if self.methode == "F":
                    # si monophasé
                    if phase == 0 :
                        # si PVC 
                        if self.isolant == "PVC" :
                            # forcément cuivre
                                result = calcSect(sectCu, cal, f, 17.86, 0.623, 16.4, 0.637)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                                
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 20.8, 0.636, 20.8, 0.636)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 14.7, 0.654, 14.7, 0.654)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                    # si triphasé :
                    else :
                        # si PVC (forcémént cuivre)
                        if self.isolant == "PVC" :
                            result = calcSect(sectCu, cal, f, 15.0, 0.625, 15.0, 0.625)
                            self.section.SetLabel(u'%s mm²'%result[0])
                            self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            
                        # si PR
                        else :
                            # si cuivre
                            if self.ame == "cuivre" :
                                result = calcSect(sectCu, cal, f, 18.77, 0.628, 17.0, 0.650)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                            # si alu
                            if self.ame == "alu" :
                                result = calcSect(sectAlu, cal, f, 14.8, 0.625, 12.6, 0.648)
                                self.section.SetLabel(u'%s mm²'%result[0])
                                self.Imax.SetLabel(u'Intensité admissible maximale : %s A'%result[1])
                                
        if self.parent.licence_ok == 0 :
            self.section.SetLabel(u'... mm² (version de démonstration)')
        
        #------------------------- Appui sur le bouton "BACK" ---------------------------
        else:
            pass
            
            
            
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnSection.Enable(True)
        self.parent.menuModuleSection.Enable(True)
        self.Destroy()

