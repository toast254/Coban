#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module �clairage
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
import pickle, os
from modcoban import ValidDigitPoint, testFloat, icone, testFich, fichierConf


############################################################################
##                                                                        ##
##                       Module "�CLAIRAGE"                               ##
##                                                                        ##
##                                                                        ##
############################################################################
    
version = u'�clairage 0.3.2'

f = open(fichierConf, 'r')
cheminDeSauvegarde = pickle.load(f)
f.close()

# Nom du fichier des sources:
fichsrces = os.path.join(os.path.expanduser(cheminDeSauvegarde),"sources.cob")
#nom du fichier de sauvegarde des pr�f�rences
fichpref = os.path.join(os.path.expanduser(cheminDeSauvegarde),"prefecl.cob")


# Tuple des sources par d�faut:
# Chaque �l�ment du tuple est une liste compos�e du nom (string) et du nombre de lumens (int)
SrcesParDef = (['Fluocompacte 13W', 900],
              ['Fluocompacte 18W', 1200], 
              ['Fluocompacte 26W', 1800],
              ['Tube fluo 18W', 1300],
              ['Tube fluo 36W', 3200],
              ['Tube fluo 58W', 5000]
          )

# liste des pr�f�rences par d�faut
# facteur de d�pr�ciation = 1.0 (float)
# facteur de r�flection = "731" (string)
valDef = [1.,731]

#-----------------------------------------------------------------------------------------
        
def testFichier(f,val) :
    """ teste si le fichier des sources existe, sinon le cr�e avec les valeurs par d�faut"""
    test = testFich(f)
    if test == 0 :
        formatFich(f, val)

def formatFich(f,tup):
    """formate un nouveau fichier en cr�ant une liste � partir du tuple d'entr�e"""
    lst = []
    for elem in tup:
        lst.append(elem)
    fich = open(f,'w')
    pickle.dump(lst, fich)
    fich.close()
    return lst
        
def lireFichier(f, val):
    """ retourne la liste des valeurs du fichier f, 
    sinon le formate avec les valeurs val"""
    testFichier(f,val)
    try :
        fich = open(f, 'r')
        lst = pickle.load(fich)
        fich.close()
        return lst
    except:
        wx.MessageBox(u"Fichier %s corrompu...\n-->Reformatage du fichier."%f, 
                     'Erreur !')
        lst = formatFich(f, val)
        return lst
    
   
#-----------------------------------------------------------------------------------------

