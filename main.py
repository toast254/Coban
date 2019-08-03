#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - lanceur principal
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


Version = "1.2.0"


############################################################################
##                                                                        ##
##           LANCEUR PRINCIPAL DU LOGICIEL COBAN                          ##
##                                                                        ##
############################################################################

try :
    import wx
except :
    print u"Coban n�cessite l'installation de wxPython pour fonctionner"
    raw_input()

from modcoban import icone, testFich, fichierConf
import os, sys, pickle


# ------------ D�marrage ----------------------#
    
# teste si le dossier .coban de l'utilisateur existe, sinon le cr�e
dossierParDef = os.path.join(os.path.expanduser("~"),'.coban')
if os.path.exists(dossierParDef) == False:
    os.mkdir(dossierParDef)

#-----------------------------------------------------------------------------------

def changeDir():
    """ conversion du r�pertoire courant en r�pertoire de travail """
    chemin = os.getcwd()
    os.chdir(chemin)

#--------------------------------------------------------------------------------------

def TestLicence():
    """ teste si la licence est activ�e 
    (uniquement pour la version "ex�cutable" pour Windows(R)).\n
    --> retourne 1 si licence OK, 0 sinon."""
    
    return 1
    

#--------------------------------------------------------------------------------------

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

#---------------------------------------------------------------------------

class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        bmp = wx.Image(opj("images/coban_maj.png")).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp,
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 3000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(2000, self.ShowMain)


    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()
        
        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
##        frame = wxPythonDemo(None, "wxPython: (A Demonstration)")
##        frame.Show()
        if self.fc.IsRunning():
            self.Raise()




#---------------------------------------------------------------------------

class Coban(wx.App):
    """Application principale"""
    def OnInit(self):
        # cr�ation de la fen�tre principale
        frame = Principale("Coban")         
        # insertion de l'icone de l'application 
        icone(frame)
        frame.Show(True)
        self.SetTopWindow(frame)
        changeDir()
        return True


#--------------------------------------------------------------------------------------


