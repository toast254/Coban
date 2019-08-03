#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module de calcul de chute de tension
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

############################################################################
##                                                                        ##
##                       Module chute de tension                          ##
##                                                                        ##
##                                                                        ##
############################################################################

import wx

version = 'Chute de tension 0.2.2'
sectCu = '1.5 2.5 4 6 10 16 25  35 50 70 95 120 150 185 240 300 400 500 630'.split()
sectAlu = '10 16 25 35 50 70 95 120 150 185 240 300 400 630'.split()
statusText = u"Chute de tension"

      

class ModuleChute(wx.Frame):
    """Calcul des sections de c�ble"""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title = version,
                      style=wx.DEFAULT_FRAME_STYLE 
                      ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent = parent
        
        #------- Cr�ation du panel -----------------------        
        panel =  wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        #---------- cr�ation du sizer principal ----------------
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        #------- Cr�ation de statusbar -----------------        
        self.CreateStatusBar()
        self.SetStatusText(statusText)
        
        #---- Cr�ation de la barre d'outils (toolbar) ---------------------------------------------------

        #-------------- import des images ----------------------
        
        from modcoban import bmp_aide, bmp_quit
        
        img_aide = wx.Bitmap(bmp_aide, wx.BITMAP_TYPE_PNG)
        img_quit = wx.Bitmap(bmp_quit, wx.BITMAP_TYPE_PNG)
        
        self.tbar = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL)
        # Hack pour windows :
        # ajustement de la taille des boutons aux images (24x24 px):
        self.tbar.SetToolBitmapSize((24,24))
        
        self.tbar.AddSimpleTool(90, 
                                img_aide,
                                shortHelpString = u"Aide",
                                longHelpString = u"Valeurs maxi des chutes de tension")
        self.tbar.AddSeparator()
        self.tbar.AddSimpleTool(99, 
                           img_quit,
                           shortHelpString = "Quitter",
                           longHelpString = "Quitter ce module")
        self.tbar.Realize()
        self.SetToolBar(self.tbar)
        
        
        
        #------------- Cr�ation des widgets ---------------------
        # Mono / Tri
        listeCircuit=[u'monophas�', u'triphas�']
        labelMonoTri = wx.StaticText(panel, -1, u'Type de circuit')
        self.monoTri = wx.Choice(panel, -1, choices=listeCircuit)
        self.monoTri.SetSelection(1)
        self.monoTri.SetFocus()
        self.labelCosPhi = wx.StaticText(panel, -1, u'cos Phi = 0,8')
        # type de c�ble :
        listeCable = ['Cuivre', 'Aluminium']
        labelCable = wx.StaticText(panel, -1, u"Type de c�ble")
        self.cable = wx.Choice(panel, -1, choices=listeCable)
        self.cable.SetSelection(0)
        # Longueur du c�ble
        labelLg = wx.StaticText(panel, -1, u'Longueur du c�ble\n(en m�tres) :')
        self.lg = wx.SpinCtrl(panel, -1, "", size=self.cable.GetSize())
        self.lg.SetRange(1, 999)
        self.lg.SetValue(100)
        # Section du conducteur
        labelSection = wx.StaticText(panel, -1, u'Section du conducteur\n (en mm�)')
        self.section = wx.Choice(panel, -1, choices=sectCu, size=self.cable.GetSize())
        self.section.SetSelection(6)
        # Courant d'emploi
        labelCourant = wx.StaticText(panel, -1, u"Courant d'emploi\n(en Amp�res)")
        self.courant = wx.SpinCtrl(panel, -1, "", size=self.cable.GetSize())
        self.courant.SetRange(1,999)
        self.courant.SetValue(100)
        # Tension Ph/N
        labelTension = wx.StaticText(panel, -1, u'Tension entre phase\net neutre (en Volts)')
        listeTension = ['110V', '230V', '240 V', '380 V', '400 V']
        self.tension = wx.Choice(panel, -1, choices=listeTension, size=self.cable.GetSize())
        self.tension.SetSelection(1)
        # Bouton calcul
        self.btnCalc = wx.Button(panel, -1, 'Calculer')
        self.btnCalc.SetBackgroundColour('yellow')
        self.btnCalc.SetDefault()
        if self.parent.licence_ok == 0:
            self.btnCalc.Enable(False)
        # S�paration
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 5)
        # R�sultats
        labelResult = wx.StaticText(panel, -1, u'R�sultats')
        labelResult.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelChuteDelta=wx.StaticText(panel, -1, u'Chute de tension\n(en %)')
        self.labelDeltaU = wx.StaticText(panel, -1, u'... %')
        self.labelDeltaU.SetForegroundColour('blue')
        self.labelDeltaU.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        labelChuteV = wx.StaticText(panel, -1, u'Chute de tension\n(en Volts)')
        self.labelChuteVolt = wx.StaticText(panel, -1, u'... V')
        self.labelChuteVolt.SetForegroundColour('blue')
        self.labelChuteVolt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #------------------ binds ------------------------------
        self.Bind(wx.EVT_CHOICE, self.onSection, self.cable)
        #self.Bind(wx.EVT_CHOICE, self.onRaz, id=wx.ID_ANY)
        self.Bind(wx.EVT_SPINCTRL, self.onRaz)
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
        self.Bind(wx.EVT_TOOL, self.onAide, id=90)
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        self.Bind(wx.EVT_TOOL, self.onQuitter, id=99)
        
        #---------------- placement des widgets ------------------
        self.gbs.Add(labelMonoTri, (0,0))
        self.gbs.Add(self.monoTri, (0,1))
        self.gbs.Add(self.labelCosPhi, (0,2))
        self.gbs.Add(labelCable, (1,0))
        self.gbs.Add(self.cable, (1,1))
        self.gbs.Add(labelLg, (2,0))
        self.gbs.Add(self.lg, (2,1))
        self.gbs.Add(labelSection, (3,0))
        self.gbs.Add(self.section, (3,1))
        self.gbs.Add(labelCourant, (4,0))
        self.gbs.Add(self.courant, (4,1))
        self.gbs.Add(labelTension, (5,0))
        self.gbs.Add(self.tension, (5,1))
        self.gbs.Add(self.btnCalc, (6,2))
        self.gbs.Add(sep, (7,0), (1,4),wx.EXPAND)
        self.gbs.Add(labelResult, (8,0))
        self.gbs.Add(labelChuteDelta, (9,0))
        self.gbs.Add(self.labelDeltaU, (9,1))
        self.gbs.Add(labelChuteV, (10,0))
        self.gbs.Add(self.labelChuteVolt, (10,1))
                
        #-------- r�glage de la taille ---------------------------
        panel.SetSizerAndFit(self.gbs)
        self.SetClientSize(panel.GetSize())
        
        
    def onSection(self, evt):
        if self.cable.GetSelection() == 0 :
            self.section.SetItems(sectCu)
            self.section.SetSelection(6)
        else :
            self.section.SetItems(sectAlu)
            self.section.SetSelection(0)
        
        
        self.onRaz(self)
        
        
        
    def onAide(self, evt):
        msgAide = (u'Alimentation entre disjoncteur de branchement et tableau de r�partition :\n'
                   u'  - Chute de tension maximale : 2%\n\n'
                   u'Installations aliment�es directement � partir d\'un r�seau de '
                   u'distribution publique basse tension :\n'
                   u'  - �clairage : 3 % max\n'
                   u'  - Autres usages : 5 % max\n\n'
                   u'Installations aliment�es � partir d\'un poste HT/BT :\n'
                   u'  - �clairage : 6 % max\n'
                   u'  - Autres usages : 8 % max'
                   )

        dlg = wx.MessageDialog(self, msgAide,
                               u'M�mo Chute de tension',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()
        
    
        
    def onRaz(self, evt):
        self.labelChuteVolt.SetLabel('... V')
        self.labelDeltaU.SetLabel('... %')
        if self.monoTri.GetSelection() == 0:
            self.labelCosPhi.SetLabel(u'')
        else :
            self.labelCosPhi.SetLabel(u'cos Phi = 0,8')
            
        
    def onCalcul(self, evt):
        # import si mono ou tri
        if self.monoTri.GetSelection()==0:
            b = 2
            cosPhi = 1
            sinPhi = 1
        else : 
            b = 1
            cosPhi = 0.8
            sinPhi = 0.6
        # import de la r�sistivit�
        if self.cable.GetSelection() == 0:
            rau1 = 23
        else :
            rau1 = 37
        # import de la longueur
        L = self.lg.GetValue()
        # import de la section
        S = float(self.section.GetStringSelection())
        # import du courant d'emploi
        Ib = self.courant.GetValue()
        # import de la tension
        if self.tension.GetSelection() == 0:
            Uo = 110
        elif self.tension.GetSelection() == 1:
            Uo = 230
        elif self.tension.GetSelection() == 2:
            Uo = 240
        elif self.tension.GetSelection() == 3:
            Uo = 380
        else :
            Uo = 400
        # coef lambda
        Lambda = 0.08
        
        # r�sultats
        u = round((b*(rau1*(L/S)*cosPhi+Lambda*L*sinPhi)*Ib)/1000, 3)
        deltaU = round((100*(u/Uo)), 2)
        self.labelChuteVolt.SetLabel(u'%s V'%u)
        self.labelDeltaU.SetLabel((u'%s '%deltaU)+'%')
    
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnChute.Enable(True)
        self.parent.menuModuleChute.Enable(True)
        self.Destroy()