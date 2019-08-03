#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module de conversions �lectriques
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

############################################################################
##                                                                        ##
##                       Module de conversions                            ##
##                            �lectriques                                 ##
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
        
        ############## Cr�ation du panel #########################
        
        panel =  wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## Cr�ation de statusbar #####################
        
        self.CreateStatusBar()
        self.SetStatusText("Entrez une valeur puis cliquez sur convertir")
        
        ############## cr�ation des widgets #####################
        
        # Choix de la tension
        self.listetension = [u'220V monophas�', 
                             u'230V monophas�',
                             u'240V monophas�', 
                             u'380V triphas� cosPhi = 0.8', 
                             u'400V triphas� cosPhi = 0.8']
        self.tension = wx.RadioBox(panel, -1, u" Tension d'emploi ", 
                                   (-1, -1), wx.DefaultSize, self.listetension, 1, 
                                   style = wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.onChoixTension, self.tension)
        
        # Choix du type de conversion
        self.listeConversion = [u'Amp�res (A)', u'Watts (W)', u'Chevaux (CV)', 'Horse Power (HP)']
        self.Conversion = wx.Choice(panel, -1, choices=self.listeConversion)
        self.Conversion.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.onChoixUnite, self.Conversion)
        
        # Choix de la valeur � convertir
        self.Valeur = wx.SpinCtrl(panel, -1, "")
        self.Valeur.SetRange(1,650)
        self.Valeur.SetValue(100)
        
        # bouton "convertir" (par d�faut)
        self.btnConv = wx.Button(panel, -1, "Convertir")
        self.btnConv.SetBackgroundColour('yellow')
        self.btnConv.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onConvertir, self.btnConv)
        
        # s�paration
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 5)
        
        # fen�tre des r�sultats
        labelResult = wx.StaticText(panel, -1, u"R�sultats :")
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
        """ RaZ des r�sultats pr�c�dents lors du choix de la tension """
        self.Result1.SetLabel("...")
        self.Result2.SetLabel("...")
        self.Result3.SetLabel("...")
       
        
    def onChoixUnite(self, evt):
        """Choisit les unit�s � convertir """
        # permet de fixer les valeurs du spinctrl
        def setValeur(range1, range2, value, label1, label2, label3):
            self.Valeur.SetRange(range1, range2)
            self.Valeur.SetValue(value)
            self.unite1.SetLabel(label1)
            self.unite2.SetLabel(label2)
            self.unite3.SetLabel(label3)
        
        # Permet de choisir les unit� converties de sortie
        unite = self.Conversion.GetStringSelection()
        # de HP � A,W,CV
        if unite == self.listeConversion[3]:
            setValeur(1, 489, 5, 'A', 'W', 'CV')
        # de CV � A,W,HP
        elif unite == self.listeConversion[2]:
            setValeur(1, 489, 5, 'A', 'W', 'HP')
        # de W � CV,A,HP
        elif unite == self.listeConversion[1]: 
            setValeur(1,360000,5000,'A','CV','HP')
        # de A � W,CV,HP
        elif unite == self.listeConversion[0] :
            setValeur(1,650,100,'W','CV','HP')
        # Raz des r�sultats
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
    