class Principale(wx.Frame):
    """Lanceur principal des diff�rents modules"""
    def __init__(self, titre):
        wx.Frame.__init__(self, None, -1, title = titre,
                      style=wx.DEFAULT_FRAME_STYLE 
                      ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        # teste si le chemin par d�faut du fichier de configuration existe
        try :
            f = open(fichierConf, 'r')
            self.cheminParDef = pickle.load(f)
            self.Maj = pickle.load(f)
            f.close()
        except :
            try :
                self.cheminParDef = os.path.join(os.path.expanduser('~'), '.coban')
                self.Maj = 1
                f = open(fichierConf, 'w')
                pickle.dump(self.cheminParDef, f)
                pickle.dump(self.Maj, f)
                f.close()
                
            except :
                wx.MessageBox(u"Vous n'avez pas les droits n�cessaires pour �crire dans le dossier :\n%s\n\n"
                              u"Certains modules ne fonctionneront pas\n\n"
                              u"Contactez votre administrateur syst�me pour vous donner les droits n�cessaires, "
                              u"ou modifiez manuellement le fichier :\n%s\n\n"
                              u"(consultez l'aide de Coban ou le site\n"
                              u"http://sg-logiciels.fr pour plus d'informations)." %(os.getcwd(), os.path.join(os.getcwd(), fichierConf)),
                              u'Erreur !',
                              wx.ICON_WARNING)
                self.cheminParDef = os.path.join(os.path.expanduser('~'), '.coban')
                
        #------------- teste la licence au d�marrage -------------#
        #-------------- (pour windows uniquement) ----------------#
        self.licence_ok = TestLicence()
        #---------------------------------------------------------#
        
        
        ############## Cr�ation du panel #########################
        
        panel =  wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        ############## cr�ation du sizer principal ###############
        
        self.gbs = wx.GridBagSizer(hgap=5, vgap=5)
        
        ############## Cr�ation de statusbar #####################
        
        self.CreateStatusBar()
        self.SetStatusText("Consultez l'aide pour plus d'infos sur les modules")
        
        ################# CR�ATION DES MENUS #######################
        
        barreMenu = wx.MenuBar()
        
        # Menu des modules
        self.menuModule = wx.Menu()
        
        # sous-menu "�lectricit�" ---------------------------------------------------------------------
        self.sousMenuCalcul = wx.Menu()
        # module section
        self.menuModuleSection = self.sousMenuCalcul.Append(wx.ID_ANY, u"Section de c�ble", 
                                              u"Calcul de section de c�ble")
        self.Bind(wx.EVT_MENU, self.onSection, self.menuModuleSection)
        # module chute
        self.menuModuleChute = self.sousMenuCalcul.Append(wx.ID_ANY, u"Chutes de tension", 
                                              u"Calcul de chute de tension")
        self.Bind(wx.EVT_MENU, self.onChute, self.menuModuleChute)
        
        self.menuModule.AppendMenu(-1, u"�lectricit�", self.sousMenuCalcul)
        self.menuModule.AppendSeparator()
        
        # sous-menu "Conversions" ---------------------------------------------------------------------
        self.sousMenuConv = wx.Menu()
        # module conversion
        self.menuModuleConversion = self.sousMenuConv.Append(wx.ID_ANY, u"Conversions W/A/CV/HP", 
                                                 u"Conversions Watts / Amp�res / Chevaux / Horse Power")
        self.Bind(wx.EVT_MENU, self.onConversion, self.menuModuleConversion)
        # module AWG
        self.menuModuleConvAwg = self.sousMenuConv.Append(wx.ID_ANY, u"Conversion AWG", 
                                                 u"Conversion de l'AWG vers mm2")
        self.Bind(wx.EVT_MENU, self.onConvAwg, self.menuModuleConvAwg)

        self.menuModule.AppendMenu(-1, u"Conversions", self.sousMenuConv)
        self.menuModule.AppendSeparator()
        
        # sous-menu "Sono-Vid�o" ---------------------------------------------------------------------------
        self.sousMenuSonoVideo = wx.Menu()
        # module Vid�o
        self.menuModuleVideo = self.sousMenuSonoVideo.Append(wx.ID_ANY, u"Calculs de champs de vision",
                                                      u"Calculs de champs de vision en fonction de focales et de distances")
        self.Bind(wx.EVT_MENU, self.onVideo, self.menuModuleVideo)
        # module sono
        self.menuModuleSono = self.sousMenuSonoVideo.Append(wx.ID_ANY, u"HP et puissances",
                                                      u"Calculs du nombre de HP et de la puissance n�cessaire")
        self.Bind(wx.EVT_MENU, self.onSono, self.menuModuleSono)
        
        self.menuModule.AppendMenu(-1, u"Sono / Vid�o", self.sousMenuSonoVideo)
        self.menuModule.AppendSeparator()
        
        # sous-menu "Climatic" -------------------------------------------------------------------------------------
        self.sousMenuClimatic = wx.Menu()
        # module climatic
        self.menuModuleChauffage = self.sousMenuClimatic.Append(wx.ID_ANY, u'Bilans thermiques',
                                                          u"Calculer la puissance n�cessaire pour chauffer ou climatiser une pi�ce.")
        self.Bind(wx.EVT_MENU, self.onClimatic, self.menuModuleChauffage)
        
        self.menuModule.AppendMenu(-1, u"Chauffage/Climatisation", self.sousMenuClimatic)
        self.menuModule.AppendSeparator()
        
        # sous-menu "�clairage" ------------------------------------------------------------------------------------
        self.sousMenuEclairage = wx.Menu()
        # module �clairage
        self.menuModuleEcl = self.sousMenuEclairage.Append(wx.ID_ANY, u"�clairage int�rieur",
                                                           u"Calculer de nombre d'appareils d'�clairage n�cessaires\n"
                                                           u"en fonction du niveau d'�clairement souhait�")
        self.Bind(wx.EVT_MENU, self.onEclairage, self.menuModuleEcl)
        
        self.menuModule.AppendMenu(-1, u"�clairage", self.sousMenuEclairage)
        self.menuModule.AppendSeparator()
        
        # menu quitter ----------------------------------------------------------------------------------------------
        self.menuModuleQuitter = self.menuModule.Append(wx.ID_EXIT, "Quitter", "Quitter l'application...")
        self.Bind(wx.EVT_MENU, self.onQuitter, self.menuModuleQuitter)
        
        # Menu Aide --------------------------------------------------------------------------------------------
        
        menuAide = wx.Menu()
        
        # sous-menu "aide"
        menuAideAide = menuAide.Append(wx.ID_HELP,'Aide', u"Aide sur le logiciel")
        self.Bind(wx.EVT_MENU, self.onAide, menuAideAide)

        # sous-menu "Pr�f�rences" 
        self.menuPreferences = wx.Menu()
        # dossier de sauvegarde
        self.menuPreferencesSauvegarde = self.menuPreferences.Append(-1, u"R�pertoire de sauvegarde", u"Choix du r�pertoire de sauvegarde")
        self.Bind(wx.EVT_MENU, self.onPreferencesSauvegarde, self.menuPreferencesSauvegarde)        
        # Mises � jour auto
        self.menuMaJauto = self.menuPreferences.Append(-1, u"Pr�venir des mise � jour", u"Pr�venir des mise � jour automatiquement", wx.ITEM_CHECK)
        self.menuMaJauto.Check(self.Maj)
        self.Bind(wx.EVT_MENU, self.onMaJ, self.menuMaJauto)
        
        menuAide.AppendMenu(wx.ID_PREFERENCES, u"Pr�f�rences", self.menuPreferences)
        menuAide.AppendSeparator()
        
        ############################ Menu enregistrement de la licence ###############################
        ############################ pour la version Windows uniquement ##############################
        menuAideEnregistrer = menuAide.Append(wx.ID_APPLY, u'Enregistrement', u'Enregistrer Coban')
        self.Bind(wx.EVT_MENU, self.onEnregistrement, menuAideEnregistrer)
        menuAide.AppendSeparator()
        ##############################################################################################
        ##############################################################################################
        
        menuAideApropos = menuAide.Append(wx.ID_ABOUT,'A propos...', u"A propos de ce logiciel...")
        self.Bind(wx.EVT_MENU, self.onApropos, menuAideApropos)
                
        barreMenu.Append(self.menuModule, u"&Modules") 
        barreMenu.Append(menuAide, "&Aide")
        
        self.SetMenuBar(barreMenu)
        
      
        #--------------------- Cr�ation des widgets ----------------------------------
        # Taille des boutons
        colSize = (200,-1)
        
        # titres 
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        titreConversion = wx.StaticText(panel, -1, u'CONVERSIONS', size=colSize, style=wx.ALIGN_CENTRE)
        titreConversion.SetFont(font)
        titreCalcul = wx.StaticText(panel, -1, u"�LECTRICIT�", size=colSize, style=wx.ALIGN_CENTRE)
        titreCalcul.SetFont(font)
        titreSonoVideo = wx.StaticText(panel, -1, u"SONO - VID�O",size=colSize, style=wx.ALIGN_CENTER)
        titreSonoVideo.SetFont(font)
        titreClimatic = wx.StaticText(panel, -1, u"CHAUFFAGE / CLIM",size=colSize, style=wx.ALIGN_CENTRE)
        titreClimatic.SetFont(font)
        titreEclairage = wx.StaticText(panel, -1, u"�CLAIRAGE",size=colSize, style=wx.ALIGN_CENTRE)
        titreEclairage.SetFont(font)
        
        # bouton section de c�ble
        self.btnSection = wx.Button(panel, -1, u"Section de c�ble", size=colSize)
        self.btnSection.SetToolTipString(u"calcul de section de c�ble")
        self.Bind(wx.EVT_BUTTON, self.onSection, self.btnSection)
        
        # bouton chute de tension
        self.btnChute = wx.Button(panel, -1, u"Chute de tension", size=colSize)
        self.btnChute.SetToolTipString(u"calcul de chutes de tension")
        self.Bind(wx.EVT_BUTTON, self.onChute, self.btnChute)
        
        # bouton Conversions
        self.btnConv = wx.Button(panel, -1, "Conversions", size=colSize)
        self.btnConv.SetToolTipString(u"Convertir Watts en Amp�res, CV et HP...")
        self.Bind(wx.EVT_BUTTON, self.onConversion, self.btnConv)
        
        # bouton Conversion AWG
        self.btnConvAwg = wx.Button(panel, -1, "Conversion AWG", size=colSize)
        self.btnConvAwg.SetToolTipString("Convertir des AWG en mm")
        self.Bind(wx.EVT_BUTTON, self.onConvAwg, self.btnConvAwg)
        
        # bouton Vid�o
        self.btnVideo = wx.Button(panel, -1, "Champs de vision", size=colSize)
        self.btnVideo.SetToolTipString(u"Calculs de champs de vision en fonction de focales et de distances")
        self.Bind(wx.EVT_BUTTON, self.onVideo, self.btnVideo)
        
        # bouton Sono
        self.btnSono = wx.Button(panel, -1, "Sonorisation", size=colSize)
        self.btnSono.SetToolTipString(u"Calculs du nombre de HP et de la puissance n�cessaire")
        self.Bind(wx.EVT_BUTTON, self.onSono, self.btnSono)
        
        # bouton thermique 
        self.btnChauff = wx.Button(panel, -1, "Bilans", size=colSize)
        self.btnChauff.SetToolTipString(u"Bilans thermiques chaud/froid d'une pi�ce...")
        self.Bind(wx.EVT_BUTTON, self.onClimatic, self.btnChauff)
        
        
        # bouton Eclairage
        self.btnEcl = wx.Button(panel, -1, u"�clairage int�rieur", size=colSize)
        self.btnEcl.SetToolTipString(
            u"Estimer le nombre d'appareils d'�clairage n�cessaires\n"
            u"en fonction du niveau d'�clairement souhait�")
        self.Bind(wx.EVT_BUTTON, self.onEclairage, self.btnEcl)
        
        self.Bind(wx.EVT_CLOSE, self.onQuitter)
        
        ############### Ajout des wigets au sizer ####################
        
        self.gbs.Add(titreCalcul, (0,0))
        self.gbs.Add(self.btnSection, (1,0))
        self.gbs.Add(self.btnChute, (2,0))
        
        self.gbs.Add(titreConversion, (0,1))
        self.gbs.Add(self.btnConv, (1,1))
        self.gbs.Add(self.btnConvAwg, (2,1))
        
        self.gbs.Add(titreSonoVideo, (0,2))
        self.gbs.Add(self.btnVideo, (1,2))
        self.gbs.Add(self.btnSono, (2,2))
        
        self.gbs.Add(titreClimatic, (4,0))
        self.gbs.Add(self.btnChauff, (5,0))

        self.gbs.Add(titreEclairage, (4,1))
        self.gbs.Add(self.btnEcl, (5,1))
                
        panel.SetSizerAndFit(self.gbs)
        self.SetClientSize(panel.GetSize())
        
        self.Centre() # centre la fen�tre � l'ouverture sur l'�cran
        
        
        
        #---- v�rification des mises � jour (si actif) ----#
        if self.Maj == 1 :
            try :
                import urllib2
                #---- Affichage du spash -----#
                splash = MySplashScreen()
                splash.Show()
                
                def chargePage(url):
                    """charge l'url sp�cifi�e et renvoie la page"""
                    http = urllib2.urlopen(url)
                    content = http.read()
                    http.close()
                    return content
                
                urlbase= "http://www.sg-logiciels.fr/version_coban.txt"
                
                # charge le fichier coban.txt et extrait le num�ro de version et le changelog
                # (s�par�s par un ';' dans le fichier)
                buffer= chargePage(urlbase)
                version = u''
                changes = u''
                # cherche le ';' et �crit la version (version) et le changelog (changes)
                saut = 0
                try :
                    for char in buffer :
                        if char == ';' :
                            saut = 1
                        if saut == 0 :
                            version += char
                        if saut == 1 :
                            changes += char
                # si char accentu� dans le fichier coban.txt
                except :
                    changes += ' (...)'
                # enl�ve le ';' au d�but du changelog
                changes= changes[1:]
                if version != Version :
                    dlg = wx.MessageDialog(self, u'La version (%s) est disponible !'
                                           u'\n\nChangements : '
                                           u'\n%s'%(version,changes),
                                           'Nouvelle version !',wx.OK | wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()
            except :
                wx.MessageBox(u"Impossible de v�rifier les mises � jours !\n\n"
                              u"La recherche automatique de mise � jour\n"
                              u"sera d�sactiv�e au prochain d�marrage\n"
                              u"de Coban...\n"
                              u"(vous pouvez modifier ce param�tre dans le menu\n"
                              u"'Aide > Pr�f�rences'\n",
                              u'Erreur !',
                              wx.ICON_WARNING)
                self.Maj = 0
                f = open(fichierConf, 'w')
                pickle.dump(self.cheminParDef,f)
                pickle.dump(self.Maj, f)
                f.close()
            
    def onSection(self, evt):
        import section
        section.Section(self)

    def onChute(self, evt):
        import chute
        self.dlg = chute.ModuleChute(self)
        self.btnChute.Enable(False)
        self.menuModuleChute.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        

    def onConversion(self, evt):
        import conversion
        self.dlg = conversion.ModuleConv(self)
        self.btnConv.Enable(False)
        self.menuModuleConversion.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        
    def onConvAwg(self, evt):
        import convawg
        self.dlg = convawg.Awg(self)
        self.btnConvAwg.Enable(False)
        self.menuModuleConvAwg.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        
    def onVideo(self, evt):
        import video
        self.dlg = video.Video(self)
        self.btnVideo.Enable(False)
        self.menuModuleVideo.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        
    def onSono(self, evt):
        import sono
        self.dlg = sono.Sono(self)
        self.btnSono.Enable(False)
        self.menuModuleSono.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        
    def onClimatic(self, evt):
        import climatic
        self.dlg = climatic.Climatic(self)
        self.btnChauff.Enable(False)
        self.menuModuleChauffage.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        
        
    def onEclairage(self,evt):
        import eclairage
        self.dlg = eclairage.Eclairage(self)
        self.btnEcl.Enable(False)
        self.menuModuleEcl.Enable(False)
        icone(self.dlg)
        self.dlg.Show(True)
        
    def onMaJ(self, evt):
        """ �crit en 2�me position dans le fichier
        'config.cob' 0 ou 1 selon si la notification des M�J
        est active ou pas..."""
        if self.menuMaJauto.IsChecked() == False :
            self.Maj = 0
        else :
            self.Maj = 1
        f = open(fichierConf, 'w')
        pickle.dump(self.cheminParDef,f)
        pickle.dump(self.Maj, f)
        f.close()
    
        
    def onPreferencesSauvegarde(self, evt):
        dlg = wx.DirDialog(self, u"Choisissez un r�pertoire de sauvegarde :")
        
        if dlg.ShowModal() == wx.ID_OK:
            try :
                os.mkdir(os.path.join(dlg.GetPath(), '.coban'))
                f = open(fichierConf, 'w')
                pickle.dump(os.path.join(dlg.GetPath(), '.coban'), f)
                pickle.dump(self.Maj, f)
                f.close()
                wx.MessageBox(u'Vous avez choisi "%s" comme r�pertoire de sauvegarde.\n'
                              u'Le dossier ".coban" y est cr�e.'
                              u'\n\nCoban doit �tre relanc� pour que les modifications soient prise en compte.'%dlg.GetPath(),
                              u'Attention !',
                              wx.ICON_EXCLAMATION
                              )
            except :
                wx.MessageBox(u"Vous n'avez pas les droits n�cessaires pour �crire dans le dossier :\n%s\n\n"
                              u"Certains modules ne fonctionneront pas\n\n"
                              u"Contactez votre administrateur syst�me pour vous donner les droits n�cessaires, "
                              u"ou modifiez manuellement le fichier :\n%s\n\n"
                              u"(consultez l'aide de Coban ou le site\n"
                              u"http://sg-logiciels.fr pour plus d'informations)." %(os.getcwd(), os.path.join(os.getcwd(), fichierConf)),
                              u'Erreur !',
                              wx.ICON_WARNING)
                
            
            dlg.Destroy()
            sys.exit()
        else :
##            wx.MessageBox(u"Vous n'avez pas modifi� le r�pertoire de sauvegarde.",
##                          u'Attention !',
##                          wx.ICON_EXCLAMATION
##                          )
            dlg.Destroy()
            
            
        
    ###########################################################################################
    ###################################### pour Windows #######################################
    def onEnregistrement(self, evt):
        
        class TestDialog(wx.Dialog):
            def __init__(
                    self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
                    style=wx.DEFAULT_DIALOG_STYLE,
                    ):
                
                pre = wx.PreDialog()
                pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
                pre.Create(parent, ID, title, pos, size, style)
                self.PostCreate(pre)
                
                sizer = wx.BoxSizer(wx.VERTICAL)
                
                box = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(self, -1, u"             www.sg-logiciels.fr\npour obtenir votre code de d�blocage")
                box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
                sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                
                line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
                sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
                
                box = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(self, -1, u"Num�ro de facture :")
                box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
                self.textLicence = wx.TextCtrl(self, -1, "", size=(100,-1))
                box.Add(self.textLicence, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
                
                sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                
                box = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(self, -1, u"Code de d�blocage :")
                box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
                self.textCode = wx.TextCtrl(self, -1, "", size=(200,-1))
                box.Add(self.textCode, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
                
                sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                
                line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
                sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
                
                btnsizer = wx.StdDialogButtonSizer()
                
                btn = wx.Button(self, wx.ID_OK)
                btn.SetDefault()
                btnsizer.AddButton(btn)
                
                btn = wx.Button(self, wx.ID_CANCEL)
                btnsizer.AddButton(btn)
                btnsizer.Realize()
                
                sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                
                self.SetSizer(sizer)
                sizer.Fit(self)
        
        #---------------------------------------------------------------------------
        
        
        dlg = TestDialog(self, -1, u"Enregistrement", size=(400, 200),
                         style=wx.DEFAULT_DIALOG_STYLE
                         )
        dlg.CenterOnScreen()

        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
            config = []
            config.append(dlg.textLicence.GetValue())
            config.append(dlg.textCode.GetValue().upper())
            
            f = open(fichierConf, 'r')
            self.cheminParDef = pickle.load(f)
            f.close()
            
            try :
                f = open(os.path.join(os.path.expanduser(self.cheminParDef), 'licence.cob'), 'w')
                pickle.dump(config, f)
                f.close()
                wx.MessageBox(u"\n\nCoban doit �tre relanc� pour que l'enregistrement soit pris en compte.",
                          u'Attention !',
                          wx.ICON_EXCLAMATION
                          )
                dlg.Destroy()
            except :
                wx.MessageBox(u"Vous n'avez pas les droits n�cessaires pour �crire dans le dossier :\n%s\n\n"
                              u"Certains modules ne fonctionneront pas\n\n"
                              u"Contactez votre administrateur syst�me pour vous donner les droits n�cessaires, "
                              u"ou modifiez manuellement le fichier :\n%s\n\n"
                              u"(consultez l'aide de Coban ou le site\n"
                              u"http://www.sg-logiciels.fr pour plus d'informations)." %(os.getcwd(), os.path.join(os.getcwd(), fichierConf)),
                              u'Erreur !',
                              wx.ICON_WARNING)
                dlg.Destroy()
            sys.exit()
            
        else:
            dlg.Destroy()
        
        
    #######################################################################################################
        
        
    def onQuitter(self, evt):
        """Quitter l'application"""
        self.Destroy()

    def onAide(self, evt):
        # ouvre le fichier d'aide dans le navigateur de l'OS si possible
        try :
            import webbrowser
            chemin = "help.html"
            chemin = os.path.normpath(chemin)
            webbrowser.open(chemin)
        # sinon le faire manuellement
        except :
            wx.MessageBox(u'impossible d\'ouvrir le fichier d\'aide.\n'
                          u'Consultez le fichier d\'aide se trouvant dans '
                          u'le r�pertoire d\'installation de Coban\n\n'
                          u'(Par exemple C:\\Program Files\\Coban\help.html sous Windows)',
                          u'Attention !',
                          wx.ICON_EXCLAMATION)

    
    def onApropos(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = "Coban"
        info.Version = "%s" % Version
        info.WebSite = "http://www.sg-logiciels.fr"
        licenseText = (u"\n\nCoban est un programme informatique destin� aux �lectriciens et" 
                       u"\npermettant d'estimer rapidement la section d'un c�ble, de r�aliser des"
                       u"\nconversions d'unit�s �lectriques, etc.... "
                       u"\n\nVoir la Licence pour plus de d�tails"
                       u"\n( voir le fichier \"licence.txt\")")
        info.Description = (u"Coban est un utilitaire destin� aux �lectriciens \n"
                            u"et permettant d'estimer rapidement la section d'un c�ble,\n"
                            u"de r�aliser des conversions d'unit�s �lectriques, etc..."
                            u'\n\nVoir le fichier "licence.txt" pour consulter la licence d\'utilisation.' 
                            u"\n\nPour tout contact, visiter le site :")
        info.Developers = [ u"St�phan GU�RIN | contact@sg-logiciels.fr"]
        info.Licence = licenseText
        wx.AboutBox(info)   
        
        
        
def main():
    app = Coban(False)
    app.MainLoop()

#if __name__ == "__main__":
    #app = Coban()
    #app.MainLoop()