class Pref(wx.Frame):
    """Fen�tre des pr�f�rences"""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, u'Pr�f�rences',
                size=wx.DefaultSize,
                style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX| wx.CLOSE_BOX)
            )
        self.parent = parent  
        panel = wx.Panel(self, -1)
        
        # grise l'entr�e du menu et le bouton de la toolbar
        self.parent.menu1Pref.Enable(False)
        self.parent.tbar.EnableTool(wx.ID_PREFERENCES, False)
        
        #--- Variables ---------------------------------------------------------------
        # Facteur de d�pr�ciation pour le calcul (float):
        # - si local � faible empoussi�rement : 1.5
        # - si local � empoussi�rement moyen : 1.75
        # - si local � fort empoussi�rement : 2
        self.fDep = [1.0, 1.25, 1.5, 1.75, 2]
        # Choix du facteur de d�pr�ciation
        # Liste des facteurs de d�pr�ciation au format "string"
        lstFdep = [u'Aucun (1,00)',
                   u'Local � tr�s faible empoussi�rement (1,25)',
                   u"Local � faible empoussi�rement (1,50)",
                   u"Local � empoussi�rement moyen (1,75)",
                   u"Local � fort empoussi�rement (2,00)"]
        lblFDep = wx.StaticText(panel, -1, u"Facteur compensateur\nde d�pr�ciation :")
        self.choixFdep = wx.Choice(panel, -1,(-1,-1), choices = lstFdep)
        self.choixFdep.SetSelection(0)
        # choix des facteurs de r�flexion Plafond/Mur/Plan utile
        lblreflPlaf = wx.StaticText(panel, -1, u"Facteur de r�flexion du plafond")
        self.choixReflPlaf = wx.SpinCtrl(panel, -1, "", size = (60,-1))
        self.choixReflPlaf.SetRange(1,9)
        self.choixReflPlaf.SetValue(7)
        lblreflMur = wx.StaticText(panel, -1, u"Facteur de r�flexion des murs")
        self.choixReflMur = wx.SpinCtrl(panel, -1, "", size = (60,-1))
        self.choixReflMur.SetRange(1,9)
        self.choixReflMur.SetValue(3)
        lblreflPlan = wx.StaticText(panel, -1, u"Facteur de r�flexion du plan utile")
        self.choixReflPlan = wx.SpinCtrl(panel, -1, "", size = (60,-1))
        self.choixReflPlan.SetRange(1,9)
        self.choixReflPlan.SetValue(1)
        # bouton de validation
        btnValid = wx.Button(panel, -1, "Valider")
        btnValid.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onValid, btnValid)
        # bouton d'annulation
        btnAnnul = wx.Button(panel, -1, 'Annuler')
        self.Bind(wx.EVT_BUTTON, self.onAnnul, btnAnnul)
        # ajout des widgets au sizer
        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([lblFDep, self.choixFdep, lblreflPlaf, self.choixReflPlaf, 
                       lblreflMur, self.choixReflMur, lblreflPlan, self.choixReflPlan,
                       btnAnnul, btnValid])
        panel.SetSizerAndFit(sizer)
        self.SetClientSize(panel.GetSize())
        
    def onValid(self,evt):
        # changement du facteur de d�pr�ciation
        self.parent.factDep = self.fDep[self.choixFdep.GetSelection()]        
        # changement du facteur de r�flexion
        plaf = self.choixReflPlaf.GetValue()
        mur = self.choixReflMur.GetValue()
        plan = self.choixReflPlan.GetValue()
        self.parent.factRefl = plaf*100+mur*10+plan
        # �criture du fichier
        formatFich(fichpref, [self.parent.factDep, self.parent.factRefl])
        # RaZ du r�sultat pr�c�dent
        self.parent.nbApp.SetLabel("...")
        self.parent.eclMoy.SetLabel('...')
        self.parent.nbAppPreco.SetLabel('...')
        self.parent.distance.SetLabel('...')
        # modification du label des donn�es
        self.parent.donnees = (u"Facteur de r�flexion Plafond/Mur/Plan utile = %s\n"
                               u"Facteur compensateur de d�pr�ciation = %s"
                               %(self.parent.factRefl,self.parent.factDep))
        self.parent.lbldonnees.SetLabel(self.parent.donnees)
        # d�grise l'entr�e du menu et le bouton de la toolbar
        self.parent.tbar.EnableTool(wx.ID_PREFERENCES, True)
        self.parent.menu1Pref.Enable(True)
        self.MakeModal(False)
        self.Close()
    
    def onAnnul(self, evt):
        # d�grise l'entr�e du menu et le bouton de la toolbar
        self.parent.tbar.EnableTool(wx.ID_PREFERENCES, True)
        self.parent.menu1Pref.Enable(True)
        self.MakeModal(False)
        self.Close()
        

