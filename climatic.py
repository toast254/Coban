#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module Climatic
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
import pickle, os
from modcoban import icone, ValidDigitPoint, ValidDigitPoint2, testFloat, testFloatCalc, testFich, fichierConf


############################################################################
##                                                                        ##
##                       Module Climatic                                  ##
##                                                                        ##
##                                                                        ##
############################################################################

version = "0.2"

#----------- fichier de sauvegarde des préférences -----------

f = open(fichierConf, 'r')
path = pickle.load(f)
f.close()

fichierPref = os.path.join(os.path.expanduser(path), "prefcalo.cob")

# valeurs par défaut du fichier des sauvegarde des préférences
valDef = [33,85,80]

#----------- messages d'aide -----------------------

aidePlancher = (u'Surface de la pièce en m².\n'
                u'* Pour les salles de bains, penser à enlever la\n'
                u'  surface occupée par la baignoire et/ou la douche\n'
                u'* Pour les cuisines, penser à enlever la\n'
                u'  surface occupée par les éléments de cuisine.'
                u'\n\n*** ASTUCE ! ***\nVous pouvez entrer directement\n'
                u'votre calcul de surface (longueur * largeur).\n'
                u'ex: 7.43*3.7')
aideAutre = u'Surface de la pièce en m².'


#---------------------------------------------------------------------------

def testPref(f) :
    test = testFich(f)
    if test == 0 :
        fich = open(f,'w')
        pickle.dump(valDef, fich)
        fich.close()


def lireDef(f):
    """ retourne la liste des valeurs du fichier des préférences """
    testPref(f)
    fich = open(f, 'r')
    lstPdef = pickle.load(fich)
    fich.close()
    return lstPdef


#---------------------------------------------------------------------------

class Pref(wx.Frame):
    """Fenêtre des préférences pour l'onglet chauffage domestique"""
       
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE,
            ):

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.parent = parent
        
        #----------- Création du panel ------------------
        panel = wx.Panel(self, -1)
        
        #------- création du sizer principal -----------------
        gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        #--------- Lecture des valeurs par défaut ------------
        lst = lireDef(fichierPref)
        PpannDef = lst[0]
        PplanDef = lst[1]
        Paccudef = lst[2]
        
        #--------- Création des widgets --------------------
        labelPpann = wx.StaticText(panel, -1, 'Chauffage par panneaux rayonnants :\nPuissance en Watts/m3 :')
        self.Ppann = wx.SpinCtrl(panel, -1, "", size=(50,-1))
        self.Ppann.SetRange(1,150)
        self.Ppann.SetValue(PpannDef)
        
        labelPplan = wx.StaticText(panel, -1, u'Chauffage par câble chauffant :\nPuissance en Watts/m² :')
        self.Pplan = wx.SpinCtrl(panel, -1, "", size=(50,-1))
        self.Pplan.SetRange(1,150)
        self.Pplan.SetValue(PplanDef)
        
        labelPaccu = wx.StaticText(panel, -1, 'Chauffage par accumulateurs :\nPuissance en Watts/m3 :')
        self.Paccu = wx.SpinCtrl(panel, -1, "", size=(50,-1))
        self.Paccu.SetRange(1,400)
        self.Paccu.SetValue(Paccudef)
        
        btnValid = wx.Button(panel, -1, "Valider")
        btnValid.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onValid, btnValid)
        
        btnReset = wx.Button(panel, -1, u"Valeurs par défaut")
        self.Bind(wx.EVT_BUTTON, self.onReset, btnReset)
        
        #-------------- Ajout des wigets au sizer --------------------
        
        gbs.Add(labelPpann, (0,0))
        gbs.Add(labelPplan, (1,0))
        gbs.Add(labelPaccu, (2,0))
        gbs.Add(self.Ppann, (0,1))
        gbs.Add(self.Pplan, (1,1))
        gbs.Add(self.Paccu, (2,1))
        gbs.Add(btnValid, (3,2))
        gbs.Add(btnReset, (3,0))
        
        panel.SetSizerAndFit(gbs)
        self.SetClientSize(panel.GetSize())
    
    def onReset(self,evt):
        self.Ppann.SetValue(valDef[0])
        self.Pplan.SetValue(valDef[1])
        self.Paccu.SetValue(valDef[2])


    def onValid(self, event):
        testPref(fichierPref)
        f= open(fichierPref, "w")
        pan = self.Ppann.GetValue()
        plan = self.Pplan.GetValue()
        accu = self.Paccu.GetValue()
        pickle.dump([pan, plan, accu], f)
        f.close()
        
            
        #--------- Lecture des coefs par défaut ------------
        lst = lireDef(fichierPref)
        PpannDef = lst[0]
        PplanDef = lst[1]
        Paccudef = lst[2]
        
        # modification dans la fenetre chauffage de l'affichage de la puissance de calcul et du résultat
        if self.parent.typeChauf.GetStringSelection() == self.parent.listeTypeChauf[0]: # si panneau
            self.parent.labelTypeCalc.SetLabel("%s W/m3"%PpannDef)
        elif self.parent.typeChauf.GetStringSelection() == self.parent.listeTypeChauf[2]: # si accu
            self.parent.labelTypeCalc.SetLabel("%s W/m3"%Paccudef)
        else : # si plancher
            self.parent.labelTypeCalc.SetLabel(u"%s Wm²2"%PplanDef)
        
        self.parent.pCalc.SetLabel('... W')
        self.parent.pSup.SetLabel('')
        
        # enlève la propriétée "modale" de la fenêtre
        self.MakeModal(False)
        self.Close(True)
        
        


#---------------------------------------------------------------------------



