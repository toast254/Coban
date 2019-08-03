#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

##----------------------------------------------------------------------------------------------
## Coban - Module des fonctions r�utilisables
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
    
#------------- D�FINITIONS --------------------------------------------

def icone(dlg):
    """ Ins�re l'icone de l'application sur les fen�tres cr��es """
    icon = wx.Icon(favicon, wx.BITMAP_TYPE_ICO)
    dlg.SetIcon(icon)
    
#---------------------------------------------------------------------------
    
def testFich(f):
    """teste si le fichier existe et retourne 1 - sinon le cr�e et retourne 0 """
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
    Teste si la valeur entree peut �tre convertie en "float", sinon affiche un messageBox d'erreur.\n
    Si OK retourne la valeur au format "float".\n
    Sinon, retourne la valeur valdef (0 par d�faut)
    """
    try:
        val = float(entree.GetValue())
        entree.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        entree.Refresh()
        return val
    except :
        wx.MessageBox(u"La valeur entr�e est incorrecte !\n"
                      u"et doit �tre de la forme xx.y\n"
                      u"\nLe calcul sera erron� !!!"
                      , "Erreur")
        entree.SetBackgroundColour("pink")
        entree.SetFocus()
        entree.Refresh()
        return valdef

    
def testFloatCalc(entree, valdef = 0):
    """
    testFloat(entree, valdef = 0)\n
    Teste si la valeur entree peut �tre convertie en "float".
    Teste aussi si un calcul peut �tre effectu� (multiplication).
    Sinon affiche un messageBox d'erreur.\n
    Si OK retourne la valeur au format "float".\n
    Sinon, retourne la valeur valdef (0 par d�faut)
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
        wx.MessageBox(u"La valeur entr�e est incorrecte !\n"
                      u"et doit �tre de la forme xx.y\n"
                      u"\nLe calcul sera erron� !!!"
                      , "Erreur")
        entree.SetBackgroundColour("pink")
        entree.SetFocus()
        entree.Refresh()
        return valdef

#----------------------------------------------------------------------