class AjoutSrce(wx.Frame):
    """Ajouter une source"""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Ajouter une nouvelle source', 
                          style=wx.DEFAULT_FRAME_STYLE
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX| wx.CLOSE_BOX))
        self.parent = parent
        
        panel = wx.Panel(self, -1) 
        # grise l'entr�e du menu et le bouton de la toolbar
        self.parent.menu1plus.Enable(False)
        self.parent.tbar.EnableTool(wx.ID_ADD, False)
        
        # nom de la nouvelle source
        LblNomSrce = wx.StaticText(panel, -1, "Nom :")
        self.nomSrce = wx.TextCtrl(panel, -1, "", size=(200, -1))
        self.nomSrce.SetInsertionPoint(0)
        # flux de la nouvelle source
        lblFlux = wx.StaticText(panel, -1, "Flux en Lumens :")
        self.flux = wx.SpinCtrl(panel, -1, "", size=(80,-1))
        self.flux.SetRange(300,99000)
        self.flux.SetValue(1500)
        # bouton de validation
        btnValid = wx.Button(panel, -1, "Valider")
        btnValid.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onValid, btnValid)
        # bouton d'annulation
        btnAnnul = wx.Button(panel, -1, 'Annuler')
        self.Bind(wx.EVT_BUTTON, self.onAnnul, btnAnnul)
        # ajout des widgets au sizer
        sizer = wx.FlexGridSizer(cols=2, hgap=15, vgap=15)
        sizer.AddMany([LblNomSrce, self.nomSrce, lblFlux, self.flux, btnAnnul, btnValid])
        panel.SetSizerAndFit(sizer)
        self.Fit()

    
    def onValid(self,evt):
        """ Ajout de la source � la liste des sources """
        # r�cup�ration des valeurs entr�es
        nomSrce = self.nomSrce.GetValue()
        lm = self.flux.GetValue()
        # ajout de la source cr��e � self.lstSrces
        # + classement par ordre alphab�tique
        self.parent.lstSrces.append([nomSrce, lm])
        self.parent.lstSrces.sort()
        # r��criture du fichier des sources
        f=open(fichsrces, 'w')
        pickle.dump(self.parent.lstSrces, f)
        f.close()
        # Re-cr�ation de la liste de choix du widget self.source
        lst = lireFichier(fichsrces, SrcesParDef)
        self.parent.source.Clear()
        for elem in lst:
            self.parent.source.Append("%s - %s lm"%(elem[0], elem[1]))
        self.parent.source.SetSelection(0) 
        # RaZ du r�sultat pr�c�dent
        self.parent.nbApp.SetLabel("...")
        self.parent.eclMoy.SetLabel('...')
        # d�grise l'entr�e du menu et le bouton de la toolbar
        self.parent.tbar.EnableTool(wx.ID_ADD, True)
        self.parent.menu1plus.Enable(True)
        self.MakeModal(False)
        self.Close(True)
        
    def onAnnul(self, evt):
        # d�grise l'entr�e du menu et le bouton de la toolbar
        self.parent.tbar.EnableTool(wx.ID_ADD, True)
        self.parent.menu1plus.Enable(True)
        self.MakeModal(False)
        self.Close(True)
       
        
class SuppSrce(wx.Frame):
    """Supprimer une source"""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Supprimer une source',
                          style=wx.DEFAULT_FRAME_STYLE
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX| wx.CLOSE_BOX))
        self.parent = parent  
        panel = wx.Panel(self, -1) 
        
        # grise l'entr�e du menu et le bouton de la toolbar
        self.parent.menu1moins.Enable(False)
        self.parent.tbar.EnableTool(wx.ID_REMOVE, False)
        
        # Choix de la source � supprimer
        lblSrce = wx.StaticText(panel, -1, u'Source � supprimer')
        self.srceSup = wx.Choice(panel, -1, (-1,-1), choices=[])
        for elem in self.parent.lstSrces:
            self.srceSup.Append("%s - %s lm"%(elem[0], elem[1]))
        self.srceSup.SetSelection(0)  
        # bouton de validation
        btnValid = wx.Button(panel, -1, "Valider")
        self.Bind(wx.EVT_BUTTON, self.onValid, btnValid)
        # bouton d'annulation
        btnAnnul = wx.Button(panel, -1, "Annuler")
        btnAnnul.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onAnnul, btnAnnul)
        # ajout des widgets au sizer
        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([lblSrce, self.srceSup, btnAnnul, btnValid])
        panel.SetSizerAndFit(sizer)
        self.Fit()
        
    def onValid(self,evt):
        srce = self.srceSup.GetStringSelection()
        dlg = wx.MessageDialog(None, u"Attention, la source %s va �tre supprim�e.\nConfirmer ?"%srce,
                          'Confirmation',
                          wx.YES_NO | wx.ICON_QUESTION)

        result = dlg.ShowModal()
        if result == wx.ID_YES:
            # r�cup�ration l'index de la source � enlever
            index = self.srceSup.GetSelection()
            # lecture et r��criture du fichier des sources
            lst = lireFichier(fichsrces, SrcesParDef)
            lst.pop(index)
            f=open(fichsrces, 'w')
            pickle.dump(lst, f)
            f.close()
            # RaZ du widget self.source
            lst = lireFichier(fichsrces, SrcesParDef)
            self.parent.source.Clear()
            for elem in lst:
                self.parent.source.Append("%s - %s lm"%(elem[0], elem[1]))
            self.parent.source.SetSelection(0) 
            # RaZ du r�sultat pr�c�dent
            self.parent.nbApp.SetLabel("...")
            self.parent.eclMoy.SetLabel('...')
        # d�grise l'entr�e du menu et le bouton de la toolbar
        self.parent.tbar.EnableTool(wx.ID_REMOVE, True)
        self.parent.menu1moins.Enable(True)
        dlg.Destroy()
        self.MakeModal(False)
        self.Close(True)
        
    def onAnnul(self, evt):
        # d�grise l'entr�e du menu et le bouton de la toolbar
        self.parent.tbar.EnableTool(wx.ID_REMOVE, True)
        self.parent.menu1moins.Enable(True)
        self.MakeModal(False)
        self.Close(True)



