#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module des fonctions réutilisables
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
import string, os

#------------ VARIABLES GLOBALES --------------------------------------

favicon = "images/coban.ico"
logo = "images/coban.png"        
bmp_plus = "images/plus.png"
bmp_plus_16 = "images/plus_16.png"
bmp_moins = "images/moins.png"
bmp_moins_16 = "images/moins_16.png"
bmp_pref = "images/pref.png"
bmp_pref_16 = "images/pref_16.png"
bmp_raz = "images/raz.png"
bmp_raz_16 = "images/raz_16.png"
bmp_quit = "images/quit.png"
bmp_quit_16 = "images/quit_16.png"
bmp_aide = "images/help.png"
bmp_aide_16 = "images/help_16.png"
fichierConf = os.path.join(os.path.join(os.path.expanduser("~"),'.coban'), 'config.cob')

#------------ CLASSES -------------------------------------------------

class ValidDigitPoint(wx.PyValidator):
    """ uniquement des digits et le . """
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return ValidDigitPoint()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        
        for x in val:
            if x not in string.digits+".":
                return False
            
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        
        if chr(key) in string.digits+".":
            event.Skip()
            return
        
        if not wx.Validator_IsSilent():
            wx.Bell()
            
        return
    
class ValidDigitPoint2(wx.PyValidator):
    """ uniquement des digits, le '.' e le '*' """
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return ValidDigitPoint2()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        
        for x in val:
            if x not in string.digits+"."+"*":
                return False
            
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        
        if chr(key) in string.digits+"."+"*":
            event.Skip()
            return
        
        if not wx.Validator_IsSilent():
            wx.Bell()
            
        return
    
#------------- DÉFINITIONS --------------------------------------------

def icone(dlg):
    """ Insère l'icone de l'application sur les fenêtres créées """
    icon = wx.Icon(favicon, wx.BITMAP_TYPE_ICO)
    dlg.SetIcon(icon)
    
#---------------------------------------------------------------------------
    
def testFich(f):
    """teste si le fichier existe et retourne 1 - sinon le crée et retourne 0 """
    try : 
        fich = open(f, 'r')
        fich.close()
        return 1
    except : 
        fich = open(f, "w")
        fich.close()
        return 0



    
#----------------------------------------------------------------------

def testFloat(entree, valdef = 0):
    """
    testFloat(entree, valdef = 0)\n
    Teste si la valeur entree peut être convertie en "float", sinon affiche un messageBox d'erreur.\n
    Si OK retourne la valeur au format "float".\n
    Sinon, retourne la valeur valdef (0 par défaut)
    """
    try:
        val = float(entree.GetValue())
        entree.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        entree.Refresh()
        return val
    except :
        wx.MessageBox(u"La valeur entrée est incorrecte !\n"
                      u"et doit être de la forme xx.y\n"
                      u"\nLe calcul sera erroné !!!"
                      , "Erreur")
        entree.SetBackgroundColour("pink")
        entree.SetFocus()
        entree.Refresh()
        return valdef

    
def testFloatCalc(entree, valdef = 0):
    """
    testFloat(entree, valdef = 0)\n
    Teste si la valeur entree peut être convertie en "float".
    Teste aussi si un calcul peut être effectué (multiplication).
    Sinon affiche un messageBox d'erreur.\n
    Si OK retourne la valeur au format "float".\n
    Sinon, retourne la valeur valdef (0 par défaut)
    """
    try:
        try :    
            val = float(entree.GetValue())
            entree.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            entree.Refresh()
            return val
        except :
            longueur = ''
            largeur = ''
            multip = 0
            for char in entree.GetValue() :
                if multip == 0 and char != "*":
                    longueur += char
                elif char == "*":
                    multip = 1
                else : 
                    largeur += char
            l1 = float(longueur)
            l2 = float(largeur)
            val = l1*l2
            entree.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            entree.Refresh()
            return val
                
    except :
        wx.MessageBox(u"La valeur entrée est incorrecte !\n"
                      u"et doit être de la forme xx.y\n"
                      u"\nLe calcul sera erroné !!!"
                      , "Erreur")
        entree.SetBackgroundColour("pink")
        entree.SetFocus()
        entree.Refresh()
        return valdef

#----------------------------------------------------------------------