class OngletChauffDomestique(wx.Panel):
    """Calcul d'un champ de vision en fonction d'une distance"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## création du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        #--------- Lecture des coefs par défaut ------------
        lst = lireDef(fichierPref)
        PplanDef = lst[1]
        
        ############## création des widgets #####################
        
        # titres
        fontTitre = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        lblProjet = wx.StaticText(self, -1, u"Données du projet")
        lblProjet.SetFont(fontTitre)
        lblResult = wx.StaticText(self, -1, u"Résultats")
        lblResult.SetFont(fontTitre)
        
        # Choix de sélection du type de chauffage
        self.listeTypeChauf = ['Radiateurs',u'Câble chauffant','Accumulateurs']
        labelType = wx.StaticText(self, -1, u"Mode de chauffage :")
        self.typeChauf = wx.Choice(self, -1, (-1, -1), choices = self.listeTypeChauf)
        self.typeChauf.SetStringSelection(self.listeTypeChauf[1])
        
        # bouton de choix des paramètres
        from modcoban import bmp_pref
        img_pref = wx.Bitmap(bmp_pref, wx.BITMAP_TYPE_PNG)
        self.btnPrefs = wx.BitmapButton(self, -1, img_pref)
        
        # Choix de la surface
        labelSurface = wx.StaticText(self, -1, u'Surface (en m²) :')
        self.surface = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint2())
        self.surface.SetToolTipString(aidePlancher)
        self.bain = wx.CheckBox(self, -1, "Salle de bain ?")
        self.bain.SetToolTipString(u'Cocher cette case si la pièce est une salle de bain')
        
        # Choix hauteur sous plafond
        labelHsp= wx.StaticText(self, -1, 'H.S.P. (en m) :')
        self.hsp = wx.TextCtrl(self, -1, "2.5", validator = ValidDigitPoint())
        self.hsp.SetToolTipString(u'Hauteur sous plafond en mètres')
        
        # séparation
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        
        # Fenêtre "mode de calcul"
        labelModeCalc = wx.StaticText(self, -1, u"Mode de calcul : ")
        labelModeCalc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,wx.NORMAL))
        self.labelTypeCalc = wx.StaticText(self, -1, u"%s W/m²"%PplanDef)
        self.labelTypeCalc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,wx.NORMAL))
        
        # Fenêtre "Puissance calculée"
        labelPCalc = wx.StaticText(self, -1, u"Puissance calculée :", style=wx.ALIGN_RIGHT)
        self.pCalc = wx.StaticText(self, -1, '... W')
        self.pCalc.SetForegroundColour('blue')
        self.pCalc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.labelPsup = wx.StaticText(self, -1, u'Puissance\ncomplémentaire :')
        self.pSup = wx.StaticText(self, -1, u'')
        
        # bouton Calcul
        self.btnCalc = wx.Button(self, -1, "calculer")
        self.btnCalc.SetDefault()
        self.btnCalc.SetBackgroundColour('yellow')
        if self.parent.licence == 0:
            self.btnCalc.Enable(False)
            
        #-------------- Binds -------------------
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalc)
        self.Bind(wx.EVT_BUTTON, self.onPref, self.btnPrefs)
        self.typeChauf.Bind(wx.EVT_CHOICE, self.onTypeChauf, self.typeChauf)
            
            
        self.gbs.Add(lblProjet, (0,0), (1,2), wx.EXPAND)
        
        self.gbs.Add(labelType, (1,0))
        self.gbs.Add(self.typeChauf, (1,1),(1,2),wx.EXPAND)
        self.gbs.Add(self.btnPrefs, (1,3))
        
        self.gbs.Add(labelSurface, (2,0))
        self.gbs.Add(self.surface, (2,1))
        self.gbs.Add(self.bain, (2,2))
        
        self.gbs.Add(labelHsp, (3,0))
        self.gbs.Add(self.hsp, (3,1))
        
        self.gbs.Add(self.btnCalc, (4,2))
        
        self.gbs.Add(sep, (5,0), (1,3),wx.EXPAND)
        
        self.gbs.Add(lblResult, (6,0))
        
        self.gbs.Add(labelModeCalc, (7,0))
        self.gbs.Add(self.labelTypeCalc, (7,1))
        
        self.gbs.Add(labelPCalc, (8,0))
        self.gbs.Add(self.pCalc, (8,1))
        
        self.gbs.Add(self.labelPsup, (9,0))
        self.gbs.Add(self.pSup, (9,1))
        
        self.SetSizerAndFit(self.gbs)
        
        
        
    def onTypeChauf(self, evt):
        """Modifie les paramètres en fonction du type de chauffage"""
        
        #--------- Lecture des coefs par défaut ------------
        lst = lireDef(fichierPref)
        PpannDef = lst[0]
        PplanDef = lst[1]
        Paccudef = lst[2]
        
        self.pCalc.SetLabel('... W')
        self.labelPsup.SetLabel('')
        self.pSup.SetLabel('')
        
        if self.typeChauf.GetStringSelection() != self.listeTypeChauf[1]: # si panneau ou accu
            self.bain.Enable(False)
            self.bain.Set3StateValue(wx.CHK_UNCHECKED)
            self.surface.SetToolTipString(aideAutre)
            if self.typeChauf.GetStringSelection() == self.listeTypeChauf[0]: # si panneau
                self.labelTypeCalc.SetLabel("%s W/m3"%PpannDef)
            else : # si accu
                self.labelTypeCalc.SetLabel("%s W/m3"%Paccudef)
            
        else : # si plancher
            self.bain.Enable(True)
            self.surface.SetToolTipString(aidePlancher)
            self.labelTypeCalc.SetLabel(u"%s W/m²"%PplanDef)
        
        
    def onPref(self, evt):
        testPref(fichierPref)
        dlg = Pref(self, -1, u"Réglages", size=(350, 200),
                   style=wx.DEFAULT_FRAME_STYLE 
                   ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX| wx.CLOSE_BOX))
        icone(dlg)
        dlg.Show(True) 
        # la fenêtre des préférence devient modale
        dlg.MakeModal(True)
        
        
        
    def onCalcul (self, evt):
        """Calcul de la puissance calorifique"""
        
        #--------- Récupération des valeurs saisies -----------
        s = testFloatCalc(self.surface)
        self.surface.SetValue(str(round(s, 1)))
        h = testFloat(self.hsp)
        vol = s*h
        chauf = self.typeChauf.GetStringSelection()
        bain = self.bain.Get3StateValue()
        
        #--------- Lecture des coefs par défaut ------------
        lst = lireDef(fichierPref)
        PpannDef = lst[0]
        PplanDef = lst[1]
        Paccudef = lst[2]
        
        if chauf == self.listeTypeChauf[0]: # panneaux
            p = int(vol*PpannDef)
        if chauf == self.listeTypeChauf[1]: # plancher
            if bain == 0:
                s = s*0.85
                p = int(s*PplanDef)
            else :
                p = int(s*PplanDef)
            
            # si hsp > 2,5m, calcul de P supp à installer
            if h > 2.5 :
                p2 = int(vol*PpannDef)-p
                self.labelPsup.SetLabel(u'Puissance\ncomplémentaire :')
                self.pSup.SetLabel(u'%s W'%p2)
                self.pSup.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
            else :
                self.labelPsup.SetLabel('')
                self.pSup.SetLabel('')
                
        if chauf == self.listeTypeChauf[2]: # accus
            p = int(vol*Paccudef)
            
        self.pCalc.SetLabel('%s W'%p)
        
        
        
        
        
        
        
        
class OngletChauffIndus(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## création du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## création des widgets #####################
        
        #--------------- création des widgets --------------------

        # insertion de l'image
        def opj(path):
            """Convert paths to the platform-specific separator"""
            st = apply(os.path.join, tuple(path.split('/')))
            # HACK: on Linux, a leading / gets lost...
            if path.startswith('/'):
                st = '/' + st
            return st
        pos = 100
        img = wx.Image(opj('images/france.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        pos = pos + img.GetHeight() + 10
        self.carte = wx.StaticBitmap(self, -1, img, (10, pos), (img.GetWidth(), img.GetHeight()))
        
        # choix de la zone
        btnSize = (25,25)
        lblChoixZone = wx.StaticText(self, -1, u"Emplacement du local:")
        self.btnRouge = wx.Button(self, 100, "", size=btnSize)
        self.btnRouge.SetBackgroundColour('red')
        self.btnVert = wx.Button(self, 102, "", size=btnSize)
        self.btnVert.SetBackgroundColour('green')
        self.btnBleu = wx.Button(self, 101, "", size=btnSize)
        self.btnBleu.SetBackgroundColour('blue')        
        self.btnJaune = wx.Button(self, 103, "", size=btnSize)
        self.btnJaune.SetBackgroundColour('yellow')
        
        # volume
        lblVolume = wx.StaticText(self, -1, u"Volume du local en m3 :")
        self.volume = wx.SpinCtrl(self, -1, "")
        self.volume.SetRange(10,500)
        self.volume.SetValue(100)
        
        taille1 = self.volume.GetSizeTuple()
        # HSP :
        lblHsp = wx.StaticText(self, -1, u"Hauteur sous plafond\n(en m) :")
        choixHsp = [u'< 5m', u'5m', u'6m', u'8m', u'10m']
        self.hsp = wx.Choice(self, -1, choices=choixHsp, size=taille1)
        self.hsp.SetSelection(0)
        
        # NB Personnes :
        lblNbPersonnes = wx.StaticText(self,-1, u'Nombre de personnes\noccupant le local :')
        self.personnes = wx.SpinCtrl(self, -1, "", size=taille1)
        self.personnes.SetRange(0,99)
        self.personnes.SetValue(10)
        
        # type de local
        lblLocal = wx.StaticText(self, -1, u"Type de local :")
        loc = [u"Bureaux", u"Ateliers, entrepôts, magasins..."]
        self.local = wx.Choice(self, -1, choices=loc, size=taille1)
        self.local.SetSelection(1)
        
        taille2 = taille1
        # environnement :
        lblEnvironnement = wx.StaticText(self, -1, u"Environnement du local :")
        choixEnv = [u"Murs extérieurs bien exposés : Murs intérieurs entourés de locaux chauffés.", 
                    u'1 mur extérieur mal exposé : Murs intérieurs entourés de locaux chauffés.', 
                    u'2 ou 3 murs extérieurs mal exposés : Murs intérieurs entourés de locaux peu ou pas chauffés.']
        self.environnement = wx.Choice(self, -1, choices=choixEnv, size = taille2)
        self.environnement.SetSelection(0)
        
        # construction :
        lblConstruction = wx.StaticText(self, -1, u'Construction du local :')
        choixConstr = [u'Murs épais (25cm).',
                       u'Construction légère : ossature béton, grands vitrages...',
                       u'Construction très légère : portes fréquemment ouvertes']
        self.construction = wx.Choice(self, -1, choices=choixConstr, size = taille2)
        self.construction.SetSelection(1)
        
        # altitude :
        lblAltitude = wx.StaticText(self, -1, u"Altitude du local :")
        choixAltitude = [u'< 200m', u'200 à 500m', u'500 à 1000m', u'1000 à 1500m', u'1500 à 2000m']
        self.altitude = wx.Choice(self, -1, choices=choixAltitude)
        self.altitude.SetSelection(0)
        
        # bouton calcul
        self.btnCalcul = wx.Button(self, -1, "Calculer")
        self.btnCalcul.Enable(False)
        self.btnCalcul.SetDefault()
        if self.parent.licence == 0:
            self.btnCalcul.Enable(False)
        
        # séparation
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        
        # résultat :
        lblresultat = wx.StaticText(self, -1, u"Puissance estimée :")
        self.resultat = wx.StaticText(self, -1, u"... W")
        self.resultat.SetForegroundColour('blue')
        self.resultat.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        
        #----------------- Binds -------------------------------------
        
        self.Bind(wx.EVT_BUTTON, self.onCalcul, self.btnCalcul)
        self.Bind(wx.EVT_BUTTON, self.onZone, id=100)
        self.Bind(wx.EVT_BUTTON, self.onZone, id=101)
        self.Bind(wx.EVT_BUTTON, self.onZone, id=102)
        self.Bind(wx.EVT_BUTTON, self.onZone, id=103)
        self.Bind(wx.EVT_SPINCTRL, self.onRaz)
        self.Bind(wx.EVT_CHOICE, self.onRaz)
        
        #-------------- Ajout des wigets au sizer --------------------
        
        self.gbs.Add(self.carte, (0,0), span=(7,1))
        self.gbs.Add(lblChoixZone, (0,1), (1,4))
        self.gbs.Add(self.btnRouge, (1,1))
        self.gbs.Add(self.btnVert, (1,2))
        self.gbs.Add(self.btnBleu, (1,3))
        self.gbs.Add(self.btnJaune, (1,4))
        
        self.gbs.Add(lblVolume,(3,1), (1,4))
        self.gbs.Add(self.volume, (3,5))
        
        self.gbs.Add(lblHsp, (4,1), (1,4))
        self.gbs.Add(self.hsp, (4,5))
        
        self.gbs.Add(lblNbPersonnes, (5,1), (1,4))
        self.gbs.Add(self.personnes, (5,5))
        
        self.gbs.Add(lblLocal, (6,1), (1,4))
        self.gbs.Add(self.local, (6,5))
        
        self.gbs.Add(lblEnvironnement, (7,0))
        self.gbs.Add(self.environnement, (7,1), (1,5), wx.EXPAND)
        
        self.gbs.Add(lblConstruction, (8,0))
        self.gbs.Add(self.construction, (8,1), (1,5), wx.EXPAND)
        
        self.gbs.Add(lblAltitude, (9,0))
        self.gbs.Add(self.altitude, (9,1), (1,5), wx.EXPAND)
        
        
        self.gbs.Add(self.btnCalcul, (10,0))
        
        self.gbs.Add(sep, (11,0), (1,6), wx.EXPAND)
        
        self.gbs.Add(lblresultat, (12,0))
        self.gbs.Add(self.resultat, (12,1), (1,5), wx.EXPAND)
        
        self.SetSizerAndFit(self.gbs)

        #----------- variables de calcul ----------------------
        
        self.zone = 1.0
        
    def onZone(self, evt):
        if evt.GetId()== 100: # rouge
            self.zone = 0.8
            self.btnCalcul.SetBackgroundColour('red')
        if evt.GetId()== 101: # bleu
            self.zone = 1.3
            self.btnCalcul.SetBackgroundColour('blue')
        if evt.GetId()== 102: # vert
            self.zone = 1.0
            self.btnCalcul.SetBackgroundColour('green')
        if evt.GetId()== 103: # jaune
            self.zone = 1.6
            self.btnCalcul.SetBackgroundColour('yellow')
        if self.parent.licence == 0:
            self.btnCalcul.Enable(False)
        else :
            self.btnCalcul.Enable(True)
        self.resultat.SetLabel(u"... W")
        
    def onRaz(self, evt) :
        self.resultat.SetLabel(u"... W")
            

    def onCalcul(self, evt):
        
        # Volume de la pièce :
        vol = self.volume.GetValue()
        
        # Nombre de personnes occupant la pièce
        nbPers = self.personnes.GetValue()
        
        # Détermination du coef Kg en fonction de la zone géographique
        Kg = self.zone
        
        # Détermination du coef Kc en fonction de l'environnement et du type de construction
        if self.environnement.GetSelection() == 0 :
            if self.construction.GetSelection() == 0 :
                Kc = 1.0
            elif self.construction.GetSelection() == 1 :
                Kc = 1.1
            else :
                Kc = 1.2
        elif self.environnement.GetSelection() == 1 :
            if self.construction.GetSelection() == 0 :
                Kc = 1.1
            elif self.construction.GetSelection() == 1 :
                Kc = 1.2
            else :
                Kc = 1.3
        else :
            if self.construction.GetSelection() == 0 :
                Kc = 1.2
            elif self.construction.GetSelection() == 1 :
                Kc = 1.3
            else :
                Kc = 1.4
        
        # Coef Ka de majoration pour l'altitude
        if self.altitude.GetSelection() == 0 :
            Ka = 1
        elif self.altitude.GetSelection() ==1 :
            Ka = 1.1
        elif self.altitude.GetSelection() ==2 :
            Ka = 1.2
        elif self.altitude.GetSelection() == 3 :
            Ka = 1.3
        else :
            Ka = 1.45
        
        # Coef Kh de majoration pour grande hauteur sous plafond
        if self.hsp.GetSelection() == 0 :
            Kh = 1
        elif self.hsp.GetSelection() == 1 :
            Kh = 1.03
        elif self.hsp.GetSelection() == 2 :
            Kh = 1.06
        elif self.hsp.GetSelection() == 3 :
            Kh = 1.12
        else :
            Kh = 1.18
        
        # Calcul en fonction du type de local :
        if self.local.GetSelection() == 0 :
            # si bureaux :
            K = 0.025
        else :
            # si atelier
            K = 0.050
        
        # Puissance calculée
        P = round(((K*vol*Kg*Kc)-0.2*nbPers)*Ka*Kh, 1)
        self.resultat.SetLabel("%s kW" %P)



class OngletBilanClim(wx.Panel):
    """bilan de climatisation"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        
        ############## création du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        
        
        #------------- création des widgets ---------------------
        fontTitre = (wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # occupants, travail et air        
        lblApportInterne = wx.StaticText(self, -1, u'APPORTS INTERNES')
        lblApportInterne.SetFont(fontTitre)
        lblNbOccupants = wx.StaticText(self, -1, u"Nombre d'occupants")
        self.nbOccupants = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.nbOccupants.SetToolTipString(u"Nombre de personnes occupant le local")
        lstTypetravail = [u"Repos", u"Bureau", u"Physique"]
        self.typeTravail = wx.Choice(self, -1, choices=lstTypetravail)
        self.typeTravail.SetSelection(1)
        self.typeTravail.SetToolTipString(u"Type d'activité effectuée dans le local")
        lstFumeur = [u"Fumeur", u"Non fumeur"]
        self.fumeur = wx.Choice(self, -1, choices=lstFumeur)
        self.fumeur.SetSelection(1)
        self.fumeur.SetToolTipString(u"Local fumeur ou non fumeur ?")
        # eclairage
        lblEclairage = wx.StaticText(self, -1, u"Éclairage :")
        self.eclairage = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.eclairage.SetToolTipString(u"Puissance d'éclairage installée (en Watts)")
        # matériel bureau
        lblbureautique = wx.StaticText(self, -1, u"Matériel bureautique :")
        self.bureautique = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.bureautique.SetToolTipString(u"Puissance en Watts du matériel de bureautique installé dans le local.\n"
                                          u"Par ex : ordinateur, fax, photocopieuse...")
        dureeUtilisation = ['15min', '30min', '45min', '1h', '1h15min', '1h30min', '1h45min', '2h', '2h30min', '3h', '3h30min' ,'4h']
        self.dureeUtilMatBureau = wx.Choice(self, -1, choices=dureeUtilisation)
        self.dureeUtilMatBureau.SetSelection(3)
        self.dureeUtilMatBureau.SetToolTipString(u"Durée d'utilisation aux heures les plus chaudes de la journée")
        # matériel chaud
        lblMaterielChaud = wx.StaticText(self, -1, u'Appareils "chauds" :')
        self.materielChaud = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.materielChaud.SetToolTipString(u"Puissance en Watts des appareils à forte émission de chaleur.\n"
                                          u"Par ex : four, moteur...")
        self.dureeUtilMatChaud = wx.Choice(self, -1, choices=dureeUtilisation)
        self.dureeUtilMatChaud.SetSelection(3)
        self.dureeUtilMatChaud.SetToolTipString(u"Durée d'utilisation aux heures les plus chaudes de la journée")
        # matériel froid
        lblMaterielFroid = wx.StaticText(self, -1, u'Appareils "froids" :')
        self.materielFroid = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.materielFroid.SetToolTipString(u"Puissance en Watts des appareils produisant du froid.\n"
                                          u"Par ex : réfrigérateur, congélateur...")
        self.dureeUtilMatFroid = wx.Choice(self, -1, choices=dureeUtilisation)
        self.dureeUtilMatFroid.SetSelection(3)
        self.dureeUtilMatFroid.SetToolTipString(u"Durée d'utilisation aux heures les plus chaudes de la journée")
        
        # surfaces vitrées
        lblSurfacesVitrees = wx.StaticText(self, -1, u"SURFACES VITRÉES")
        lblSurfacesVitrees.SetFont(fontTitre)
        lblSurfaceVitreeTotale = wx.StaticText(self, -1, u'Total des surfaces vitrées :')
        self.surfaceVitreeTotale = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.surfaceVitreeTotale.SetToolTipString(u"Surface en m² de l'ensemble des surfaces vitrées de la pièce")
        lblSurfaceVitreeExposee = wx.StaticText(self, -1, u'Surface vitrée la plus exposée :')
        self.surfaceVitreeExposee = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.surfaceVitreeExposee.SetToolTipString(u"Surface en m² de la surface vitrée la plus exposée.")
        lstOrientation = ["Horizontal", "Ouest", "Sud-Ouest", "Sud-Est", "Sud", "Est", "Nord-Ouest", "Nord-Est"]
        self.orientation = wx.Choice(self, -1, choices=lstOrientation)
        self.orientation.SetSelection(1)
        self.orientation.SetToolTipString(u"Orientation des surfaces vitrées les plus exposées.\n"
                                          u"Les expositions sont classées de la plus importante à la moins importante.")
        self.vitrage = wx.Choice(self, -1, choices=["Simple Vitrage", "Double vitrage"])
        self.vitrage.SetSelection(1)
        self.vitrage.SetToolTipString(u"Type de vitrage installé")
        self.store = wx.Choice(self, -1, choices=[u"Extérieur", u"Intérieur", u"Sans"])
        self.store.SetSelection(0)
        self.store.SetToolTipString(u"Possibilité d'occultation des surfaces vitrées :\n"
                                    u"- extérieur : ex=volets\n"
                                    u"- intérieur : ex=stores\n"
                                    u"-sans : pas de possibilité d'occultation")
        
        # plancher/plafond
        lblHorizontal = wx.StaticText(self, -1, u"SURFACES HORIZONTALES")
        lblHorizontal.SetFont(fontTitre)
        lblPlancher = wx.StaticText(self, -1, u"Plancher \n(si au dessus d'un local)")
        self.plancher = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.plancher.SetToolTipString(u"Surface en m² du plancher de la pièce si celui-ci est situé AU DESSUS D'UN LOCAL")
        lblPlafond = wx.StaticText(self, -1, u"Plafond :")
        self.plafond = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.plafond.SetToolTipString(u"Surface en m² du plafond de la pièce")
        lstPlafond = [u"Sous un local", u"sous terrasse non isolée", u"sous terrasse isolée", u"sous combles ventilés non isolés", u"sous combles ventilés isolés"]
        self.typePlafond = wx.Choice(self, -1, choices=lstPlafond)
        self.typePlafond.SetSelection(4)
        self.typePlafond.SetToolTipString(u"Type d'isolation du plafond")
        lstEpaisseurisolant = ["8cm", "9cm", "10cm", "11cm", "12cm", "13cm", "14cm", "15cm", "16cm", "17cm", "18cm", "19cm", "20cm", "21cm", "22cm", "23cm", "24cm"]
        self.epaisseurIsolationPlafond = wx.Choice(self, -1, choices=lstEpaisseurisolant)
        self.epaisseurIsolationPlafond.SetSelection(12)
        self.epaisseurIsolationPlafond.SetToolTipString(u"Épaisseur en cm de l'isolant")
        
        # Murs et cloisons
        lblVertical = wx.StaticText(self, -1, u"MURS ET CLOISONS")
        lblVertical.SetFont(fontTitre)
        lstMur = ["1cm", "2cm", "3cm", "4cm", "5cm", "6cm", "7cm", "8cm", "10cm"]
        lblMurOmbre = wx.StaticText(self, -1, u"Murs à l'ombre")
        self.murOmbre = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.epaisseurIsolationMurOmbre = wx.Choice(self, -1, choices=lstMur)
        self.epaisseurIsolationMurOmbre.SetToolTipString(u"Épaisseur en cm de l'isolant des murs")
        self.epaisseurIsolationMurOmbre.SetSelection(8)
        self.murOmbre.SetToolTipString(u"Surface en m² des murs à l'ombre aux heures les plus chaudes de la journée")
        lblMurSoleil = wx.StaticText(self, -1, u"Murs au soleil")
        self.murSoleil = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.murSoleil.SetToolTipString(u"Surface en m² des murs exposés au soleil aux heures les plus chaudes de la journée")
        self.epaisseurIsolationMurSoleil = wx.Choice(self, -1, choices=lstMur)
        self.epaisseurIsolationMurSoleil.SetToolTipString(u"Épaisseur en cm de l'isolant des murs")
        self.epaisseurIsolationMurSoleil.SetSelection(8)
        lblCloison = wx.StaticText(self, -1, u"Cloisons")
        self.cloison = wx.TextCtrl(self, -1, "", validator=ValidDigitPoint())
        self.cloison.SetToolTipString(u"Surface en m² des cloisons du local")
        
        # bouton calcul
        self.btnCalcul = wx.Button(self, -1, 'Calculer')
        self.btnCalcul.SetBackgroundColour('yellow')
        self.btnCalcul.SetDefault()
        if self.parent.licence == 0:
            self.btnCalcul.Enable(False)
        
        # séparation
        sep = wx.BoxSizer(wx.VERTICAL)
        sep.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        
        # résultat :
        lblresultat = wx.StaticText(self, -1, u"Total des apports de chaleur :")
        lblresultat.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.resultat = wx.StaticText(self, -1, u"... W")
        self.resultat.SetForegroundColour('blue')
        self.resultat.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.resultat.SetForegroundColour('blue')
        
        #------------- binds -------------------------------------
        
        self.typePlafond.Bind(wx.EVT_CHOICE, self.onPlafond)
        self.btnCalcul.Bind(wx.EVT_BUTTON, self.onCalcul)
        
        
        #------------- Placement des widgets ---------------------
        
        self.gbs.Add(lblApportInterne, (0,1), (1,4))
        self.gbs.Add(lblNbOccupants, (1,0))
        self.gbs.Add(self.nbOccupants, (1,1))
        self.gbs.Add(self.typeTravail, (1,2))
        self.gbs.Add(self.fumeur, (1,3))
        self.gbs.Add(lblEclairage, (2,0))
        self.gbs.Add(self.eclairage, (2,1))
        self.gbs.Add(lblbureautique, (3,0))
        self.gbs.Add(self.bureautique, (3,1))
        self.gbs.Add(self.dureeUtilMatBureau, (3,2))
        self.gbs.Add(lblMaterielChaud, (4,0))
        self.gbs.Add(self.materielChaud, (4,1))
        self.gbs.Add(self.dureeUtilMatChaud, (4,2))
        self.gbs.Add(lblMaterielFroid, (5,0))
        self.gbs.Add(self.materielFroid, (5,1))
        self.gbs.Add(self.dureeUtilMatFroid, (5,2))
        
        self.gbs.Add(lblSurfacesVitrees, (6,1), (1,4))
        self.gbs.Add(lblSurfaceVitreeTotale, (7,0))
        self.gbs.Add(self.surfaceVitreeTotale, (7,1))
        self.gbs.Add(lblSurfaceVitreeExposee, (8,0))
        self.gbs.Add(self.surfaceVitreeExposee, (8,1))
        self.gbs.Add(self.orientation, (8,2))
        self.gbs.Add(self.vitrage, (8,3))
        self.gbs.Add(self.store, (8,4))
        
        self.gbs.Add(lblHorizontal, (9,1), (1,4))
        self.gbs.Add(lblPlancher, (10,0))
        self.gbs.Add(self.plancher, (10,1))
        self.gbs.Add(lblPlafond, (11,0))
        self.gbs.Add(self.plafond, (11,1))
        self.gbs.Add(self.typePlafond, (11,2), (1,2))
        self.gbs.Add(self.epaisseurIsolationPlafond, (11,4))
        
        self.gbs.Add(lblVertical, (12,1), (1,4))
        self.gbs.Add(lblMurOmbre, (13,0))
        self.gbs.Add(self.murOmbre, (13,1))
        self.gbs.Add(self.epaisseurIsolationMurOmbre, (13,2))
        self.gbs.Add(lblMurSoleil, (14,0))
        self.gbs.Add(self.murSoleil, (14,1))
        self.gbs.Add(self.epaisseurIsolationMurSoleil, (14,2))
        self.gbs.Add(lblCloison, (15,0))
        self.gbs.Add(self.cloison, (15,1))
        
        self.gbs.Add(self.btnCalcul, (16,0))
        
        self.gbs.Add(sep, (17,0), (1,6), wx.EXPAND)
        
        self.gbs.Add(lblresultat, (18,0))
        self.gbs.Add(self.resultat, (18,1), (1,5), wx.EXPAND)
        
        self.SetSizerAndFit(self.gbs)
        
        
        
        
    def onPlafond(self, evt):
        if self.typePlafond.GetSelection() == 2 :
            lstEpaisseurisolant = ["1cm", "2cm", "3cm", "4cm", "5cm", "6cm", "7cm", "8cm"]
            self.epaisseurIsolationPlafond.SetItems(lstEpaisseurisolant)
            self.epaisseurIsolationPlafond.SetSelection(7)
            self.epaisseurIsolationPlafond.Enable(True)
        elif self.typePlafond.GetSelection() == 4 :
            lstEpaisseurisolant = ["8cm", "9cm", "10cm", "11cm", "12cm", "13cm", "14cm", "15cm", "16cm", "17cm", "18cm", "19cm", "20cm", "21cm", "22cm", "23cm", "24cm"]
            self.epaisseurIsolationPlafond.SetItems(lstEpaisseurisolant)
            self.epaisseurIsolationPlafond.SetSelection(12)
            self.epaisseurIsolationPlafond.Enable(True)
        else :
            self.epaisseurIsolationPlafond.Enable(False)
            
    def onCalcul(self, evt):
        # nombre d'occupants -> nbOccup = entier
        try :
            nbOccup = int(float(self.nbOccupants.GetValue()))
            self.nbOccupants.SetBackgroundColour(None)
            self.nbOccupants.SetValue('%s'%nbOccup)
        except :
            nbOccup = 0
            self.nbOccupants.SetValue('0')
            self.nbOccupants.SetBackgroundColour('pink')
        
        # type d'activité --> Kactivite = float
        activite = self.typeTravail.GetSelection()
        lstKactivite = [0.8, 1., 1.2]
        Kactivite = lstKactivite[activite]
        
        # local fumeur --> Kair = float
        air = self.fumeur.GetSelection()
        lstKair = [1.3, 1.]
        Kair = lstKair[air]
        
        # éclairage --> Keclairage = float
        try :
            eclairage = int(float(self.eclairage.GetValue()))
            self.eclairage.SetBackgroundColour(None)
            self.eclairage.SetValue('%s'%eclairage)
        except :
            eclairage = 0
            self.eclairage.SetValue('0')
            self.eclairage.SetBackgroundColour('pink')
        
        # matériel bureautique
        try :
            bureautique = int(float(self.bureautique.GetValue()))
            self.bureautique.SetBackgroundColour(None)
            self.bureautique.SetValue('%s' %bureautique)
        except :
            bureautique = 0
            self.bureautique.SetValue('0')
            self.bureautique.SetBackgroundColour('pink')
        lstDureeUtilisation = [0.25, 0.5, 0.75, 1., 1.25, 1.5, 1.75, 2., 2.5, 3., 3.5, 4.]
        dureeBureau = lstDureeUtilisation[self.dureeUtilMatBureau.GetSelection()]
        
        # appareils "chauds"
        try :
            materielChaud = int(float(self.materielChaud.GetValue()))
            self.materielChaud.SetBackgroundColour(None)
            self.materielChaud.SetValue('%s' %materielChaud)
        except :
            materielChaud = 0
            self.materielChaud.SetValue('0')
            self.materielChaud.SetBackgroundColour('pink')
        dureeChaud = lstDureeUtilisation[self.dureeUtilMatChaud.GetSelection()]
        
        # appareils "froids"
        try :
            materielFroid = int(float(self.materielFroid.GetValue()))
            self.materielFroid.SetBackgroundColour(None)
            self.materielFroid.SetValue('%s' %materielFroid)
        except :
            materielFroid = 0
            self.materielFroid.SetValue('0')
            self.materielFroid.SetBackgroundColour('pink')
        dureeFroid = lstDureeUtilisation[self.dureeUtilMatFroid.GetSelection()]
        
        #------------------------- calcul du coef KapportsInternes
        KapportsInternes = int((nbOccup*Kactivite*130)+eclairage+(Kair*nbOccup*51)+(bureautique*dureeBureau)+(materielChaud*dureeChaud)+(materielFroid*dureeFroid))
        
        # surfaces vitrées
        try:
            surfaceVitreeTotale = round(float(self.surfaceVitreeTotale.GetValue()), 1)
            self.surfaceVitreeTotale.SetBackgroundColour(None)
            self.surfaceVitreeTotale.SetValue('%s' %surfaceVitreeTotale)
        except:
            surfaceVitreeTotale = 0
            self.surfaceVitreeTotale.SetValue('0')
            self.surfaceVitreeTotale.SetBackgroundColour('pink')
            
        # surface vitrée la plus exposée
        try:
            surfaceVitreeExposee = round(float(self.surfaceVitreeExposee.GetValue()), 1)
            self.surfaceVitreeExposee.SetBackgroundColour(None)
            self.surfaceVitreeExposee.SetValue('%s' %surfaceVitreeExposee)
        except:
            surfaceVitreeExposee = 0
            self.surfaceVitreeExposee.SetBackgroundColour('pink')
            self.surfaceVitreeExposee.SetValue('0')
        lstKorientation = [508., 355., 312., 295., 219., 202., 185., 39.]
        orientation = lstKorientation[self.orientation.GetSelection()]
        lstKvitrage = [1.18, 1.]
        vitrage = lstKvitrage[self.vitrage.GetSelection()]
        lstKstore = [0.25, 0.5, 1.]
        store = lstKstore[self.store.GetSelection()]
        
        #----------------------------------- calcul Kvitres
        Kvitres = int((surfaceVitreeTotale*28)+(surfaceVitreeExposee*orientation*vitrage*store))
        
        # surface horizontales (plancher/plafond)
        try:
            surfacePlancher = round(float(self.plancher.GetValue()), 1)
            self.plancher.SetBackgroundColour(None)
            self.plancher.SetValue('%s' %surfacePlancher)
        except:
            surfacePlancher = 0
            self.plancher.SetBackgroundColour('pink')
            self.plancher.SetValue('0')
        
        try:
            surfacePlafond = round(float(self.plafond.GetValue()), 1)
            self.plafond.SetBackgroundColour(None)
            self.plafond.SetValue('%s' %surfacePlafond)
        except:
            surfacePlafond = 0
            self.plafond.SetBackgroundColour('pink')
            self.plafond.SetValue('0')
        lstKplafond = [12., 40., 14., 40., 4.]
        typePlafond = lstKplafond[self.typePlafond.GetSelection()]
        
        if self.epaisseurIsolationPlafond.Enabled == True :
            if self.typePlafond.GetSelection() == 4:
                lstKisolationPlafond = [1.9, 1.7, 1.5, 1.4, 1.3, 1.2, 1.1, 1.05, 1., 0.9, 0.85, 0.82, 0.8, 0.78, 0.75, 0.72, 0.7]
                isolationplafond = lstKisolationPlafond[self.epaisseurIsolationPlafond.GetSelection()]
            else :
                lstKisolationPlafond = [2., 1.6, 1.25, 1., 0.85, 0.7, 0.6, 0.5]
                isolationplafond = lstKisolationPlafond[self.epaisseurIsolationPlafond.GetSelection()]
        else :
            isolationplafond = 1
        
        #----------------------------------  calcul Khorizontal
        Khorizontal = int((surfacePlancher*12.)+(surfacePlafond*typePlafond*isolationplafond))
        
        # surfaces verticales
        try:
            surfaceMurOmbre = round(float(self.murOmbre.GetValue()), 1)
            self.murOmbre.SetBackgroundColour(None)
            self.murOmbre.SetValue('%s' %surfaceMurOmbre)
        except:
            surfaceMurOmbre = 0
            self.murOmbre.SetBackgroundColour('pink')
            self.murOmbre.SetValue('%s' %surfaceMurOmbre)
        lstKmur = [1.3, 1., 0.8, 0.65, 0.55, 0.5, 0.45, 0.4, 0.35]
        isolationMurOmbre = lstKmur[self.epaisseurIsolationMurOmbre.GetSelection()]
        
        try:
            surfaceMurSoleil = round(float(self.murSoleil.GetValue()), 1)
            self.murSoleil.SetBackgroundColour(None)
            self.murSoleil.SetValue('%s' %surfaceMurSoleil)
        except:
            surfaceMurSoleil = 0
            self.murSoleil.SetBackgroundColour('pink')
            self.murSoleil.SetValue('%s' %surfaceMurSoleil)
        isolationMurSoleil = lstKmur[self.epaisseurIsolationMurSoleil.GetSelection()]
        
        try:
            surfaceCloison = round(float(self.cloison.GetValue()), 1)
            self.cloison.SetBackgroundColour(None)
            self.cloison.SetValue('%s' %surfaceCloison)
        except:
            surfaceCloison = 0
            self.cloison.SetBackgroundColour('pink')
            self.cloison.SetValue('%s' %surfaceCloison)
        
        #---------------------- calcul de Kvertical
        Kvertical = (surfaceMurOmbre*isolationMurOmbre*8)+(surfaceCloison*isolationMurSoleil*12)+surfaceCloison*16

        # Total des apports :
        apports = int(KapportsInternes+Kvitres+Kvertical+Khorizontal)
        self.resultat.SetLabel('%s W'%apports)
        
        
        
        
        
        
        
        
        
        
        
        
        
class Climatic(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=u"Bilans thermiques %s"%version, 
                          style=wx.DEFAULT_FRAME_STYLE 
                          ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent = parent
        
        ################### pour windows ###################
        self.licence = self.parent.licence_ok
        ####################################################
        
        # Ajout d'une barre d'état
        self.statusText = "Chauffage de locaux d'habitation"
        self.CreateStatusBar()
        self.SetStatusText(self.statusText)    
        
        # Création d'un panel pour y placer les Widgets
        panel = wx.Panel(self)
        
        # Création d'un sizer pour organiser les widgets
        sizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        # Ajout du notebook au panel
        self.nb = wx.Notebook(panel)#, size=(500,500))
        ##### pour windows ###########
        self.nb.licence = self.licence
        ##############################
        
        # Création des onglets
        self.page1 = OngletChauffDomestique(self.nb)
        self.page2 = OngletChauffIndus(self.nb)
        self.page3 = OngletBilanClim(self.nb)

        
        # Ajout des onglets au notebook
        self.nb.AddPage(self.page1, "Chauffage habitation")
        self.nb.AddPage(self.page2, u"Chauffage tertiaire")
        self.nb.AddPage(self.page3, u'Climatisation')

        # définition de l'onglet par défaut
        self.nb.ChangeSelection(2)
        
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
            self.SetStatusText(self.statusText)
        elif numOnglet == 1 :
            self.SetStatusText(u"Chauffage de locaux tertiaires ou industriels < 500m3")
        #elif numOnglet == 2 :
            #self.SetStatusText(u"Calcul de la hauteur et de la focale en fonction de la largeur à visualiser")
        else :
            self.SetStatusText(u"Bilan thermique de climatisation")
        
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.parent.btnChauff.Enable(True)
        self.parent.menuModuleChauffage.Enable(True)
        self.Destroy()