class Eclairage(wx.Frame):
    """Module de calcul du nombre de luminaire
    en fonction du niveau d'�clairemet requis"""
       
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title = version, size=(500,500), 
                          style=wx.DEFAULT_FRAME_STYLE 
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent = parent
        
        #---- INITIALISATION : ------------------------------------------------------------------------
              
        # r�cup�ration des param�tres par d�faut
        lstDef = lireFichier(fichpref, valDef)
        # Facteur de d�pr�ciation pour le calcul (float):
        self.factDep = lstDef[0]
        # Facteurs de r�flection (string) plafond/mur/plan
        self.factRefl = lstDef[1]
        
        #---- Cr�ation du panel ------------------------------------------------------------------------
        
        panel =  wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        #---- cr�ation du sizer principal -------------------------------------------------------------
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        #---- Cr�ation de statusbar --------------------------------------------------------------------
        
        self.CreateStatusBar()
        self.SetStatusText(u"�clairage int�rieur : Estimation du nombre de luminaires")
        
        #---- Images de la toolbar et des menus --------------------------------------------------------

        from modcoban import bmp_moins, bmp_moins_16, bmp_plus, bmp_plus_16, bmp_pref, bmp_pref_16, bmp_quit, bmp_quit_16, bmp_raz, bmp_raz_16
        
        img_plus = wx.Bitmap(bmp_plus, wx.BITMAP_TYPE_PNG)
        img_moins = wx.Bitmap(bmp_moins, wx.BITMAP_TYPE_PNG)
        img_pref = wx.Bitmap(bmp_pref, wx.BITMAP_TYPE_PNG)
        img_raz = wx.Bitmap(bmp_raz, wx.BITMAP_TYPE_PNG)
        img_quit = wx.Bitmap(bmp_quit, wx.BITMAP_TYPE_PNG)
        img_plus_16 = wx.Bitmap(bmp_plus_16, wx.BITMAP_TYPE_PNG)
        img_moins_16 = wx.Bitmap(bmp_moins_16, wx.BITMAP_TYPE_PNG)
        img_pref_16 = wx.Bitmap(bmp_pref_16, wx.BITMAP_TYPE_PNG)
        img_raz_16 = wx.Bitmap(bmp_raz_16, wx.BITMAP_TYPE_PNG)
        img_quit_16 = wx.Bitmap(bmp_quit_16, wx.BITMAP_TYPE_PNG)
        
        #---- Cr�ation de la barre d'outils (toolbar) ---------------------------------------------------
        
        self.tbar = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL)
        # Hack pour windows :
        # ajustement de la taille des boutons aux images (24x24 px):
        self.tbar.SetToolBitmapSize((24,24))
        
        self.tbar.AddSimpleTool(wx.ID_ADD, 
                           img_plus,
                           shortHelpString = "Ajouter",
                           longHelpString = "Ajouter une source")
        self.tbar.AddSimpleTool(wx.ID_REMOVE, 
                           img_moins,
                           shortHelpString = "Enlever",
                           longHelpString = "Supprimer une source")
        self.tbar.AddSeparator()
        self.tbar.AddSimpleTool(wx.ID_PREFERENCES, 
                           img_pref,
                           shortHelpString = u"R�glages",
                           longHelpString = u"R�glage des param�tres")
        self.tbar.AddSeparator()
        self.tbar.AddSimpleTool(wx.ID_EXIT, 
                           img_quit,
                           shortHelpString = "Quitter",
                           longHelpString = "Quitter ce module")
        self.tbar.Realize()
        self.SetToolBar(self.tbar)
        
        
        #---- CR�ATION DES MENUS -----------------------------------------------------------------------
        
        barreMenu = wx.MenuBar()
        self.menu1 = wx.Menu()
        
        self.menu1plus = wx.MenuItem(self.menu1, wx.ID_ADD, 
                                     u"&Ajouter une source", u"Ajouter une source")
        self.menu1plus.SetBitmap(img_plus_16)
        self.menu1.AppendItem(self.menu1plus)
        self.Bind(wx.EVT_MENU, self.onSrcePlus, self.menu1plus)
        
        self.menu1moins = wx.MenuItem(self.menu1, wx.ID_REMOVE, 
                                      u"&Enlever une source", u"Enlever une source")
        self.menu1moins.SetBitmap(img_moins_16)
        self.menu1.AppendItem(self.menu1moins)
        self.Bind(wx.EVT_MENU, self.onSrceMoins, self.menu1moins)
        self.menu1.AppendSeparator()
        
        self.menu1Raz = wx.MenuItem(self.menu1, wx.ID_REFRESH, 
                                    u'Remise � &z�ro de la liste des sources', u"Revenir aux valeurs d'origine")
        self.menu1Raz.SetBitmap(img_raz_16)
        self.menu1.AppendItem(self.menu1Raz)
        self.Bind(wx.EVT_MENU, self.onRazSrces, self.menu1Raz)
        self.menu1.AppendSeparator()
        
        self.menu1Pref = wx.MenuItem(self.menu1, wx.ID_PREFERENCES, 
                                    u'&R�glages', u'R�glage des param�tres')
        self.menu1Pref.SetBitmap(img_pref_16)
        self.menu1.AppendItem(self.menu1Pref)
        self.Bind(wx.EVT_MENU, self.onPref, self.menu1Pref)
        self.menu1.AppendSeparator()

        self.menu1Quit = wx.MenuItem(self.menu1, wx.ID_EXIT, 
                                    u"Quitter", u"Quitter ce module...")
        self.menu1Quit.SetBitmap(img_quit_16)
        self.menu1.AppendItem(self.menu1Quit)
        self.Bind(wx.EVT_MENU, self.onQuitter, self.menu1Quit)
        
        barreMenu.Append(self.menu1, u"&Pr�f�rences") 
        self.SetMenuBar(barreMenu)
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        #---- cr�ation des widgets ----------------------------------------------------------------------
        # Titres :
        fontTitre = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        lblProjet = wx.StaticText(panel, -1, u"Donn�es du projet")
        lblProjet.SetFont(fontTitre)
        lblResult = wx.StaticText(panel, -1, u"R�sultats")
        lblResult.SetFont(fontTitre)
        # SpinCtrl pour le choix de l'�clairage moyen d�sir�
        lblLux = wx.StaticText(panel, -1, u"Niveau d'�clairement\nrecherch� (en Lux) :")
        self.lux = wx.SpinCtrl(panel, -1, "", size=(60,-1))
        self.lux.SetRange(1,2000)
        self.lux.SetValue(400)
        self.lux.SetFocus()
        # Choix du rendement du luminaire
        lblRendlum = wx.StaticText(panel, -1, u"Rendement du luminaire :\n(en %)")
        self.rendLum = wx.SpinCtrl(panel, -1, "", size=(60,-1))
        self.rendLum.SetRange(1,99)
        self.rendLum.SetValue(70)
        # Classe du luminaire
        lblClasse = wx.StaticText(panel, -1, u'Classe :')
        classe = ['A','B','C','D','E','F','G','H','I','J']
        self.classe = wx.Choice(panel, -1, (-1,-1), choices = classe)
        self.classe.SetSelection(1)
        # Nb de sources par appareil
        lblNbSrce = wx.StaticText(panel, -1, 'Nombre de sources\npar luminaire :')
        self.nbSrce = wx.SpinCtrl(panel, -1, "", size=(60,-1))
        self.nbSrce.SetRange(1,4)
        self.nbSrce.SetValue(2) 
        #Type de source
        lblSource = wx.StaticText(panel, -1, 'Type de source :')
        self.lstSrces=[]
        self.source = wx.Choice(panel, -1, (-1, -1), choices = self.lstSrces)
        self.lstSrces = lireFichier(fichsrces, SrcesParDef)
        for elem in self.lstSrces:
            self.source.Append("%s - %s lm"%(elem[0], elem[1]))
        self.source.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.onRaz, self.source)
        # Longueur de la pi�ce
        lblLongueur = wx.StaticText(panel, -1, u"Longueur de la pi�ce :\n(en m)")
        self.longueur = wx.TextCtrl(panel, -1, "", size=(65, -1), validator=ValidDigitPoint())
        # Largeur de la pi�ce
        lblLargeur = wx.StaticText(panel, -1, u"Largeur de la pi�ce :\n(en m)")
        self.largeur = wx.TextCtrl(panel, -1, "", size=(65, -1), validator=ValidDigitPoint())
        # Hauteur sous plafond
        lblHsp = wx.StaticText(panel, -1, u"Hauteur d'installation\ndu luminaire (en m) :")
        self.hsp = wx.TextCtrl(panel, -1, "", size=(65, -1), validator=ValidDigitPoint())
        # Plan utile
        lblPu = wx.StaticText(panel, -1, u"hauteur du plan utile :\n(en m)")
        self.pu = wx.TextCtrl(panel, -1, "0.8", size=(65, -1), validator=ValidDigitPoint())
        # donn�es du calcul
        self.donnees = (u"Donn�es :\nFacteur de r�flexion Plafond/Mur/Plan utile = %s\n"
                        u"Facteur compensateur de d�pr�ciation = %s"%(self.factRefl,self.factDep))                 
        self.lbldonnees = wx.StaticText(panel, -1, self.donnees)
        self.lbldonnees.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,wx.NORMAL))
        # s�paration
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 5)
        # Nb d'appareil � installer
        fontResult = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        lblNbApp = wx.StaticText(panel, -1,u"Nombre calcul� de luminaires :")
        self.nbApp = wx.StaticText(panel, -1, "...")
        self.nbApp.SetForegroundColour('blue')
        self.nbApp.SetFont(fontResult)
        # Niveau d'�clairement moyen
        lbleclMoy = wx.StaticText(panel, -1, u"Niveau d'�clairement moyen :")
        self.eclMoy = wx.StaticText(panel, -1, "...")
        self.eclMoy.SetForegroundColour('blue')
        self.eclMoy.SetFont(fontResult)
        # Nb d'appareil pr�conis� � installer
        lblNbAppPreco = wx.StaticText(panel, -1,u"Nombre pr�conis� de luminaires :")
        self.nbAppPreco = wx.StaticText(panel, -1, "...")
        self.nbAppPreco.SetForegroundColour('blue')
        self.nbAppPreco.SetFont(fontResult)
        # interdistance des appareils
        lblDistance = wx.StaticText(panel, -1, u"Interdistance maximale :")
        self.distance = wx.StaticText(panel, -1, "...")
        self.distance.SetForegroundColour('blue')
        self.distance.SetFont(fontResult)
        # bouton "calculer"
        self.btnCalc = wx.Button(panel, -1, "calculer")
        self.btnCalc.SetDefault()
        self.btnCalc.SetBackgroundColour('yellow')
        if self.parent.licence_ok == 0:
            self.btnCalc.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
    
        #----- Ajout des wigets au sizer --------------------------------------------------------
        
        self.gbs.Add(lblProjet, (0,0))
        self.gbs.Add(lblLux, (1,0))
        self.gbs.Add(self.lux, (1,1))
        self.gbs.Add(lblRendlum, (1,2))
        self.gbs.Add(self.rendLum, (1,3))
        self.gbs.Add(lblClasse, (1,4))
        self.gbs.Add(self.classe, (1,5))
        
        self.gbs.Add(lblNbSrce, (2,0))
        self.gbs.Add(self.nbSrce, (2,1))
        self.gbs.Add(lblSource, (2,2))
        self.gbs.Add(self.source, (2,3), (1,3), wx.EXPAND)
        
        self.gbs.Add(lblLongueur, (3,0))
        self.gbs.Add(self.longueur, (3,1))
        self.gbs.Add(lblLargeur, (3,2))
        self.gbs.Add(self.largeur, (3,3))
        
        self.gbs.Add(lblHsp, (4,0))
        self.gbs.Add(self.hsp,(4,1))
        self.gbs.Add(lblPu, (4,2))
        self.gbs.Add(self.pu, (4,3))
        
        self.gbs.Add(self.lbldonnees, (5,0), span=(1,3))
        self.gbs.Add(self.btnCalc, (5,4), (1,2), wx.EXPAND)
        
        self.gbs.Add(sep, (6,0), (1,6),wx.EXPAND)
        
        self.gbs.Add(lblResult,(7,0), (1,3))
        
        self.gbs.Add(lblNbApp, (8,0), (1,2))
        self.gbs.Add(self.nbApp, (8,2))
        self.gbs.Add(lbleclMoy, (9,0), (1,2))
        self.gbs.Add(self.eclMoy, (9,2))
        self.gbs.Add(lblNbAppPreco, (10,0), (1,2))
        self.gbs.Add(self.nbAppPreco, (10,2))
        self.gbs.Add(lblDistance, (11,0), (1,2))
        self.gbs.Add(self.distance, (11,2), (1,3))
        
        panel.SetSizerAndFit(self.gbs)
        self.Fit()
        
        
    def onRaz(self, evt):
        # RaZ du r�sultat pr�c�dent
        self.nbApp.SetLabel("...")
        self.eclMoy.SetLabel('...')  
        self.nbAppPreco.SetLabel('...')
        self.distance.SetLabel('...')
    
    def onCalcul(self, evt):
        # cr�ation des utilances :
        ut1 = [0.75, 0.65, 0.55]
        ut3 = [0.85, 0.8, 0.75]
        ut5 = [0.95, 0.9, 0.85]
        # r�cup�ration des valeurs pour le calcul
        longueur = testFloat(self.longueur, 1)
        largeur = testFloat(self.largeur, 1)
        hsp = testFloat(self.hsp, 1)
        pu = testFloat(self.pu, 1)
        lux = self.lux.GetValue()
        nbSrce = self.nbSrce.GetValue()
        factRefl = self.factRefl
        fDep = self.factDep
        # r�cup�ration de la valeur en lumen de la source (int)
        lst = lireFichier(fichsrces, SrcesParDef)
        s = self.source.GetCurrentSelection()
        lm = lst[s][1]
        # R�cup�ration de la classe de l'appareil
        # --> renvoie le coef multiplicateur de la distance maxi 
        # entre 2 appareils
        lstCoef = [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.45, 1.5, 1.5, 1.5]
        coef = lstCoef[self.classe.GetSelection()]
        # Calcul de l'indice K
        K = ((longueur*largeur)/((longueur+largeur)*(hsp-pu)))
        # Calcul de l'utilance ut
        if K < 1:
            if factRefl > 751:
                ut = ut1[0]
            elif factRefl > 731:
                ut = ut1[0]-(((ut1[0]-ut1[1])/20.)*(751-factRefl))
            elif factRefl > 531:
                ut = ut1[1]-(((ut1[1]-ut1[2])/200.)*(731-factRefl))
            else:
                ut = (ut1[2]/531)*factRefl
        elif K < 3:
            if factRefl > 751:
                ut = ut1[0]+((ut3[0]-ut1[0])/2)*(K-1)
            elif factRefl > 731:
                utt1 = ut1[0]+((ut3[0]-ut1[0])/2)*(K-1)
                utt2 = ut1[1]+((ut3[1]-ut1[1])/2)*(K-1)
                ut = utt2+(((utt1-utt2)/20)*(factRefl-731))
            elif factRefl > 531:
                utt1 = ut1[1]+((ut3[1]-ut1[1])/2)*(K-1)
                utt2 = ut1[2]+((ut3[2]-ut1[2])/2)*(K-1)
                ut = utt2+(((utt1-utt2)/200)*(factRefl-531))
            else:
                utt1 = ut1[2]+((ut3[2]-ut1[2])/2)*(K-1)
                ut = (utt1/531)*factRefl
        elif K < 5:
            if factRefl > 751:
                ut = ut3[0]+((ut5[0]-ut3[0])/2)*(K-3)
            elif factRefl > 731:
                utt1 = ut3[0]+((ut5[0]-ut3[0])/2)*(K-3)
                utt2 = ut3[1]+((ut5[1]-ut3[1])/2)*(K-3)
                ut = utt2+(((utt1-utt2)/20)*(factRefl-731))
            elif factRefl > 531:
                utt1 = ut3[1]+((ut5[1]-ut3[1])/2)*(K-3)
                utt2 = ut3[2]+((ut5[2]-ut3[2])/2)*(K-3)
                ut = utt2+(((utt1-utt2)/200)*(factRefl-531))
            else:
                utt1 = ut3[2]+((ut5[2]-ut3[2])/2)*(K-3)
                ut = (utt1/531)*factRefl
        else:
            if factRefl > 751:
                ut = ut5[0]
            elif factRefl > 731:
                ut = ut5[0]-((ut5[0]-ut5[1]/20)*(751-factRefl))
            elif factRefl > 531:
                ut = ut5[1]-((ut5[1]-ut5[2]/200)*(731-factRefl))
            else:
                ut = (ut5[2]/531)*factRefl   
                        
        # facteur d'utilisation :
        r = self.rendLum.GetValue()/100.
        factUtil = ut*r
        # Calcul du flux total � installer :
        ft = (lux*longueur*largeur*fDep)/factUtil
        # Nombre d'appareils
        nbAppMini = int(round(ft/(nbSrce*lm),0))
        if nbAppMini != 1:
            if nbAppMini%2 != 0 :
                nbAppMiniPair = nbAppMini+1
            else :
                nbAppMiniPair = nbAppMini
            # Flux moyen maintenu :
            fluxMoy = int(((nbAppMini*nbSrce*lm*factUtil)/(longueur*largeur*fDep))) 
            
            
            # Placement des appareils selon la classe
            nbAppLargeur = largeur/(coef*(hsp-pu))    
            
            if int(nbAppLargeur) < nbAppLargeur:
                nbAppLargeur = int(nbAppLargeur) + 1
            
            nbAppLongueur = nbAppMiniPair/float(nbAppLargeur)
            
            if int(nbAppLongueur) < nbAppLongueur:
                nbAppLongueur = int(nbAppLongueur +1)
            
            nbAppPreco = nbAppLargeur * nbAppLongueur
            if nbAppPreco < nbAppMiniPair:
                nbAppPreco = nbAppMiniPair
            
            
            #Affichage des r�sultats
            self.nbApp.SetLabel(u"%s" %nbAppMini)
            self.eclMoy.SetLabel(u"%s Lux" %fluxMoy)
            self.nbAppPreco.SetLabel(u"%s soit %s rang�es de %s luminaires" %(int(nbAppPreco), int(nbAppLargeur), int(nbAppLongueur)))
            self.distance.SetLabel(u"%sm" %(coef*hsp))
        else :
            # Flux moyen maintenu :
            fluxMoy = int(((nbAppMini*nbSrce*lm*factUtil)/(longueur*largeur*fDep)))
            #Affichage des r�sultats
            self.nbApp.SetLabel(u"%s" %nbAppMini)
            self.eclMoy.SetLabel(u"%s Lux" %fluxMoy)
            self.nbAppPreco.SetLabel(u"1")
      
    def onSrcePlus(self, evt):
        """Ajoute une source � la liste"""
        dlg = AjoutSrce(self)
        dlg.Show()
        dlg.MakeModal(True)
    
    def onRazSrces(self, evt):
        """ Remise aux valeurs par d�faut de la liste des source"""
        dlg = wx.MessageDialog(None, u"Attention, la liste des sources va �tre r�initialis�e.\nConfirmer ?",
                          'Confirmation',
                          wx.YES_NO | wx.ICON_QUESTION)

        result = dlg.ShowModal()
        if result == wx.ID_YES:
            # r��criture du fichier des sources
            formatFich(fichsrces, SrcesParDef)
            # Recr�ation de la liste des sources
            self.lstSrces = lireFichier(fichsrces, SrcesParDef)
            # Recr�ation de la liste de choix du widget self.source
            self.source.Clear()
            for elem in self.lstSrces:
                self.source.Append("%s - %s lm"%(elem[0], elem[1]))
            self.source.SetSelection(0)
            # RaZ du r�sultat pr�c�dent
            self.nbApp.SetLabel("...")
            self.eclMoy.SetLabel('...')
        
    def onSrceMoins(self, evt):
        dlg = SuppSrce(self)
        dlg.Show()
        dlg.MakeModal(True)
    
    def onPref(self,evt):
        dlg = Pref(self)
        dlg.Show()
        dlg.MakeModal(True)
    
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnEcl.Enable(True)
        self.parent.menuModuleEcl.Enable(True)
        self.Destroy()
    
