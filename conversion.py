#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module de conversions électriques
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

############################################################################
##                                                                        ##
##                       Module de conversions                            ##
##                            électriques                                 ##
##                                                                        ##
############################################################################
    
version = "0.1.8"
    
    
class ModuleConv(wx.Frame):
    """Module de conversion"""
       
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title = 'Conversions %s'%version,  
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
        self.SetStatusText("Entrez une valeur puis cliquez sur convertir")
        
        ############## création des widgets #####################
        
        # Choix de la tension
        self.listetension = [u'220V monophasé', 
                             u'230V monophasé',
                             u'240V monophasé', 
                             u'380V triphasé cosPhi = 0.8', 
                             u'400V triphasé cosPhi = 0.8']
        self.tension = wx.RadioBox(panel, -1, u" Tension d'emploi ", 
                                   (-1, -1), wx.DefaultSize, self.listetension, 1, 
                                   style = wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.onChoixTension, self.tension)
        
        # Choix du type de conversion
        self.listeConversion = [u'Ampères (A)', u'Watts (W)', u'Chevaux (CV)', 'Horse Power (HP)']
        self.Conversion = wx.Choice(panel, -1, choices=self.listeConversion)
        self.Conversion.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.onChoixUnite, self.Conversion)
        
        # Choix de la valeur à convertir
        self.Valeur = wx.SpinCtrl(panel, -1, "")
        self.Valeur.SetRange(1,650)
        self.Valeur.SetValue(100)
        
        # bouton "convertir" (par défaut)
        self.btnConv = wx.Button(panel, -1, "Convertir")
        self.btnConv.SetBackgroundColour('yellow')
        self.btnConv.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onConvertir, self.btnConv)
        
        # séparation
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 5)
        
        # fenêtre des résultats
        labelResult = wx.StaticText(panel, -1, u"Résultats :")
        self.Result1 = wx.StaticText(panel, -1, '...', (-1,-1), (120,-1), wx.ALIGN_LEFT)
        self.Result1.SetForegroundColour('blue')
        self.Result1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.unite1 = wx.StaticText(panel, -1, 'W')
        self.unite1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.Result2 = wx.StaticText(panel, -1, '...')
        self.Result2.SetForegroundColour('blue')
        self.Result2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.unite2 = wx.StaticText(panel, -1, 'CV')
        self.unite2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.Result3 = wx.StaticText(panel, -1, '...')
        self.Result3.SetForegroundColour('blue')
        self.Result3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.unite3 = wx.StaticText(panel, -1, 'HP')
        self.unite3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # bouton "quitter"
        self.btnQuit = wx.Button(panel, -1, "Quitter")
        self.Bind(wx.EVT_BUTTON, self.onQuitter, self.btnQuit)
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        ############### Ajout des wigets au sizer ####################
        self.gbs.Add(self.tension, (1,0), (1,3), wx.EXPAND)
        self.gbs.Add(self.Valeur, (2,0))
        self.gbs.Add(self.Conversion, pos=(2,1), span=(1,2), flag=wx.EXPAND)
        self.gbs.Add(self.btnConv, (4,2))
        self.gbs.Add(sep, (6,0), (1,3), wx.EXPAND)
        self.gbs.Add(labelResult, (7,0))
        self.gbs.Add(self.Result1, (7,1))
        self.gbs.Add(self.unite1, (7,2))
        self.gbs.Add(self.Result2, (8,1))
        self.gbs.Add(self.unite2, (8,2))
        self.gbs.Add(self.Result3, (9,1))
        self.gbs.Add(self.unite3, (9,2))
        self.gbs.Add(self.btnQuit, (11,2))
        
        panel.SetSizerAndFit(self.gbs)
        self.SetClientSize(panel.GetSize())
        
    def onChoixTension(self, evt):
        """ RaZ des résultats précédents lors du choix de la tension """
        self.Result1.SetLabel("...")
        self.Result2.SetLabel("...")
        self.Result3.SetLabel("...")
       
        
    def onChoixUnite(self, evt):
        """Choisit les unités à convertir """
        # permet de fixer les valeurs du spinctrl
        def setValeur(range1, range2, value, label1, label2, label3):
            self.Valeur.SetRange(range1, range2)
            self.Valeur.SetValue(value)
            self.unite1.SetLabel(label1)
            self.unite2.SetLabel(label2)
            self.unite3.SetLabel(label3)
        
        # Permet de choisir les unité converties de sortie
        unite = self.Conversion.GetStringSelection()
        # de HP à A,W,CV
        if unite == self.listeConversion[3]:
            setValeur(1, 489, 5, 'A', 'W', 'CV')
        # de CV à A,W,HP
        elif unite == self.listeConversion[2]:
            setValeur(1, 489, 5, 'A', 'W', 'HP')
        # de W à CV,A,HP
        elif unite == self.listeConversion[1]: 
            setValeur(1,360000,5000,'A','CV','HP')
        # de A à W,CV,HP
        elif unite == self.listeConversion[0] :
            setValeur(1,650,100,'W','CV','HP')
        # Raz des résultats
        self.Result1.SetLabel("...")
        self.Result2.SetLabel("...")
        self.Result3.SetLabel("...")
    
    def onConvertir(self, evt):
        #Choix de la tension et du coef (cos phi x sqr(3) ou 1)
        if self.tension.GetStringSelection() == self.listetension[0]:
            U = 220.
            coef = 1.
        elif self.tension.GetStringSelection() == self.listetension[1]:
            U = 230.
            coef = 1.
        elif self.tension.GetStringSelection() == self.listetension[2]:
            U = 240.
            coef = 1.
        elif self.tension.GetStringSelection() == self.listetension[3]:
            U = 380.
            coef = 1.38564
        else :
            U = 400.
            coef = 1.38564
        # import de la valeur
        val = self.Valeur.GetValue()
        
        if self.Conversion.GetStringSelection() == self.listeConversion[3]:
            # conv HP ->CV,A,W
            i = round(((val*735.5)/(U*coef)), 2)
            self.Result1.SetLabel('%s' %i)
            p = round(val*735.5, 2)
            self.Result2.SetLabel('%s' %p)
            cv = round((val*(735.5/745.7)), 2)
            self.Result3.SetLabel('%s' %cv)
        
        elif self.Conversion.GetStringSelection() == self.listeConversion[2]:
            # conv CV->A,W,HP
            i = round(((val*735.5)/(U*coef)), 2)
            self.Result1.SetLabel('%s' %i)
            p = round(val*735.5, 2)
            self.Result2.SetLabel('%s' %p)
            hp = round((val*(745.7/735.5)), 2)
            self.Result3.SetLabel('%s' %hp)
                      
        elif self.Conversion.GetStringSelection() == self.listeConversion[1]:
            # conv W->A,CV,HP
            i = round((val/(U*coef)), 2)
            self.Result1.SetLabel('%s' %i)
            cv = round((val/735.5), 2)
            self.Result2.SetLabel('%s' %cv)
            hp = round((val/745.7), 2)
            self.Result3.SetLabel('%s' %hp)
        else :
            # conv A->W,CV,HP
            p = int((U*val*coef))
            self.Result1.SetLabel('%s' %p)
            cv = round(((U*val*coef)/735.5), 2)
            self.Result2.SetLabel('%s' %cv)
            hp = round(((U*val*coef)/745.7), 2)
            self.Result3.SetLabel('%s' %hp)
    
    
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnConv.Enable(True)
        self.parent.menuModuleConversion.Enable(True)
        self.Destroy()
    