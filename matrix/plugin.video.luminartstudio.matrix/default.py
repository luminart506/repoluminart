# -*- coding: utf-8 -*-

import sys
try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
import datetime
from datetime import datetime
import re
import os
import base64
import codecs
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import time

try:
    import json
except:
    import simplejson as json


##CONFIGURAÇÕES
####  TITULO DO MENU  #################################################################
title_menu = '[COLOR orange][B]BEM-VINDOS AO LUMINART MTX[/B][/COLOR]'
###  DESCRIÇÃO DO ADDON ###############################################################
title_descricao = 'LUMINART STUDIO - Muito conteudo em servidores variados'

####  LINK DO TITULO DE MENU  #########################################################
## OBS: POR PADRÃO JÁ TEM UM MENU EM BRANCO PARA NÃO TER ERRO AO CLICAR ###############
url_b64_title = ''
#url_title = base64.b64decode(url_b64_title).decode('utf-8')
url_title = ''


##### PESQUISA - get.php
#url_b64_pesquisa = ''
#url_pesquisa = base64.b64decode(url_b64_pesquisa).decode('utf-8')
url_pesquisa = 'http://teste.com/get.php'
menu_pesquisar = '[COLOR white][B]PESQUISAR[/B][/COLOR]'
thumb_pesquisar = ''
fanart_pesquisar = ''
#### Descrição Pesquisa
desc_pesquisa = 'Pesquise por filme'
## MENU CONFIGURAÇÕES
menu_configuracoes = '[COLOR orange][B]Configurações[/B][/COLOR]'
thumb_icon_config = ''
desc_configuracoes = 'Configurações do LUMINART STUDIO'
## FAVORITOS
menu_favoritos = '[COLOR white][B]FAVORITOS[/B][/COLOR]'
thumb_favoritos = ''
desc_favoritos = 'Adicione Itens aos Favoritos, pressionando OK do controle'

#### MENU VIP ################################################################
titulo_vip = '[COLOR orange][B]LUMINART STUDIO[/B] [/COLOR]'
thumbnail_vip = 'htt://ia601504.us.archive.org/0/items/vip_20200719/vip.jpg'
fanart_vip = 'htt://ia601504.us.archive.org/0/items/vip_20200719/vip.jpg'
#### DESCRIÇÃO VIP ###########################################################
vip_descricao = 'SOLICITE SEU ACESSO VIP, CONTATE OS GRUPOS DE SUPORTE'
#### DIALOGO VIP - SERVIDOR DESATIVADO - CLICK ###################################
vip_dialogo = '[COLOR orange][B]CONFIGURE SEU ACESSO A NOSSA ÁREA VIP ANTES DE ENTRAR AQUI, MAIS INFORMAÇÕES ENTRE EM CONTATO COM NOSSO SUPORTE\nENTRE EM CONTATO PELO WHATSAPP: 55+ (48) 99194-1409 E SOLICITE SEU ACESSO[/B][/COLOR]'
##SERIVODR VIP
url_server_vip = ''


## MULTLINK
## nome para $nome, padrão: lsname para $lsname
playlist_command = 'nome'
dialog_playlist = 'Selecione um item'


# user agent - Padrão: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

# Base - seu link principal
url_b64_principal_vip = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0dVNzEyLzFBMS1FTlQuVklQL21haW4vMUIxLUVOVC1WSVAtTVRY'
url_principal_vip = base64.b64decode(url_b64_principal_vip).decode('utf-8')

url_b64_principal_free = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0dVNzEyLzFCMS1FTlQuR1JBVC1WSVAvbWFpbi8xQjEtRU5ULU1UWC1GUkVF'
url_principal_free = base64.b64decode(url_b64_principal_free).decode('utf-8')

#name - mensagem suporte
addon_name = xbmcaddon.Addon().getAddonInfo('name')



if sys.argv[1] == 'limparFavoritos':
    Path = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    arquivo = os.path.join(Path, "favorites.dat")
    exists = os.path.isfile(arquivo)
    if exists:
        try:
            os.remove(arquivo)
        except:
            pass
    xbmcgui.Dialog().ok('Sucesso', '[B][COLOR red]Favoritos limpo com sucesso![/COLOR][/B]')
    xbmc.sleep(2000)
    exit()


if sys.argv[1] == 'SetPassword':
    addonID = xbmcaddon.Addon().getAddonInfo('id')
    addon_data_path = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
    if os.path.exists(addon_data_path)==False:
        os.mkdir(addon_data_path)
    xbmc.sleep(4)
    #Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    #arquivo = os.path.join(Path, "password.txt")
    arquivo = os.path.join(addon_data_path, "password.txt")
    exists = os.path.isfile(arquivo)
    keyboard = xbmcaddon.Addon().getSetting("keyboard")
    if exists == False:
        password = '0069'
        p_encoded = base64.b64encode(password.encode()).decode('utf-8')
        p_file1 = open(arquivo,'w')
        p_file1.write(p_encoded)
        p_file1.close()
        xbmc.sleep(4)
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            if int(keyboard) == 0:
                ps2 = dialog.numeric(0, 'Insira a nova senha:')
            else:
                ps2 = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
            if ps2 != '':
                ps2_b64 = base64.b64encode(ps2.encode()).decode('utf-8')
                p_file = open(arquivo,'w')
                p_file.write(ps2_b64)
                p_file.close()
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','A Senha foi alterada com sucesso!')
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel alterar a senha!')
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
    else:
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            if int(keyboard) == 0:
                ps2 = dialog.numeric(0, 'Insira a nova senha:')
            else:
                ps2 = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
            if ps2 != '':
                ps2_b64 = base64.b64encode(ps2.encode()).decode('utf-8')
                p_file = open(arquivo,'w')
                p_file.write(ps2_b64)
                p_file.close()
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','A Senha foi alterada com sucesso!')
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel alterar a senha!')
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
    exit()



addon_handle = int(sys.argv[1])
__addon__ = xbmcaddon.Addon()
addon = __addon__
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_version = __addon__.getAddonInfo('version')
try:
    profile = xbmcvfs.translatePath(__addon__.getAddonInfo('profile').decode('utf-8'))
except:
    profile = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))
try:
    home = xbmcvfs.translatePath(__addon__.getAddonInfo('path').decode('utf-8'))
except:
    home = xbmcvfs.translatePath(__addon__.getAddonInfo('path'))
favorites = os.path.join(profile, 'favorites.dat')
favoritos = xbmcaddon.Addon().getSetting("favoritos")
#arquivo_log = os.path.join(home, "log.txt")
icone_free = os.path.join(home, "icone_free.png")
icone_vip = os.path.join(home, "icone_vip.png")
pix_icon = os.path.join(home,'qrcode-pix.png')
contribuicao_icon = os.path.join(home,'contribuicao.png')


if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else:
    FAV = []


def notify(message, timeShown=5000):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, message, timeShown, __icon__))

def to_unicode(text, encoding='utf-8', errors='strict'):
    """Force text to unicode"""
    if isinstance(text, bytes):
        return text.decode(encoding, errors=errors)
    return text

def get_search_string(heading='', message=''):
    """Ask the user for a search string"""
    search_string = None
    keyboard = xbmc.Keyboard(message, heading)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_string = to_unicode(keyboard.getText())
    return search_string

def encode_b64(string):
    try:
        string = string.encode('utf-8')
    except:
        pass
    try:
        base64_string = base64.b64encode(string).decode('utf-8')
    except:
        base64_string = base64.b64encode(string)
    return base64_string


expirado = []
def getRequest(url):
    try:
        from urllib.parse import quote #python 3
    except ImportError:    
        from urllib import quote
    try: 
        import requests        
        username = addon.getSetting('username')
        password = addon.getSetting('password')
        usernameb64 = encode_b64(username)
        passwordb64 = encode_b64(password)
        urlb64 = encode_b64(url)
        painel_acesso = '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x6c\x75\x6d\x69\x6e\x61\x72\x74\x2e\x6f\x6e\x6c\x69\x6e\x65\x2f\x70\x61\x69\x6e\x65\x6c\x76\x69\x70\x2f\x3f\x61\x63\x74\x69\x6f\x6e\x3d\x61\x63\x65\x73\x73\x6f&username={0}&password={1}&url={2}'.format(quote(str(usernameb64)),quote(str(passwordb64)),quote(str(urlb64)))
        req = requests.get(url=painel_acesso,headers={'User-Agent': useragent, 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'},timeout=12)
        html = req.content
        try:
            html = html.decode('utf-8')
        except:
            pass
    except:
        html = ''
        notify('Falha ao acessar')
    if html == 'expirado':
        if not expirado:
            #xbmcgui.Dialog().ok('Luminart', 'O Login expirou ou não existe!')
            notify('Login expirou ou não existe!')
            expirado.append('expirado')
    return html

def vencimento():
    try:
        from urllib.parse import quote #python 3
    except ImportError:    
        from urllib import quote    
    try:
        import requests
        username = addon.getSetting('username')
        password = addon.getSetting('password')
        usernameb64 = encode_b64(username)
        passwordb64 = encode_b64(password)
        painel_acesso = '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x6c\x75\x6d\x69\x6e\x61\x72\x74\x2e\x6f\x6e\x6c\x69\x6e\x65\x2f\x70\x61\x69\x6e\x65\x6c\x76\x69\x70\x2f\x3f\x61\x63\x74\x69\x6f\x6e\x3d\x76\x65\x6e\x63\x69\x6d\x65\x6e\x74\x6f&username={0}&password={1}'.format(quote(str(usernameb64)),quote(str(passwordb64)))
        req = requests.get(url=painel_acesso,headers={'User-Agent': useragent, 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'})
        html = req.content
        try:
            html = html.decode('utf-8')
        except:
            pass
    except:
        html = 'desconhecido'
    xbmcgui.Dialog().ok('Luminart', 'Vencimento: %s'%str(html))

def getRequest_free(url):
    try:
        from urllib.parse import quote #python 3
    except ImportError:    
        from urllib import quote
    try: 
        import requests        
        req = requests.get(url=url,headers={'User-Agent': useragent, 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'},timeout=12)
        html = req.content
        try:
            html = html.decode('utf-8')
        except:
            pass
    except:
        html = ''
        notify('Falha ao acessar')
    return html
      

def getRequest2(url,ref,userargent=False):
    try:
        if ref > '':
            ref2 = ref
        else:
            ref2 = url
        if userargent:
            client_user = userargent
        else:
            client_user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'),('User-Agent', client_user),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'), ('Referer', ref2)]
        data = opener.open(url).read()
        response = data.decode('utf-8')
        return response
    except:
        pass

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r



def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match



def resolve_data(url):
    try:
        data = getRequest(url)
        import gzip, binascii
        #k = base64.b32decode('').decode('utf-8')
        k = base64.b32decode('').decode('utf-8')
        try:
            from StringIO import StringIO as BytesIO ## for Python 2
        except ImportError:            
            from io import BytesIO ## for Python 3
        if k in data:
            data = data.split(k)
            buf = BytesIO(binascii.unhexlify(data[0]))
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
    except:
        data = getRequest(url)        
    return data

def resolve_data_free(url):
    try:
        data = getRequest_free(url)
        import gzip, binascii
        #k = base64.b32decode('').decode('utf-8')
        k = base64.b32decode('').decode('utf-8')
        try:
            from StringIO import StringIO as BytesIO ## for Python 2
        except ImportError:            
            from io import BytesIO ## for Python 3
        if k in data:
            data = data.split(k)
            buf = BytesIO(binascii.unhexlify(data[0]))
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
    except:
        data = getRequest_free(url)        
    return data

def getData(url,fanart,pesquisa=False):
    adult = xbmcaddon.Addon().getSetting("adult")
    data = resolve_data(url)
    if isinstance(data, (int, str, list)):
        channels = re.compile('<channels>(.+?)</channels>',re.MULTILINE|re.DOTALL).findall(data)
        channel = re.compile('<channel>(.*?)</channel>',re.MULTILINE|re.DOTALL).findall(data)
        item = re.compile('<item>(.*?)</item>',re.MULTILINE|re.DOTALL).findall(data)
        if len(channels) >0:
            for channel in channel:
                linkedUrl=''
                lcount=0
                try:
                    linkedUrl = re.compile('<externallink>(.*?)</externallink>').findall(channel)[0]
                    lcount=len(re.compile('<externallink>(.*?)</externallink>').findall(channel))
                except: pass

                name = re.compile('<name>(.*?)</name>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                try:
                    thumbnail = re.compile('<thumbnail>(.*?)</thumbnail>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                except:
                    thumbnail = ''
                try:
                    fanart1 = re.compile('<fanart>(.*?)</fanart>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                except:
                    fanart1 = ''

                if not fanart1:
                    if __addon__.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = fanart1
                if fanArt == None:
                    #raise
                    fanArt = ''

                try:
                    desc = re.compile('<info>(.*?)</info>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if desc == None:
                        #raise
                        desc = ''
                except:
                    desc = ''

                try:
                    genre = re.compile('<genre>(.*?)</genre>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if genre == None:
                        #raise
                        genre = ''
                except:
                    genre = ''

                try:
                    date = re.compile('<date>(.*?)</date>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if date == None:
                        #raise
                        date = ''
                except:
                    date = ''

                try:
                    credits = re.compile('<credits>(.*?)</credits>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if credits == None:
                        #raise
                        credits = ''
                except:
                    credits = ''

                try:
                    year = re.compile('<year>(.*?)</year>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if year == None:
                        #raise
                        year = ''
                except:
                    year = ''

                try:
                    director = re.compile('<director>(.*?)</director>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if director == None:
                        #raise
                        director = ''
                except:
                    director = ''

                try:
                    writer = re.compile('<writer>(.*?)</writer>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if writer == None:
                        #raise
                        writer = ''
                except:
                    writer = ''

                try:
                    duration = re.compile('<duration>(.*?)</duration>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if duration == None:
                        #raise
                        duration = ''
                except:
                    duration = ''

                try:
                    premiered = re.compile('<premiered>(.*?)</premiered>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if premiered == None:
                        #raise
                        premiered = ''
                except:
                    premiered = ''

                try:
                    studio = re.compile('<studio>(.*?)</studio>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if studio == None:
                        #raise
                        studio = ''
                except:
                    studio = ''

                try:
                    rate = re.compile('<rate>(.*?)</rate>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if rate == None:
                        #raise
                        rate = ''
                except:
                    rate = ''

                try:
                    originaltitle = re.compile('<originaltitle>(.*?)</originaltitle>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if originaltitle == None:
                        #raise
                        originaltitle = ''
                except:
                    originaltitle = ''

                try:
                    country = re.compile('<country>(.*?)</country>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if country == None:
                        #raise
                        country = ''
                except:
                    country = ''

                try:
                    rating = re.compile('<country>(.*?)</country>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if rating == None:
                        #raise
                        rating = ''
                except:
                    rating = ''

                try:
                    userrating = re.compile('<userrating>(.*?)</userrating>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if userrating == None:
                        #raise
                        userrating = ''
                except:
                    userrating = ''

                try:
                    votes = re.compile('<votes>(.*?)</votes>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if votes == None:
                        #raise
                        votes = ''
                except:
                    votes = ''

                try:
                    aired = re.compile('<aired>(.*?)</aired>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if aired == None:
                        #raise
                        aired = ''
                except:
                    aired = ''

                try:
                    if linkedUrl=='':
                        #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                        #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                        addDir(name.encode('utf-8', 'ignore'),'',1,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                    else:
                        #print linkedUrl
                        #addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                        if adult == 'false' and re.search("ADULTOS",name,re.IGNORECASE) and name.find('(+18)') >=0:
                            pass
                        else:
                            addDir(name.encode('utf-8', 'ignore'),linkedUrl,1,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                except:
                    notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
        elif re.search("#EXTM3U",data) or re.search("#EXTINF",data):
            get_m3u8(url,data)
        else:
            #getItems(soup('item'),fanart)
            getItems(item,fanart,pesquisa)
    else:
        #parse_m3u(soup)
        notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
    if '<SetContent>' in data:
        try:
            content=re.findall('<SetContent>(.*?)<',data)[0]
            xbmcplugin.setContent(addon_handle, str(content))
        except:
            xbmcplugin.setContent(addon_handle, 'movies')
    else:
        xbmcplugin.setContent(addon_handle, 'movies')

    if '<SetViewMode>' in data:
        try:
            viewmode=re.findall('<SetViewMode>(.*?)<',data)[0]
            xbmc.executebuiltin("Container.SetViewMode(%s)"%viewmode)
            #print 'done setview',viewmode
        except: pass

def getData_free(url,fanart,pesquisa=False):
    adult = xbmcaddon.Addon().getSetting("adult")
    data = resolve_data_free(url)
    if isinstance(data, (int, str, list)):
        channels = re.compile('<channels>(.+?)</channels>',re.MULTILINE|re.DOTALL).findall(data)
        channel = re.compile('<channel>(.*?)</channel>',re.MULTILINE|re.DOTALL).findall(data)
        item = re.compile('<item>(.*?)</item>',re.MULTILINE|re.DOTALL).findall(data)
        if len(channels) >0:
            for channel in channel:
                linkedUrl=''
                lcount=0
                try:
                    linkedUrl = re.compile('<externallink>(.*?)</externallink>').findall(channel)[0]
                    lcount=len(re.compile('<externallink>(.*?)</externallink>').findall(channel))
                except: pass

                name = re.compile('<name>(.*?)</name>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                try:
                    thumbnail = re.compile('<thumbnail>(.*?)</thumbnail>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                except:
                    thumbnail = ''
                try:
                    fanart1 = re.compile('<fanart>(.*?)</fanart>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                except:
                    fanart1 = ''

                if not fanart1:
                    if __addon__.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = fanart1
                if fanArt == None:
                    #raise
                    fanArt = ''

                try:
                    desc = re.compile('<info>(.*?)</info>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if desc == None:
                        #raise
                        desc = ''
                except:
                    desc = ''

                try:
                    genre = re.compile('<genre>(.*?)</genre>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if genre == None:
                        #raise
                        genre = ''
                except:
                    genre = ''

                try:
                    date = re.compile('<date>(.*?)</date>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if date == None:
                        #raise
                        date = ''
                except:
                    date = ''

                try:
                    credits = re.compile('<credits>(.*?)</credits>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if credits == None:
                        #raise
                        credits = ''
                except:
                    credits = ''

                try:
                    year = re.compile('<year>(.*?)</year>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if year == None:
                        #raise
                        year = ''
                except:
                    year = ''

                try:
                    director = re.compile('<director>(.*?)</director>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if director == None:
                        #raise
                        director = ''
                except:
                    director = ''

                try:
                    writer = re.compile('<writer>(.*?)</writer>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if writer == None:
                        #raise
                        writer = ''
                except:
                    writer = ''

                try:
                    duration = re.compile('<duration>(.*?)</duration>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if duration == None:
                        #raise
                        duration = ''
                except:
                    duration = ''

                try:
                    premiered = re.compile('<premiered>(.*?)</premiered>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if premiered == None:
                        #raise
                        premiered = ''
                except:
                    premiered = ''

                try:
                    studio = re.compile('<studio>(.*?)</studio>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if studio == None:
                        #raise
                        studio = ''
                except:
                    studio = ''

                try:
                    rate = re.compile('<rate>(.*?)</rate>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if rate == None:
                        #raise
                        rate = ''
                except:
                    rate = ''

                try:
                    originaltitle = re.compile('<originaltitle>(.*?)</originaltitle>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if originaltitle == None:
                        #raise
                        originaltitle = ''
                except:
                    originaltitle = ''

                try:
                    country = re.compile('<country>(.*?)</country>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if country == None:
                        #raise
                        country = ''
                except:
                    country = ''

                try:
                    rating = re.compile('<country>(.*?)</country>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if rating == None:
                        #raise
                        rating = ''
                except:
                    rating = ''

                try:
                    userrating = re.compile('<userrating>(.*?)</userrating>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if userrating == None:
                        #raise
                        userrating = ''
                except:
                    userrating = ''

                try:
                    votes = re.compile('<votes>(.*?)</votes>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if votes == None:
                        #raise
                        votes = ''
                except:
                    votes = ''

                try:
                    aired = re.compile('<aired>(.*?)</aired>',re.MULTILINE|re.DOTALL).findall(channel)[0]
                    if aired == None:
                        #raise
                        aired = ''
                except:
                    aired = ''

                try:
                    if linkedUrl=='':
                        #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                        #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                        addDir(name.encode('utf-8', 'ignore'),'',24,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                    else:
                        #print linkedUrl
                        #addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                        if adult == 'false' and re.search("ADULTOS",name,re.IGNORECASE) and name.find('(+18)') >=0:
                            pass
                        else:
                            addDir(name.encode('utf-8', 'ignore'),linkedUrl,24,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                except:
                    notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
        elif re.search("#EXTM3U",data) or re.search("#EXTINF",data):
            get_m3u8_free(url,data)
        else:
            #getItems(soup('item'),fanart)
            getItems(item,fanart,pesquisa)
    else:
        #parse_m3u(soup)
        notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
    if '<SetContent>' in data:
        try:
            content=re.findall('<SetContent>(.*?)<',data)[0]
            xbmcplugin.setContent(addon_handle, str(content))
        except:
            xbmcplugin.setContent(addon_handle, 'movies')
    else:
        xbmcplugin.setContent(addon_handle, 'movies')

    if '<SetViewMode>' in data:
        try:
            viewmode=re.findall('<SetViewMode>(.*?)<',data)[0]
            xbmc.executebuiltin("Container.SetViewMode(%s)"%viewmode)
            #print 'done setview',viewmode
        except: pass

def get_m3u8(url,data):
    f4m = xbmcvfs.translatePath('special://home/addons/plugin.video.f4mTester')
    if os.path.exists(f4m)==True:
        f4mtester = True
    else:
        f4mtester = False     
    content = data.rstrip()
    try:
        url = url.encode('utf-8')
    except:
        pass
    try:
        url = base64.b32encode(base64.b16encode(url)).decode('utf-8')
    except:
        pass
    content = data.rstrip()
    match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
    if match1 !=[]:
        group_list = []
        for thumbnail,cat,channel_name,stream_url in match1:
            if not cat in group_list:
                group_list.append(cat)
                if cat == '':
                    cat = 'Desconhecido'
                addDir(cat.encode('utf-8', 'ignore'),url.encode('utf-8'),21,'','','','','','','','','','','','','','','','','','','')
    elif match1 ==[]:
        match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
        group_list = []
        for other,channel_name,stream_url in match2:
            if 'tvg-logo' in other:
                thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                if thumbnail:
                    if thumbnail.startswith('http'):
                        thumbnail = thumbnail
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''
            else:
                thumbnail = ''

            if 'group-title' in other:
                cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
            else:
                cat = ''
            if cat > '':
                if not cat in group_list:
                    group_list.append(cat)
                    addDir(cat.encode('utf-8', 'ignore'),url.encode('utf-8'),21,'','','','','','','','','','','','','','','','','','','')
            else:
                if not 'plugin' in stream_url and not 'User-Agent' in stream_url and not 'Referer' in stream_url and not 'Origin' in stream_url and not 'Cookie' in stream_url:
                    stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                if '.m3u8' in stream_url and f4mtester and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                elif f4mtester and not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.rmvb' in stream_url and not '.mp3' in stream_url and not '.wmv' in stream_url and not '.wma' in stream_url and not '.ac3' in stream_url and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                if 'f4mTester' in stream_url:
                    stream_url = stream_url.replace('&amp;streamtype=', '&streamtype=').replace('&amp;name=', '&name=').replace('&amp;iconImage=', '&iconImage=').replace('&amp;thumbnailImage=', '&thumbnailImage=').replace('&amp;url=', '&url=')
                if re.search("Adult",cat,re.IGNORECASE) or re.search("ADULT",channel_name,re.IGNORECASE) or re.search("Blue Hustler",channel_name,re.IGNORECASE) or re.search("PlayBoy",channel_name,re.IGNORECASE) or re.search("Redlight",channel_name,re.IGNORECASE) or re.search("Sextreme",channel_name,re.IGNORECASE) or re.search("SexyHot",channel_name,re.IGNORECASE) or re.search("Venus",channel_name,re.IGNORECASE) or re.search("AST TV",channel_name,re.IGNORECASE) or re.search("ASTTV",channel_name,re.IGNORECASE) or re.search("AST.TV",channel_name,re.IGNORECASE) or re.search("BRAZZERS",channel_name,re.IGNORECASE) or re.search("CANDY",channel_name,re.IGNORECASE) or re.search("CENTOXCENTO",channel_name,re.IGNORECASE) or re.search("DORCEL",channel_name,re.IGNORECASE) or re.search("EROXX",channel_name,re.IGNORECASE) or re.search("PASSION",channel_name,re.IGNORECASE) or re.search("PENTHOUSE",channel_name,re.IGNORECASE) or re.search("PINK-O",channel_name,re.IGNORECASE) or re.search("PINK O",channel_name,re.IGNORECASE) or re.search("PRIVATE",channel_name,re.IGNORECASE) or re.search("RUSNOCH",channel_name,re.IGNORECASE) or re.search("SCT",channel_name,re.IGNORECASE) or re.search("SEXT6SENSO",channel_name,re.IGNORECASE) or re.search("SHALUN TV",channel_name,re.IGNORECASE) or re.search("VIVID RED",channel_name,re.IGNORECASE) or re.search("Porn",channel_name,re.IGNORECASE) or re.search("XY Plus",channel_name,re.IGNORECASE) or re.search("XY Mix",channel_name,re.IGNORECASE) or re.search("XY Mad",channel_name,re.IGNORECASE) or re.search("XXL",channel_name,re.IGNORECASE) or re.search("Desire",channel_name,re.IGNORECASE) or re.search("Bizarre",channel_name,re.IGNORECASE) or re.search("Sexy HOT",channel_name,re.IGNORECASE) or re.search("Reality Kings",channel_name,re.IGNORECASE) or re.search("Prive TV",channel_name,re.IGNORECASE) or re.search("Hustler TV",channel_name,re.IGNORECASE) or re.search("Extasy",channel_name,re.IGNORECASE) or re.search("Evil Angel",channel_name,re.IGNORECASE) or re.search("Erox",channel_name,re.IGNORECASE) or re.search("DUSK",channel_name,re.IGNORECASE) or re.search("Brazzers",channel_name,re.IGNORECASE) or re.search("Brasileirinhas",channel_name,re.IGNORECASE) or re.search("Pink Erotic",channel_name,re.IGNORECASE) or re.search("Passion",channel_name,re.IGNORECASE) or re.search("Passie",channel_name,re.IGNORECASE) or re.search("Meiden Van Holland Hard",channel_name,re.IGNORECASE) or re.search("Sext & Senso",channel_name,re.IGNORECASE) or re.search("Super One",channel_name,re.IGNORECASE) or re.search("Vivid TV",channel_name,re.IGNORECASE) or re.search("Hustler HD",channel_name,re.IGNORECASE) or re.search("SCT",channel_name,re.IGNORECASE) or re.search("Sex Ation",channel_name,re.IGNORECASE) or re.search("Hot TV",channel_name,re.IGNORECASE) or re.search("Hot HD",channel_name,re.IGNORECASE) or re.search("MILF",channel_name,re.IGNORECASE) or re.search("ANAL",channel_name,re.IGNORECASE) and not re.search("CANAL",channel_name,re.IGNORECASE) or re.search("PUSSY",channel_name,re.IGNORECASE) or re.search("ROCCO",channel_name,re.IGNORECASE) or re.search("BABES",channel_name,re.IGNORECASE) or re.search("BABIE",channel_name,re.IGNORECASE) or re.search("XY Max",channel_name,re.IGNORECASE) or re.search("TUSHY",channel_name,re.IGNORECASE) or re.search("FAKE TAXI",channel_name,re.IGNORECASE) or re.search("BLACKED",channel_name,re.IGNORECASE) or re.search("XXX",channel_name,re.IGNORECASE) or re.search("18",channel_name,re.IGNORECASE) or re.search("Porno",channel_name,re.IGNORECASE):
                    addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,10,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
                else:
                    addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,18,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
        if match2 ==[]:
            notify('Nenhuma lista M3U...')

def get_m3u8_free(url,data):
    f4m = xbmcvfs.translatePath('special://home/addons/plugin.video.f4mTester')
    if os.path.exists(f4m)==True:
        f4mtester = True
    else:
        f4mtester = False     
    content = data.rstrip()
    try:
        url = url.encode('utf-8')
    except:
        pass
    try:
        url = base64.b32encode(base64.b16encode(url)).decode('utf-8')
    except:
        pass
    content = data.rstrip()
    match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
    if match1 !=[]:
        group_list = []
        for thumbnail,cat,channel_name,stream_url in match1:
            if not cat in group_list:
                group_list.append(cat)
                if cat == '':
                    cat = 'Desconhecido'
                addDir(cat.encode('utf-8', 'ignore'),url.encode('utf-8'),25,'','','','','','','','','','','','','','','','','','','')
    elif match1 ==[]:
        match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
        group_list = []
        for other,channel_name,stream_url in match2:
            if 'tvg-logo' in other:
                thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                if thumbnail:
                    if thumbnail.startswith('http'):
                        thumbnail = thumbnail
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''
            else:
                thumbnail = ''

            if 'group-title' in other:
                cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
            else:
                cat = ''
            if cat > '':
                if not cat in group_list:
                    group_list.append(cat)
                    addDir(cat.encode('utf-8', 'ignore'),url.encode('utf-8'),25,'','','','','','','','','','','','','','','','','','','')
            else:
                if not 'plugin' in stream_url and not 'User-Agent' in stream_url and not 'Referer' in stream_url and not 'Origin' in stream_url and not 'Cookie' in stream_url:
                    stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                if '.m3u8' in stream_url and f4mtester and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                elif f4mtester and not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.rmvb' in stream_url and not '.mp3' in stream_url and not '.wmv' in stream_url and not '.wma' in stream_url and not '.ac3' in stream_url and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                if 'f4mTester' in stream_url:
                    stream_url = stream_url.replace('&amp;streamtype=', '&streamtype=').replace('&amp;name=', '&name=').replace('&amp;iconImage=', '&iconImage=').replace('&amp;thumbnailImage=', '&thumbnailImage=').replace('&amp;url=', '&url=')
                if re.search("Adult",cat,re.IGNORECASE) or re.search("ADULT",channel_name,re.IGNORECASE) or re.search("Blue Hustler",channel_name,re.IGNORECASE) or re.search("PlayBoy",channel_name,re.IGNORECASE) or re.search("Redlight",channel_name,re.IGNORECASE) or re.search("Sextreme",channel_name,re.IGNORECASE) or re.search("SexyHot",channel_name,re.IGNORECASE) or re.search("Venus",channel_name,re.IGNORECASE) or re.search("AST TV",channel_name,re.IGNORECASE) or re.search("ASTTV",channel_name,re.IGNORECASE) or re.search("AST.TV",channel_name,re.IGNORECASE) or re.search("BRAZZERS",channel_name,re.IGNORECASE) or re.search("CANDY",channel_name,re.IGNORECASE) or re.search("CENTOXCENTO",channel_name,re.IGNORECASE) or re.search("DORCEL",channel_name,re.IGNORECASE) or re.search("EROXX",channel_name,re.IGNORECASE) or re.search("PASSION",channel_name,re.IGNORECASE) or re.search("PENTHOUSE",channel_name,re.IGNORECASE) or re.search("PINK-O",channel_name,re.IGNORECASE) or re.search("PINK O",channel_name,re.IGNORECASE) or re.search("PRIVATE",channel_name,re.IGNORECASE) or re.search("RUSNOCH",channel_name,re.IGNORECASE) or re.search("SCT",channel_name,re.IGNORECASE) or re.search("SEXT6SENSO",channel_name,re.IGNORECASE) or re.search("SHALUN TV",channel_name,re.IGNORECASE) or re.search("VIVID RED",channel_name,re.IGNORECASE) or re.search("Porn",channel_name,re.IGNORECASE) or re.search("XY Plus",channel_name,re.IGNORECASE) or re.search("XY Mix",channel_name,re.IGNORECASE) or re.search("XY Mad",channel_name,re.IGNORECASE) or re.search("XXL",channel_name,re.IGNORECASE) or re.search("Desire",channel_name,re.IGNORECASE) or re.search("Bizarre",channel_name,re.IGNORECASE) or re.search("Sexy HOT",channel_name,re.IGNORECASE) or re.search("Reality Kings",channel_name,re.IGNORECASE) or re.search("Prive TV",channel_name,re.IGNORECASE) or re.search("Hustler TV",channel_name,re.IGNORECASE) or re.search("Extasy",channel_name,re.IGNORECASE) or re.search("Evil Angel",channel_name,re.IGNORECASE) or re.search("Erox",channel_name,re.IGNORECASE) or re.search("DUSK",channel_name,re.IGNORECASE) or re.search("Brazzers",channel_name,re.IGNORECASE) or re.search("Brasileirinhas",channel_name,re.IGNORECASE) or re.search("Pink Erotic",channel_name,re.IGNORECASE) or re.search("Passion",channel_name,re.IGNORECASE) or re.search("Passie",channel_name,re.IGNORECASE) or re.search("Meiden Van Holland Hard",channel_name,re.IGNORECASE) or re.search("Sext & Senso",channel_name,re.IGNORECASE) or re.search("Super One",channel_name,re.IGNORECASE) or re.search("Vivid TV",channel_name,re.IGNORECASE) or re.search("Hustler HD",channel_name,re.IGNORECASE) or re.search("SCT",channel_name,re.IGNORECASE) or re.search("Sex Ation",channel_name,re.IGNORECASE) or re.search("Hot TV",channel_name,re.IGNORECASE) or re.search("Hot HD",channel_name,re.IGNORECASE) or re.search("MILF",channel_name,re.IGNORECASE) or re.search("ANAL",channel_name,re.IGNORECASE) and not re.search("CANAL",channel_name,re.IGNORECASE) or re.search("PUSSY",channel_name,re.IGNORECASE) or re.search("ROCCO",channel_name,re.IGNORECASE) or re.search("BABES",channel_name,re.IGNORECASE) or re.search("BABIE",channel_name,re.IGNORECASE) or re.search("XY Max",channel_name,re.IGNORECASE) or re.search("TUSHY",channel_name,re.IGNORECASE) or re.search("FAKE TAXI",channel_name,re.IGNORECASE) or re.search("BLACKED",channel_name,re.IGNORECASE) or re.search("XXX",channel_name,re.IGNORECASE) or re.search("18",channel_name,re.IGNORECASE) or re.search("Porno",channel_name,re.IGNORECASE):
                    addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,10,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
                else:
                    addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,18,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
        if match2 ==[]:
            notify('Nenhuma lista M3U...')

def get_m3u8_2(name,url):
    f4m = xbmcvfs.translatePath('special://home/addons/plugin.video.f4mTester')
    if os.path.exists(f4m)==True:
        f4mtester = True
    else:
        f4mtester = False 
    try:
        name = name.decode('utf-8')
    except:
        pass
    if name == 'Desconhecido':
        name = ''
    data = resolve_data(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        xbmcplugin.setContent(addon_handle, 'movies')
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1 !=[]:
            for thumbnail,cat,channel_name,stream_url in match1:
                if cat == name:
                    if not 'plugin' in stream_url and not 'User-Agent' in stream_url and not 'Referer' in stream_url and not 'Origin' in stream_url and not 'Cookie' in stream_url:
                        stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                    if '.m3u8' in stream_url and f4mtester and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                        stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                    elif f4mtester and not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.rmvb' in stream_url and not '.mp3' in stream_url and not '.wmv' in stream_url and not '.wma' in stream_url and not '.ac3' in stream_url and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                        stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)                                
                    if 'f4mTester' in stream_url:
                        stream_url = stream_url.replace('&amp;streamtype=', '&streamtype=').replace('&amp;name=', '&name=').replace('&amp;iconImage=', '&iconImage=').replace('&amp;thumbnailImage=', '&thumbnailImage=').replace('&amp;url=', '&url=')
                    addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,18,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
        elif match1 ==[]:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            group_list = []
            for other,channel_name,stream_url in match2:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''
                if cat > '':
                    if cat == name:
                        if not 'plugin' in stream_url and not 'User-Agent' in stream_url and not 'Referer' in stream_url and not 'Origin' in stream_url and not 'Cookie' in stream_url:
                            stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                        if '.m3u8' in stream_url and f4mtester and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                            stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                        elif f4mtester and not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.rmvb' in stream_url and not '.mp3' in stream_url and not '.wmv' in stream_url and not '.wma' in stream_url and not '.ac3' in stream_url and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                            stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)                    
                        if 'f4mTester' in stream_url:
                            stream_url = stream_url.replace('&amp;streamtype=', '&streamtype=').replace('&amp;name=', '&name=').replace('&amp;iconImage=', '&iconImage=').replace('&amp;thumbnailImage=', '&thumbnailImage=').replace('&amp;url=', '&url=')
                        addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,18,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
            if match2 ==[]:
                notify('Nenhuma lista M3U...')
        xbmcplugin.endOfDirectory(addon_handle)

def get_m3u8_2_free(name,url):
    f4m = xbmcvfs.translatePath('special://home/addons/plugin.video.f4mTester')
    if os.path.exists(f4m)==True:
        f4mtester = True
    else:
        f4mtester = False 
    try:
        name = name.decode('utf-8')
    except:
        pass
    if name == 'Desconhecido':
        name = ''
    data = resolve_data_free(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        xbmcplugin.setContent(addon_handle, 'movies')
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1 !=[]:
            for thumbnail,cat,channel_name,stream_url in match1:
                if cat == name:
                    if not 'plugin' in stream_url and not 'User-Agent' in stream_url and not 'Referer' in stream_url and not 'Origin' in stream_url and not 'Cookie' in stream_url:
                        stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                    if '.m3u8' in stream_url and f4mtester and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                        stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                    elif f4mtester and not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.rmvb' in stream_url and not '.mp3' in stream_url and not '.wmv' in stream_url and not '.wma' in stream_url and not '.ac3' in stream_url and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                        stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)                                
                    if 'f4mTester' in stream_url:
                        stream_url = stream_url.replace('&amp;streamtype=', '&streamtype=').replace('&amp;name=', '&name=').replace('&amp;iconImage=', '&iconImage=').replace('&amp;thumbnailImage=', '&thumbnailImage=').replace('&amp;url=', '&url=')
                    addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,18,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
        elif match1 ==[]:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            group_list = []
            for other,channel_name,stream_url in match2:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''
                if cat > '':
                    if cat == name:
                        if not 'plugin' in stream_url and not 'User-Agent' in stream_url and not 'Referer' in stream_url and not 'Origin' in stream_url and not 'Cookie' in stream_url:
                            stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                        if '.m3u8' in stream_url and f4mtester and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                            stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)
                        elif f4mtester and not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.rmvb' in stream_url and not '.mp3' in stream_url and not '.wmv' in stream_url and not '.wma' in stream_url and not '.ac3' in stream_url and not 'pluto.tv' in stream_url and not 'plugin' in stream_url:
                            stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&name='+urllib.quote_plus(str(channel_name))+'&iconImage='+urllib.quote_plus(thumbnail)+'&thumbnailImage='+urllib.quote_plus(thumbnail)+'&url='+urllib.quote_plus(stream_url)                    
                        if 'f4mTester' in stream_url:
                            stream_url = stream_url.replace('&amp;streamtype=', '&streamtype=').replace('&amp;name=', '&name=').replace('&amp;iconImage=', '&iconImage=').replace('&amp;thumbnailImage=', '&thumbnailImage=').replace('&amp;url=', '&url=')
                        addDir2(channel_name.encode('utf-8', 'ignore'),stream_url,18,'',thumbnail,'','','','','','','','','','','','','','','','','','',False)
            if match2 ==[]:
                notify('Nenhuma lista M3U...')
        xbmcplugin.endOfDirectory(addon_handle)

def getItems(items,fanart,pesquisa=False):
    use_thumb = addon.getSetting('use_thumb')
    for item in items:
        try:
            name = re.compile('<title>(.*?)</title>',re.MULTILINE|re.DOTALL).findall(item)[0].replace(';','')
            if name == None or name == '':
                #raise
                name = 'unknown?'
        except:
            name = ''

        try:
            thumbnail = re.compile('<thumbnail>(.*?)</thumbnail>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if thumbnail == None:
                #raise
                thumbnail = ''
        except:
            thumbnail = ''

        try:
            fanart1 = re.compile('<fanart>(.*?)</fanart>',re.MULTILINE|re.DOTALL).findall(item)[0]
        except:
            fanart1 = ''

        if not fanart1:
            if __addon__.getSetting('use_thumb') == "true":
                fanArt = thumbnail
            else:
                fanArt = fanart
        else:
            fanArt = fanart1
        if fanArt == None:
            #raise
            fanArt = ''

        try:
            desc = re.compile('<info>(.*?)</info>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if desc == None:
                #raise
                desc = ''
        except:
            desc = ''

        try:
            category = re.compile('<category>(.*?)</category>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if category == None:
                #raise
                category = ''
        except:
            category = ''

        try:
            subtitle1 = re.compile('<subtitle>(.*?)</subtitle>',re.MULTILINE|re.DOTALL).findall(item)
            if len(subtitle1)>0:
                subtitle = subtitle1[0]
                subs = []
                for sub in subtitle1:
                    subs.append('<subtitle>'+sub+'</subtitle>')
                #subtitle2 = subtitle1
                subtitle2 = subs
            else:
                subtitle = ''
                subtitle2 = ''
        except:
            subtitle = ''
            subtitle2 = ''

        try:
            utube = re.compile('<utube>(.*?)</utube>',re.MULTILINE|re.DOTALL).findall(item)
            if len(utube)>0:
                utube = utube[0]
            else:
                utube = ''
        except:
            utube = ''

        try:
            utubelive = re.compile('<utubelive>(.*?)</utubelive>',re.MULTILINE|re.DOTALL).findall(item)
            if len(utubelive)>0:
                utubelive = utubelive[0]
            else:
                utubelive = ''
        except:
            utubelive = ''

        try:
            jsonrpc = re.compile('<jsonrpc>(.*?)</jsonrpc>',re.MULTILINE|re.DOTALL).findall(item)
            externallink = re.compile('<externallink>(.*?)</externallink>',re.MULTILINE|re.DOTALL).findall(item)
            link = re.compile('<link>(.*?)</link>',re.MULTILINE|re.DOTALL).findall(item)
            if len(jsonrpc)>0:
                url = jsonrpc[0]
                url2 = ''
            elif len(externallink)>0:
                url = externallink[0]
                url2 = ''
            elif len(link)>0:
                try:
                    url = link[0]
                    mylinks = []
                    for link in link:
                        mylinks.append('<link>'+link+'</link>')
                    #url2 = link
                    url2 = mylinks
                except:
                    url = link[0]
                    url2 = ''
            else:
                url = ''
                url2 = ''
        except:
            url = ''
            url2 = ''

        try:
            genre = re.compile('<genre>(.*?)</genre>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if genre == None:
                #raise
                genre = ''
        except:
            genre = ''

        try:
            date = re.compile('<date>(.*?)</date>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if date == None:
                #raise
                date = ''
        except:
            date = ''

        try:
            credits = re.compile('<credits>(.*?)</credits>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if credits == None:
                #raise
                credits = ''
        except:
            credits = ''

        try:
            year = re.compile('<year>(.*?)</year>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if year == None:
                #raise
                year = ''
        except:
            year = ''

        try:
            director = re.compile('<director>(.*?)</director>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if director == None:
                #raise
                director = ''
        except:
            director = ''

        try:
            writer = re.compile('<writer>(.*?)</writer>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if writer == None:
                #raise
                writer = ''
        except:
            writer = ''

        try:
            duration = re.compile('<duration>(.*?)</duration>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if duration == None:
                #raise
                duration = ''
        except:
            duration = ''

        try:
            premiered = re.compile('<premiered>(.*?)</premiered>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if premiered == None:
                #raise
                premiered = ''
        except:
            premiered = ''

        try:
            studio = re.compile('<studio>(.*?)</studio>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if studio == None:
                #raise
                studio = ''
        except:
            studio = ''

        try:
            rate = re.compile('<rate>(.*?)</rate>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if rate == None:
                #raise
                rate = ''
        except:
            rate = ''

        try:
            originaltitle = re.compile('<originaltitle>(.*?)</originaltitle>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if originaltitle == None:
                #raise
                originaltitle = ''
        except:
            originaltitle = ''

        try:
            country = re.compile('<country>(.*?)</country>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if country == None:
                #raise
                country = ''
        except:
            country = ''

        try:
            rating = re.compile('<rating>(.*?)</rating>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if rating == None:
                #raise
                rating = ''
        except:
            rating = ''

        try:
            userrating = re.compile('<userrating>(.*?)</userrating>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if userrating == None:
                #raise
                userrating = ''
        except:
            userrating = ''

        try:
            votes = re.compile('<votes>(.*?)</votes>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if votes == None:
                #raise
                votes = ''
        except:
            votes = ''

        try:
            aired = re.compile('<aired>(.*?)</aired>',re.MULTILINE|re.DOTALL).findall(item)[0]
            if aired == None:
                #raise
                aired = ''
        except:
            aired = ''

        #try:
        #    xbmcgui.Dialog().textviewer('Informação: ', item('director')[0].string)
        #except:
        #    pass

        #xbmcgui.Dialog().textviewer('Informação:', name)

        try:
            if name > '' and url == '' and not utube > '' and not utubelive > '':
                addLink(name.encode('utf-8', 'ignore'),'None','',thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
            elif name > '' and url == None and not utube > '' and not utubelive > '':
                addLink(name.encode('utf-8', 'ignore'),'None','',thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
            elif category == 'Adult' and url.find('redecanais') >= 0 and url.find('m3u8') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url,10,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif category == 'Adult' and url.find('canaismax') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url,10,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif url.find('canaismax') >= 0 and url.find('page') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif url.find('ultracine_page') >= 0 and not len(url2) >1:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif url.find('rc=') >= 0 and not len(url2) >1:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)                
            elif url.find('streamtape.com') >= 0 and not len(url2) >1:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif url.find('netcine2_page') >= 0 and not len(url2) >1:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif url.find('series_canaismax') >= 0 and not len(url2) >1:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif url.find('filmes_canaismax') >= 0 and not len(url2) >1:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif utube > '' and len(utube) == 11:
                link_youtube = 'plugin://plugin.video.youtube/play/?video_id='+utube
                addLink(name.encode('utf-8', 'ignore'), link_youtube,subtitle,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
            elif utubelive > '' and len(utubelive) == 11:
                link_live = 'https://www.youtube.com/watch?v='+utubelive
                addDir2(name.encode('utf-8', 'ignore'),link_live,17,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif len(externallink)>0:
                addDir(name.encode('utf-8', 'ignore'),resolver(url),1,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
            ##Multilink
            elif len(url2) >1 and len(subtitle2) >1 and re.search(playlist_command,url,re.IGNORECASE):
                name_resolve = name+'[COLOR white] ('+str(len(url2))+' itens)[/COLOR]'
                addDir2(name_resolve.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,str(subtitle2).replace(',','||'),thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif len(url2) >1 and re.search(playlist_command,url,re.IGNORECASE):
                name_resolve = name+'[COLOR white] ('+str(len(url2))+' itens)[/COLOR]'
                addDir2(name_resolve.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
                #addLink(name.encode('utf-8', 'ignore'),resolver(url),subtitle,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
            elif category == 'Adult':
                addDir2(name.encode('utf-8', 'ignore'),url,10,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            elif resolver(url).startswith('plugin://plugin.video.youtube/playlist') == True or resolver(url).startswith('plugin://plugin.video.youtube/channel') == True or resolver(url).startswith('plugin://plugin.video.youtube/user') == True or resolver(url).startswith('Plugin://plugin.video.youtube/playlist') == True:
                addDir(name.encode('utf-8', 'ignore'),resolver(url),6,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
            elif pesquisa:
                addDir2(name.encode('utf-8', 'ignore'),url,16,subtitle,thumbnail,fanArt,desc.encode('utf-8'),genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,False)
            else:
                #xbmcgui.Dialog().textviewer('Informação:', 'ok')
                #addLink(name.encode('utf-8', 'ignore'),resolver(url, name, thumbnail).encode('utf-8'),subtitle,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
                addLink(name.encode('utf-8', 'ignore'),resolver(url),subtitle,thumbnail,fanArt,desc,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired)
        except:
            notify('[COLOR red]Erro ao Carregar os items![/COLOR]')


def adult(name, url, iconimage, description, subtitle):
    try:
        Path = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    except:
        Path = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
    arquivo = os.path.join(Path, "password.txt")
    exists = os.path.isfile(arquivo)
    keyboard = xbmcaddon.Addon().getSetting("keyboard")
    if exists == False:
        parental_password()
        xbmc.sleep(10)
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            urlresolver = resolver(url)
            #if urlresolver.startswith("plugin://") and not 'elementum' in str(urlresolver):
            #    xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
            #elif urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
            #if urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
            #    xbmc.executebuiltin("ActivateWindow(10025," + urlresolver + ",return)")
            if urlresolver.startswith('plugin://'):
                xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')            
            else:
                li = xbmcgui.ListItem(name, path=urlresolver)
                li.setArt({"icon": iconimage, "thumb": iconimage})
                li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([subtitle])
                xbmc.Player().play(item=urlresolver, listitem=li)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
    else:
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            urlresolver = resolver(url)
            #if urlresolver.startswith("plugin://") and not 'elementum' in str(urlresolver):
            #    xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
            #elif urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
            #if urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
            #    xbmc.executebuiltin("ActivateWindow(10025," + urlresolver + ",return)")
            if urlresolver.startswith('plugin://'):
                xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')            
            else:
                li = xbmcgui.ListItem(name, path=urlresolver)
                li.setArt({"icon": iconimage, "thumb": iconimage})
                li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([subtitle])
                xbmc.Player().play(item=urlresolver, listitem=li)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')

def playlist(name, url, iconimage, description, subtitle):
    playlist_command1 = playlist_command
    dialog = xbmcgui.Dialog()
    links = re.compile('<link>([\s\S]*?)#'+playlist_command1+'', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
    names = re.compile('#'+playlist_command1+'=([\s\S]*?)</link>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
    names2 = []
    subtitles = re.compile('<subtitle>([\s\S]*?)</subtitle>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(subtitle)
    for name in names:
        myname = name.replace('+', ' ')
        names2.append(myname)
    if links !=[] and names2 !=[]:
        index = dialog.select(dialog_playlist, names2)
        if index >= 0:
            playname=names2[index]
            if playname > '':
                playname1 = playname
            else:
                playname1 = 'Desconhecido'
            playlink=links[index]
            if subtitles !=[]:
                playsub=subtitles[index]
            else:
                playsub = ''
            urlresolver = resolver(playlink)
            #if urlresolver.startswith("plugin://") and not 'elementum' in str(urlresolver):
            #    xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
            #elif urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
            #if urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
            #    xbmc.executebuiltin("ActivateWindow(10025," + urlresolver + ",return)")
            if urlresolver.startswith('plugin://') and not 'elementum' in str(urlresolver) and not 'tubemusic' in str(urlresolver):
                xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')            
            else:
                li = xbmcgui.ListItem(playname1, path=urlresolver)
                li.setArt({"icon": iconimage, "thumb": iconimage})
                li.setInfo(type='video', infoLabels={'Title': playname1, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([playsub])
                xbmc.Player().play(item=urlresolver, listitem=li)



def individual_player(name, url, iconimage, description, subtitle):
    urlresolver = resolver(url)
    if urlresolver.startswith('plugin://') and not 'elementum' in str(urlresolver):
        xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
    else:
        li = xbmcgui.ListItem(name, path=urlresolver)
        li.setArt({"icon": iconimage, "thumb": iconimage})
        li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        if subtitle > '':
            li.setSubtitles([subtitle])
        #xbmc.Player().play(item=urlresolver, listitem=li)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


def m3u8_player(name, url, iconimage, description, subtitle):
    if url.startswith('plugin://') and not 'elementum' in str(url):
        xbmc.executebuiltin('RunPlugin(' + url + ')')
    else:    
        li = xbmcgui.ListItem(name, path=url)
        li.setArt({"icon": iconimage, "thumb": iconimage})
        li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        if subtitle > '':
            li.setSubtitles([subtitle])
        xbmc.Player().play(item=url, listitem=li)


def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string
def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding, 'ignore')
    return string
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def sendJSON(command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)


def pluginquerybyJSON(url):
    json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}') %url

    json_folder_detail = json.loads(sendJSON(json_query))
    for i in json_folder_detail['result']['files'] :
        url = i['file']
        name = removeNonAscii(i['label'])
        thumbnail = removeNonAscii(i['thumbnail'])
        try:
            fanart = removeNonAscii(i['fanart'])
        except Exception:
            fanart = ''
        try:
            date = i['year']
        except Exception:
            date = ''
        try:
            episode = i['episode']
            season = i['season']
            if episode == -1 or season == -1:
                description = ''
            else:
                description = '[COLOR yellow] S' + str(season)+'[/COLOR][COLOR hotpink] E' + str(episode) +'[/COLOR]'
        except Exception:
            description = ''
        try:
            studio = i['studio']
            if studio:
                description += '\n Studio:[COLOR steelblue] ' + studio[0] + '[/COLOR]'
        except Exception:
            studio = ''

        desc = description+'\n\nDate: '+str(date)

        if i['filetype'] == 'file':
            #addLink(url,name,thumbnail,fanart,description,'',date,'',None,'',total=len(json_folder_detail['result']['files']))
            addLink(name.encode('utf-8', 'ignore'),url.encode('utf-8'),'',thumbnail,fanart,desc,'','','','','','','','','','','','','','','','')
            #xbmc.executebuiltin("Container.SetViewMode(500)")

        else:
            #addDir(name,url,53,thumbnail,fanart,description,'',date,'')
            addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),6,iconimage,fanart,desc,'','','','','','','','','','','','','','','','')
            #xbmc.executebuiltin("Container.SetViewMode(500)")

def youtube_live(url):
    data = getRequest2(url, 'https://www.youtube.com/')
    #print(data)
    match = re.compile('"hlsManifestUrl.+?"(.+?).m3u8', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if match !=[]:
        stream = match[0].replace(':\\"https:', 'https:').replace('\/', '/').replace('\n', '')+'.m3u8|Referer=https://www.youtube.com/|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        #print(stream)
        return stream
    else:
        stream = ''
        return stream


def youtube_live_player(name, url, iconimage, description, subtitle):
    li = xbmcgui.ListItem(name, path=youtube_live(url))
    li.setArt({"icon": iconimage, "thumb": iconimage})
    li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
    if subtitle > '':
        li.setSubtitles([subtitle])
    #xbmc.Player().play(item=youtube_live(url), listitem=li)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)



def youtube(url):
    plugin_url = url
    xbmc.executebuiltin("ActivateWindow(10025," + plugin_url + ",return)")



def youtube_resolver(url):
    link_youtube = url
    if link_youtube.startswith('https://www.youtube.com/watch?v') == True or link_youtube.startswith('https://youtube.com/watch?v') == True:
        get_id1 = re.compile('v=(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('v=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/play/?video_id='+id_video
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/play/?video_id='+id_video
        else:
            resolve = ''
    elif link_youtube.startswith('https://www.youtube.com/playlist?') == True or link_youtube.startswith('https://youtube.com/playlist?') == True:
        get_id1 = re.compile('list=(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('list=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/playlist/'+id_video+'/?page=0'
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/playlist/'+id_video+'/?page=0'
        else:
            resolve = ''
    elif link_youtube.startswith('https://www.youtube.com/channel') == True or link_youtube.startswith('https://youtube.com/channel') == True:
        get_id1 = re.compile('channel/(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('channel/(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/channel/'+id_video+'/'
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/channel/'+id_video+'/'
        else:
            resolve = ''
    elif link_youtube.startswith('https://www.youtube.com/user') == True or link_youtube.startswith('https://youtube.com/user') == True:
        get_id1 = re.compile('user/(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('user/(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/user/'+id_video+'/'
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/user/'+id_video+'/'
        else:
            resolve = ''

    else:
        resolve = ''
    return resolve


def youtube_restore(url):
    if url.find('/?video_id=') >= 0:
        find_id = re.compile('/?video_id=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
        normal_url = 'https://www.youtube.com/watch?v='+str(find_id[0])
    elif url.find('youtube/playlist/') >= 0:
        find_id = re.compile('/playlist/(.+?)/', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
        normal_url = 'https://www.youtube.com/playlist?list='+str(find_id[0])
    else:
        normal_url = ''
    return normal_url


def data_youtube(url, ref):
    try:
        try:
            import cookielib
        except ImportError:
            import http.cookiejar as cookielib
        try:
            import urllib2
        except ImportError:
            import urllib.request as urllib2
        if ref > '':
            ref2 = ref
        else:
            ref2 = url
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('Accept-Language', 'en-US,en;q=0.9;q=0.8'),('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'), ('Referer', ref2)]
        data = opener.open(url).read()
        response = data.decode('utf-8')
        return response
    except:
        #pass
        response = ''
        return response


def getPlaylistLinksYoutube(url):
    try:
        sourceCode = data_youtube(youtube_restore(url), '')
    except:
        sourceCode = ''
    ytb_re = re.compile('url":"https://i.ytimg.com/vi/(.+?)/hqdefault.+?"width":.+?,"height":.+?}]},"title".+?"text":"(.+?)"}],', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(sourceCode)
    for video_id,name in ytb_re:
        original_name = str(name).replace(r"\u0026","&").replace('\\', '')
        thumbnail = "https://img.youtube.com/vi/%s/0.jpg" % video_id
        fanart = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % video_id
        plugin_url = 'plugin://plugin.video.youtube/play/?video_id='+video_id
        urlfinal = str(plugin_url)
        description = ''
        addLink(original_name.encode('utf-8', 'ignore'),urlfinal,'',str(thumbnail),str(fanart),description,'','','','','','','','','','','','','','','','')


def canaismax(url):
    try:
        page = str(re.compile('canaismax_page=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)[0])
        data = getRequest2(page,'')
        source = re.compile('source.+?"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        source2 = re.compile('var.+?url.+?=.+?"(.+?)";', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if source2 !=[]:
            link = source2[0].replace('\n','').replace('\r','')
            if '.m3u8' in str(link):
                stream = str(link)
            else:
                stream = ''
        elif source !=[]:
            link = source[0].replace('\n','').replace('\r','')
            if '.m3u8' in str(link):
                stream = str(link)
            else:
                stream = ''
        else:
            stream = ''
        return stream
    except:
        stream = ''
        return stream


def netcine2(url):
    try:
        page = str(re.compile('netcine2_page=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)[0])
        data = getRequest2(page,'')
        source = re.compile('source.+?"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if source !=[]:
            link = source[0].replace('\n','').replace('\r','')
        else:
            link = ''
        return link
    except:
        link = ''
        return link


def ultracine(url):
    try:
        page = str(re.compile('ultracine_page=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)[0])
        data = getRequest2(page,'')
        source = re.compile('.log.+?"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if source !=[]:
            link = source[0].replace('\n','').replace('\r','')
        else:
            link = ''
        return link
    except:
        link = ''
        return link


def streamtape(url):
    correct_url = url.replace('streamtape.com/v/', 'streamtape.com/e/')
    data = getRequest2(correct_url,'')
    link_part1_re = re.compile('videolink.+?style="display:none;">(.*?)&token=').findall(data)
    link_part2_re = re.compile("<script>.+?token=(.*?)'.+?</script>").findall(data)
    if link_part1_re !=[] and link_part2_re !=[]:
        #link = 'https:'+link_re[0]+'&stream=1'
        #link = 'https:'+link_part1_re[0]+'&token='+link_part2_re[0]
        link = 'https:'+link_part1_re[0]+'&token='+link_part2_re[0]+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    else:
        link = ''
    return link


def series_canaismax(url):
    try:
        page = re.compile('series_canaismax=(.+?)&idioma=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
        link = page[0][0]
        idioma = page[0][1]
        if 'leg' in idioma or 'Leg' in idioma or 'LEG' in idioma:
            data = getRequest2(link,'')
            tags = re.compile('javascript.+?data-id="(.+?)".+?data-episodio="(.+?)".+?data-player="(.+?)".+?<i>(.+?)</i>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            tags2 = []
            for id,episodio,player,lang in tags:
                if 'LEG' in lang:
                    tags2.append((id,episodio,player))
            if tags2 !=[]:
                data_id = tags2[0][0]
                data_episodio = tags2[0][1]
                data_player = tags2[0][2]
                data2 = getRequest2('https://canaismax.com/embed/'+data_id+'/'+data_episodio+'/'+data_player,'')
                source = str(re.compile('source.+?"(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)[0])+'|Referer=https://canaismax.com/'
            else:
                source = ''
        elif 'dub' in idioma or 'Dub' in idioma or 'DUB' in idioma:
            data = getRequest2(link,'')
            tags = re.compile('javascript.+?data-id="(.+?)".+?data-episodio="(.+?)".+?data-player="(.+?)".+?<i>(.+?)</i>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            tags2 = []
            for id,episodio,player,lang in tags:
                if 'DUB' in lang:
                    tags2.append((id,episodio,player))
            if tags2 !=[]:
                data_id = tags2[0][0]
                data_episodio = tags2[0][1]
                data_player = tags2[0][2]
                data2 = getRequest2('https://canaismax.com/embed/'+data_id+'/'+data_episodio+'/'+data_player,'')
                source = str(re.compile('source.+?"(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)[0])+'|Referer=https://canaismax.com/'
            else:
                source = ''
        else:
            source = ''
        return source
    except:
        source = ''
        return source


def filmes_canaismax(url):
    try:
        page = re.compile('filmes_canaismax=(.+?)&idioma=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
        link = page[0][0]
        idioma = page[0][1]
        if 'leg' in idioma or 'Leg' in idioma or 'LEG' in idioma:
            data = getRequest2(link,'')
            tags = re.compile('javascript.+?data-id="(.+?)".+?data-player="(.+?)".+?<i>(.+?)</i>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            tags2 = []
            for id,player,lang in tags:
                if 'LEG' in lang:
                    tags2.append((id,player))
            if tags2 !=[]:
                data_id = tags2[0][0]
                data_player = tags2[0][1]
                data2 = getRequest2('https://canaismax.com/embed/'+data_id+'/'+data_player,'')
                source = str(re.compile('source.+?"(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)[0])+'|Referer=https://canaismax.com/'
            else:
                source = ''
        elif 'dub' in idioma or 'Dub' in idioma or 'DUB' in idioma:
            data = getRequest2(link,'')
            tags = re.compile('javascript.+?data-id="(.+?)".+?data-player="(.+?)".+?<i>(.+?)</i>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            tags2 = []
            for id,player,lang in tags:
                if 'DUB' in lang:
                    tags2.append((id,player))
            if tags2 !=[]:
                data_id = tags2[0][0]
                data_player = tags2[0][1]
                data2 = getRequest2('https://canaismax.com/embed/'+data_id+'/'+data_player,'')
                source = str(re.compile('source.+?"(.*?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)[0])+'|Referer=https://canaismax.com/'
            else:
                source = ''
        else:
            source = ''
        return source
    except:
        source = ''
        return source

def special_request(url,origin=False,referer=False,post=False):
    try:
        from urllib.parse import urlencode #python 3
    except ImportError:     
        from urllib import urlencode #python 2
    try:
        from urllib.request import Request, urlopen, URLError  # Python 3
    except ImportError:
        from urllib2 import Request, urlopen, URLError # Python 2
    try:
        from StringIO import StringIO ## for Python 2
    except ImportError:            
        from io import BytesIO as StringIO ## for Python 3
    import gzip
    req = Request(url)
    req.add_header('sec-ch-ua', '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"')
    req.add_header('sec-ch-ua-mobile', '?0')
    req.add_header('sec-ch-ua-platform', '"Windows"')
    req.add_header('Upgrade-Insecure-Requests', '1')    
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    req.add_header('Sec-Fetch-Site', 'none')
    req.add_header('Sec-Fetch-Mode', 'navigate')
    req.add_header('Sec-Fetch-User', '?1')
    req.add_header('Sec-Fetch-Dest', 'document')
    req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
    if origin:
        req.add_header('Origin', origin)    
    if referer:    
        req.add_header('Referer', referer)
    try:
        if post:
            post = urlencode(post)
            try:
                response = urlopen(req,data=post.encode('utf-8'))
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
            except:
                response = urlopen(req,data=post)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
        else:
            try:
                response = urlopen(req)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
            except:
                code = 401
                encoding = 'none'
    except:
        code = 401
        encoding = 'none'
    if code == 200:
        if encoding == 'gzip':
            try:
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            except:
                content = ''
        else:
            try:
                content = response.read()
            except:
                content = ''
    else:
        content = ''
    try:
        content = content.decode('utf-8')
    except:
        pass
    return content


def play_canais_rc(url):
    try:
        channel = str(re.compile('rc=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)[0])
        referer_player = 'https://sinalpublico.com/player3/ch.php?canal=%s&img=%s'%(channel,channel)
        base = special_request(url='https://sinalpublico.com/player3/ch.php?canal=%s&img=%s'%(channel,channel),referer='https://redecanaistv.net/')
        args = re.compile('\) \- (.+?)\)\;',re.MULTILINE|re.DOTALL).findall(base)[0]
        base = re.compile('<script>(.+?)\];',re.MULTILINE|re.DOTALL).findall(base)[0]
        base = re.compile('\[(.+)',re.MULTILINE|re.DOTALL).findall(base)[0]
        base = base.replace('\n','').replace('\r','')
        listar = re.compile('"(.+?)"').findall(base)
        base = ''
        for value in listar:
            novo = base64.b64decode(value).decode('utf-8')
            unpack = re.sub('\D','',novo)
            unpack = chr(int(unpack) - int(args))
            base += unpack
        channel = re.compile('source.+?"(.+?)"').findall(base)[0]
        stream = channel + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36&Referer=' + referer_player
        # li = xbmcgui.ListItem(path=stream)
        # #li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        # #xbmc.Player().play(item=stream, listitem=li)
        # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    except:
        stream = ''
    return stream

def resolver(link):
    link_decoded = link
    try:
        if not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://drive.google.com') == True:
            #print('verdadeiro')
            resolved = link_decoded.replace('http','plugin://plugin.video.gdrive?mode=streamURL&amp;url=http')
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('http://drive.google.com') == True:
            #print('verdadeiro')
            resolved = link_decoded.replace('http','plugin://plugin.video.gdrive?mode=streamURL&amp;url=http')
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('streamtape.com') >= 0:
            link = streamtape(link_decoded)
            resolved = link
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('rc=') >= 0:
            resolved = play_canais_rc(link_decoded)
            #print(resolved)            
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('ultracine_page') >= 0:
            link = ultracine(link_decoded)
            resolved = link
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('netcine2_page') >= 0:
            link = netcine2(link_decoded)
            resolved = link
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('series_canaismax') >= 0:
            link_corrigido = link_decoded.replace('idioma;', 'idioma')
            link = series_canaismax(link_corrigido)
            resolved = link
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('filmes_canaismax') >= 0:
            link_corrigido = link_decoded.replace('idioma;', 'idioma')
            link = filmes_canaismax(link_corrigido)
            resolved = link
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('eu-central-1.edge.mycdn.live') >= 0:
            #print('verdadeiro')
            resolved = link_decoded
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('canaismax_page') >= 0:
            stream = canaismax(link_decoded)
            resolved = stream+'|Referer=https://canaismax.com/|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://youtube.com/') == True or link_decoded.startswith('https://www.youtube.com/') == True:
            try:
                resultado = youtube_resolver(link_decoded)
                if resultado==None:
                    #print('vazio')
                    resolved = ''
                else:
                    resolved = resultado
            except:
                resolved = ''
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://photos.app') == True:
            try:
                data = getRequest2(link_decoded, 'https://photos.google.com/')
                result = re.compile('<meta property="og:video" content="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
                if result !=[]:
                    resolved = result[0].replace('-m18','-m22')
                else:
                    resolved = ''
            except:
                resolved = ''
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('magnet:?xt=') == True:
            resolved = 'plugin://plugin.video.elementum/play?uri='+link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.torrent') >= 0:
            resolved = 'plugin://plugin.video.elementum/play?uri='+link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mp4') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mkv') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.wmv') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.wma') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.avi') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mp3') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.ac3') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.rmvb') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        else:        
            resolved = link_decoded
        return resolved
    except:
        resolved = ''
        return resolved
        #pass
        #notify('[COLOR red]Não foi possivel resolver um link![/COLOR]')



def getFavorites():
    try:
        try:
            items = json.loads(open(favorites).read())
        except:
            items = ''
        total = len(items)
        if int(total) > 0:
            for i in items:
                name = i[0]
                url = i[1]
                try:
                    urldecode = base64.b64decode(base64.b16decode(url))
                except:
                    urldecode = url
                try:
                    url2 = urldecode.decode('utf-8')
                except:
                    url2 = urldecode

                mode = i[2]
                subtitle = i[3]
                try:
                    subtitledecode = base64.b64decode(base64.b16decode(subtitle))
                except:
                    subtitledecode = subtitle
                try:
                    sub2 = subtitledecode.decode('utf-8')
                except:
                    sub2 = subtitledecode
                iconimage = i[4]
                try:
                    fanArt = i[5]
                    if fanArt == None:
                        raise
                except:
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = iconimage
                    else:
                        fanArt = fanart
                description = i[6]

                if mode == 0:
                    try:
                        #addLink(name.encode('utf-8', 'ignore'),url2,sub2,iconimage,fanArt,description.encode('utf-8'),'','','','','','','','','','','','','','','','')
                        addLink(name.encode('utf-8', 'ignore'),url2,sub2,iconimage,fanArt,description.encode('utf-8'),'','','','','','','','','','','','','','','','')
                    except:
                        pass
                elif mode == 11 or mode == 16 or mode == 17 or mode == 18:
                    try:
                        addDir2(str(name).encode('utf-8', 'ignore'),url2,mode,sub2,iconimage,fanArt,description.encode('utf-8'),'','','','','','','','','','','','','','','','',False)
                    except:
                        pass
                elif mode > 0 and mode < 7:
                    try:
                        addDir(name.encode('utf-8', 'ignore'),url2,mode,iconimage,fanArt,description.encode('utf-8'),'','','','','','','','','','','','','','','','')
                    except:
                        pass
                else:
                    try:
                        addDir2(name.encode('utf-8', 'ignore'),url2,mode,sub2,iconimage,fanArt,description.encode('utf-8'),'','','','','','','','','','','','','','','','')
                    except:
                        pass
                xbmcplugin.setContent(addon_handle, 'movies')
                xbmcplugin.endOfDirectory(addon_handle)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Nada Adicionado nos Favoritos')
    except:
        pass


def addFavorite(name,url,fav_mode,subtitle,iconimage,fanart,description):
    favList = []
    if os.path.exists(favorites)==False:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
        favList.append((name,url,fav_mode,subtitle,iconimage,fanart,description))
        a = open(favorites, "w")
        a.write(json.dumps(favList))
        a.close()
        notify('Adicionado aos Favoritos do '+__addonname__)
        #xbmc.executebuiltin("XBMC.Container.Refresh")
    else:
        a = open(favorites).read()
        data = json.loads(a)
        data.append((name,url,fav_mode,subtitle,iconimage,fanart,description))
        b = open(favorites, "w")
        b.write(json.dumps(data))
        b.close()
        notify('Adicionado aos Favoritos do '+__addonname__)
        #xbmc.executebuiltin("XBMC.Container.Refresh")


def rmFavorite(name):
    data = json.loads(open(favorites).read())
    for index in range(len(data)):
        if data[index][0]==name:
            del data[index]
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()
            break
    notify('Removido dos Favoritos do '+__addonname__)
    #xbmc.executebuiltin("XBMC.Container.Refresh")

def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,folder=True):
    if mode == 1 or mode == 24:
        if url > '':
            #u=sys.argv[0]+"?url="+urllib.quote_plus(base64.b64encode(url))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            #u=sys.argv[0]+"?url="+urllib.quote_plus(codecs.encode(base64.b32encode(base64.b16encode(url)), '\x72\x6f\x74\x31\x33'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            #u=sys.argv[0]+"?url="+urllib.quote_plus(base64.b32encode(url.encode('utf-8')))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            u=sys.argv[0]+"?url="+urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8'))))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(5)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    else:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    li=xbmcgui.ListItem(name)
    if folder:
        li.setArt({"icon": "DefaultFolder.png", "thumb": iconimage})
    else:
        li.setArt({"icon": "DefaultVideo.png", "thumb": iconimage})
    if date == '':
        date = None
    else:
        description += '\n\nDate: %s' %date
    li.setInfo('video', { 'title': name, 'plot': description })
    try:
        li.setInfo('video', { 'genre': str(genre) })
    except:
        pass
    try:
        li.setInfo('video', { 'dateadded': str(date) })
    except:
        pass
    try:
        li.setInfo('video', { 'credits': str(credits) })
    except:
        pass
    try:
        li.setInfo('video', { 'year': int(year) })
    except:
        pass
    try:
        li.setInfo('video', { 'year': int(year) })
    except:
        pass
    try:
        li.setInfo('video', { 'director': str(director) })
    except:
        pass
    try:
        li.setInfo('video', { 'writer': str(writer) })
    except:
        pass
    try:
        li.setInfo('video', { 'duration': int(duration) })
    except:
        pass
    try:
        li.setInfo('video', { 'premiered': str(premiered) })
    except:
        pass
    try:
        li.setInfo('video', { 'studio': str(studio) })
    except:
        pass
    try:
        li.setInfo('video', { 'mpaa': str(rate) })
    except:
        pass
    try:
        li.setInfo('video', { 'originaltitle': str(originaltitle) })
    except:
        pass
    try:
        li.setInfo('video', { 'country': str(country) })
    except:
        pass
    try:
        li.setInfo('video', { 'rating': float(rating) })
    except:
        pass
    try:
        li.setInfo('video', { 'userrating': int(userrating) })
    except:
        pass
    try:
        li.setInfo('video', { 'votes': str(votes) })
    except:
        pass
    try:
        li.setRating("imdb", float(rating), int(votes), True)
    except:
        pass
    try:
        li.setInfo('video', { 'aired': str(aired) })
    except:
        pass

    if fanart > '':
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', ''+home+'/fanart.jpg')
    try:
        name_decode = name.decode('utf-8')
    except:
        name_decode = name
    try:
        name_fav = json.dumps(name_decode)
    except:
        name_fav =  name_decode
    try:
        contextMenu = []
        if favoritos == 'true' and  mode !=4 and mode !=7 and mode !=8 and mode !=9 and mode !=10 and mode !=12 and mode !=15:
            if name_fav in FAV:
                contextMenu.append(('Remover dos Favoritos do '+__addonname__,'RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
            else:
                fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8')))), '', urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description), str(mode)))
                contextMenu.append(('Adicionar aos Favoritos do '+__addonname__,'RunPlugin(%s)' %fav_params))
        contextMenu.append(('Informação', 'RunPlugin(%s?mode=19&name=%s&description=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(description))))
        li.addContextMenuItems(contextMenu)
    except:
        pass
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=li, isFolder=folder)

def addDir2(name,url,mode,subtitle,iconimage,fanart,description,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,folder=True):
    if mode == 1:
        if url > '':
            u=sys.argv[0]+"?url="+urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8'))))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(5)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    else:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)+"&subtitle="+urllib.quote_plus(subtitle)+"&description="+urllib.quote_plus(description)
    li=xbmcgui.ListItem(name)
    if folder:
        li.setArt({"icon": "DefaultFolder.png", "thumb": iconimage})
    else:
        li.setArt({"icon": "DefaultVideo.png", "thumb": iconimage})
    if mode == 16 or mode == 17:
        li.setProperty('IsPlayable', 'true')        
    if date == '':
        date = None
    else:
        description += '\n\nDate: %s' %date
    li.setInfo('video', { 'title': name, 'plot': description })
    try:
        li.setInfo('video', { 'genre': str(genre) })
    except:
        pass
    try:
        li.setInfo('video', { 'dateadded': str(date) })
    except:
        pass
    try:
        li.setInfo('video', { 'credits': str(credits) })
    except:
        pass
    try:
        li.setInfo('video', { 'year': int(year) })
    except:
        pass
    try:
        li.setInfo('video', { 'year': int(year) })
    except:
        pass
    try:
        li.setInfo('video', { 'director': str(director) })
    except:
        pass
    try:
        li.setInfo('video', { 'writer': str(writer) })
    except:
        pass
    try:
        li.setInfo('video', { 'duration': int(duration) })
    except:
        pass
    try:
        li.setInfo('video', { 'premiered': str(premiered) })
    except:
        pass
    try:
        li.setInfo('video', { 'studio': str(studio) })
    except:
        pass
    try:
        li.setInfo('video', { 'mpaa': str(rate) })
    except:
        pass
    try:
        li.setInfo('video', { 'originaltitle': str(originaltitle) })
    except:
        pass
    try:
        li.setInfo('video', { 'country': str(country) })
    except:
        pass
    try:
        li.setInfo('video', { 'rating': float(rating) })
    except:
        pass
    try:
        li.setInfo('video', { 'userrating': int(userrating) })
    except:
        pass
    try:
        li.setInfo('video', { 'votes': str(votes) })
    except:
        pass
    try:
        li.setRating("imdb", float(rating), int(votes), True)
    except:
        pass
    try:
        li.setInfo('video', { 'aired': str(aired) })
    except:
        pass
    if fanart > '':
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', ''+home+'/fanart.jpg')
    try:
        name_decode = name.decode('utf-8')
    except:
        name_decode = name
    try:
        name_fav = json.dumps(name_decode)
    except:
        name_fav =  name_decode
    try:
        contextMenu = []
        if favoritos == 'true' and  mode !=4 and mode !=7 and mode !=8 and mode !=9 and mode !=10 and mode !=12 and mode !=15:
            if name_fav in FAV:
                contextMenu.append(('Remover dos Favoritos do '+__addonname__,'RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
            else:
                fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8')))), urllib.quote_plus(base64.b16encode(base64.b64encode(subtitle.encode('utf-8')))), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description), str(mode)))
                contextMenu.append(('Adicionar aos Favoritos do '+__addonname__,'RunPlugin(%s)' %fav_params))
        contextMenu.append(('Informação', 'RunPlugin(%s?mode=19&name=%s&description=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(description))))
        li.addContextMenuItems(contextMenu)
    except:
        pass
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=li, isFolder=folder)

def addLink(name,url,subtitle,iconimage,fanart,description,genre,date,credits,year,director,writer,duration,premiered,studio,rate,originaltitle,country,rating,userrating,votes,aired,folder=False):
    if date == '':
        date = None
    else:
        description += '\n\nDate: %s' %date
    if iconimage > '':
        thumbnail = iconimage
    else:
        thumbnail = 'DefaultVideo.png'
    li=xbmcgui.ListItem(name)
    li.setArt({"icon": "DefaultVideo.png", "thumb": thumbnail})
    if url.startswith("plugin://plugin.video.f4mTester"):
        li.setProperty('IsPlayable', 'false')
    else:
        li.setProperty('IsPlayable', 'true')
    if fanart > '':
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', ''+home+'/fanart.jpg')
    try:
        name_fav = json.dumps(name)
    except:
        name_fav = name
    name2_fav = name
    desc_fav = description
    li.setInfo('video', { 'plot': description })
    try:
        li.setInfo('video', { 'genre': str(genre) })
    except:
        pass
    try:
        li.setInfo('video', { 'dateadded': str(date) })
    except:
        pass
    try:
        li.setInfo('video', { 'credits': str(credits) })
    except:
        pass
    try:
        li.setInfo('video', { 'year': int(year) })
    except:
        pass
    try:
        li.setInfo('video', { 'year': int(year) })
    except:
        pass
    try:
        li.setInfo('video', { 'director': str(director) })
    except:
        pass
    try:
        li.setInfo('video', { 'writer': str(writer) })
    except:
        pass
    try:
        li.setInfo('video', { 'duration': int(duration) })
    except:
        pass
    try:
        li.setInfo('video', { 'premiered': str(premiered) })
    except:
        pass
    try:
        li.setInfo('video', { 'studio': str(studio) })
    except:
        pass
    try:
        li.setInfo('video', { 'mpaa': str(rate) })
    except:
        pass
    try:
        li.setInfo('video', { 'originaltitle': str(originaltitle) })
    except:
        pass
    try:
        li.setInfo('video', { 'country': str(country) })
    except:
        pass
    try:
        li.setInfo('video', { 'rating': float(rating) })
    except:
        pass
    try:
        li.setInfo('video', { 'userrating': int(userrating) })
    except:
        pass
    try:
        li.setInfo('video', { 'votes': str(votes) })
    except:
        pass
    try:
        li.setRating("imdb", float(rating), int(votes), True)
    except:
        pass
    try:
        li.setInfo('video', { 'aired': str(aired) })
    except:
        pass

    if subtitle > '':
        li.setSubtitles([subtitle])
    try:
        name_decode = name.decode('utf-8')
    except:
        name_decode = name
    try:
        name_fav = json.dumps(name_decode)
    except:
        name_fav =  name_decode
    try:
        contextMenu = []
        if favoritos == 'true':
            if name_fav in FAV:
                contextMenu.append(('Remover dos Favoritos do '+__addonname__,'RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
            else:
                fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=0'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8')))), urllib.quote_plus(base64.b16encode(base64.b64encode(subtitle.encode('utf-8')))), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description)))
                contextMenu.append(('Adicionar aos Favoritos do '+__addonname__,'RunPlugin(%s)' %fav_params))
        contextMenu.append(('Informação', 'RunPlugin(%s?mode=19&name=%s&description=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(description))))
        li.addContextMenuItems(contextMenu)
    except:
        pass
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=folder)

def parental_password():
    try:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
        #Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
        #arquivo = os.path.join(Path, "password.txt")
        arquivo = os.path.join(addon_data_path, "password.txt")
        exists = os.path.isfile(arquivo)
        if exists == False:
            password = '0069'
            p_encoded = base64.b64encode(password.encode()).decode('utf-8')
            p_file = open(arquivo,'w')
            p_file.write(p_encoded)
            p_file.close()
    except:
        pass

def check_addon():
    try:
        check_file = xbmcvfs.translatePath(home+'/check.txt')
        exists = os.path.isfile(check_file)
        check_addon = addon.getSetting('check_addon')
        #check_file = 'check.txt'
        if exists == True:
            #print('existe')
            fcheck = open(check_file,'r+')
            elementum = addon.getSetting('elementum')
            youtube = addon.getSetting('youtube')
            if fcheck and fcheck.read() == '1' and check_addon == 'true':
                #print('valor 1')
                fcheck.close()
                link = getRequest2('https://raw.githubusercontent.com/zoreu/zoreu.github.io/master/kodi/verificar_addons_matrix.txt','').replace('\n','').replace('\r','')
                match = re.compile('addon_name="(.+?)".+?ddon_id="(.+?)".+?ir="(.+?)".+?rl_zip="(.+?)".+?escription="(.+?)"').findall(link)
                for addon_name,addon_id,directory,url_zip,description in match:
                    if addon_id == 'plugin.video.elementum' and elementum == 'false':
                        pass
                    elif addon_id == 'script.module.six' and youtube == 'false':
                        pass
                    elif addon_id == 'plugin.video.youtube' and youtube == 'false':
                        pass
                    else:
                        existe = xbmcvfs.translatePath(directory)
                        #print('Path dir:'+existe)
                        if os.path.exists(existe)==False:
                            install_wizard(addon_name,addon_id,url_zip,directory,description)
                            if addon_id == 'plugin.video.elementum':
                                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATIVAR O ELEMENTUM')
                        else:
                            pass
        elif check_addon == 'true':
            #print('nao existe')
            fcheck = open(check_file,'w')
            fcheck.write('1')
            fcheck.close()
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA VERIFICAR COMPLEMENTOS')
    except:
        pass


def install_wizard(name,addon_id,url,directory,description):
    try:
        import downloader
        import extract
        import ntpath
        path = xbmcvfs.translatePath(os.path.join('special://','home/','addons', 'packages'))
        filename = ntpath.basename(url)
        dp = xbmcgui.DialogProgress()
        dp.create("Install addons","Baixando "+name+", por favor aguarde....")
        lib=os.path.join(path, filename)
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, name, lib)
        addonfolder = xbmcvfs.translatePath(os.path.join('special://','home/','addons'))
        xbmc.sleep(100)
        dp.update(0,"Instalando "+name+", Por Favor Espere")
        try:
            xbmc.executebuiltin("Extract("+lib+","+addonfolder+")")
        except:
            try:
                extract.all(lib,addonfolder,dp)
            except:
                pass
        #############
        #time.sleep(2)
        xbmc.sleep(100)
        xbmc.executebuiltin("UpdateLocalAddons()")
        notify(name+' Instalado com Sucesso!')
        import database
        database.enable_addon(addon_id)
        if addon_id == 'plugin.video.elementum':
            database.enable_addon('repository.elementum')
        #xbmc.executebuiltin("XBMC.Container.Refresh()")
        xbmc.executebuiltin("Container.Update()")
        #xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]',''+name+' instalado, feche e abra o Kodi novamente')
    except:
        notify('Erro ao baixar o complemento')


def time_convert(timestamp):
    try:
        if timestamp > '':
            dt_object = datetime.fromtimestamp(int(timestamp))
            time_br = dt_object.strftime('%d/%m/%Y às %H:%M:%S')
            return str(time_br)
        else:
            valor = ''
            return valor
    except:
        valor = ''
        return valor

def info_vip():
    username_vip = addon.getSetting('username')
    password_vip = addon.getSetting('password')
    if username_vip > '' and password_vip > '':
        try:
            url_info = url_server_vip.replace('/get.php', '')+'/player_api.php?username=%s&password=%s'%(username_vip,password_vip)
            dados_vip = getRequest2(url_info, '')
            filtrar_info = re.compile('"status":"(.+?)".+?"exp_date":"(.+?)".+?"is_trial":"(.+?)".+?"created_at":"(.+?)".+?max_connections":"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(dados_vip)
            if filtrar_info !=[]:
                status = str(filtrar_info[0][0])
                exp_date = str(filtrar_info[0][1])
                trial = str(filtrar_info[0][2])
                created = str(filtrar_info[0][3])
                max_connection = str(filtrar_info[0][4])
                #status do usuario
                if status > '' and status == 'Active':
                    status_result = 'Ativo'
                else:
                    status_result = 'Expirado'
                #Validade do vip
                if exp_date > '':
                    expires = time_convert(str(exp_date))
                else:
                    expires = ''
                #usuario de teste
                if trial > '' and trial == '0':
                    vip_trial = 'Não'
                else:
                    vip_trial = 'Sim'
                #criado
                if created > '':
                    created_time = time_convert(str(created))
                else:
                    created_time = ''
                #limite de conexoes
                if max_connection > '':
                    limite_conexao = max_connection
                else:
                    limite_conexao = ''

                try:
                    xbmcaddon.Addon().setSetting("status_vip", status_result)
                    xbmcaddon.Addon().setSetting("created_at", created_time)
                    xbmcaddon.Addon().setSetting("exp_date", expires)
                    xbmcaddon.Addon().setSetting("is_trial", vip_trial)
                    xbmcaddon.Addon().setSetting("max_connection", limite_conexao)
                except:
                    pass
        except:
            try:
                xbmcaddon.Addon().setSetting("status_vip", '')
                xbmcaddon.Addon().setSetting("created_at", '')
                xbmcaddon.Addon().setSetting("exp_date", '')
                xbmcaddon.Addon().setSetting("is_trial", '')
                xbmcaddon.Addon().setSetting("max_connection", '')
            except:
                pass

def vip():
    username_vip = addon.getSetting('username')
    password_vip = addon.getSetting('password')
    #tipo_servidor = addon.getSetting('servidor')
    vip_menu = addon.getSetting('exibirvip')
    saida_transmissao = addon.getSetting('saida')
    if username_vip > '' and password_vip > '':
        info_vip()
    if int(saida_transmissao) == 1:
        saida_canal = 'm3u8'
    else:
        saida_canal = 'ts'
    if vip_menu == 'true':
        if username_vip > '' and password_vip > '':
            url = ''+url_server_vip+'?username=%s&password=%s&type=m3u_plus&output=%s'%(username_vip,password_vip,saida_canal)
            #addDir(name,url,mode,iconimage,fanart,description)
            addDir(titulo_vip,url,1,thumbnail_vip,fanart_vip,vip_descricao,'','','','','','','','','','','','','','','','')
        else:
            #if tipo_servidor=='Desativado':
            #addDir(name,url,mode,iconimage,fanart,description)
            addDir(titulo_vip,'',9,thumbnail_vip,fanart_vip,vip_descricao,'','','','','','','','','','','','','','','','')

def Pesquisa():
    vq = get_search_string(heading="Digite algo para pesquisar")
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    addDir('[COLOR white][B]PESQUISAR NOVAMENTE...[/B][/COLOR]','',7,thumb_pesquisar,fanart_pesquisar,desc_pesquisa,'','','','','','','','','','','','','','','','')
    try:
        getData(url_pesquisa+'?pesquisar='+title, '')
    except:
        pass
    xbmcplugin.endOfDirectory(addon_handle)

def SetView(name):
    if name == 'Wall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(500)')
        except:
            pass
    if name == 'List':
        try:
            xbmc.executebuiltin('Container.SetViewMode(50)')
        except:
            pass
    if name == 'Poster':
        try:
            xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
            pass
    if name == 'Shift':
        try:
            xbmc.executebuiltin('Container.SetViewMode(53)')
        except:
            pass
    if name == 'InfoWall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(54)')
        except:
            pass
    if name == 'WideList':
        try:
            xbmc.executebuiltin('Container.SetViewMode(55)')
        except:
            pass
    if name == 'Fanart':
        try:
            xbmc.executebuiltin('Container.SetViewMode(502)')
        except:
            pass

def entrar():
    username = addon.getSetting('username')
    password = addon.getSetting('password')
    if not username and not password:
        xbmcaddon.Addon().openSettings()
    else:
        addDir('[B]VENCIMENTO DO LOGIN[/B]','',23,__icon__,'',title_descricao,'','','','','','','','','','','','','','','','')
        getData(url_principal_vip, '')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

def SKindex():
    #addDir(name,url,mode,iconimage,fanart,description)
    addDir(title_menu,url_title,1,__icon__,'',title_descricao,'','','','','','','','','','','','','','','','')
    if favoritos == 'true':
        addDir(menu_favoritos,'',15,thumb_favoritos,'',desc_favoritos,'','','','','','','','','','','','','','','','')
    addDir('[B]ENTRADA VIP[/B]','',22,icone_vip,'',title_descricao,'','','','','','','','','','','','','','','','')
    addDir('[B]ENTRADA FREE[/B]',url_principal_free,24,icone_free,'',title_descricao,'','','','','','','','','','','','','','','','')
    addDir('[B]CONTRIBUIÇÃO[/B]','',26,contribuicao_icon,'','Faça uma contribuição e ajude esse addon','','','','','','','','','','','','','','','','')
    addDir('[B]CONFIGURAÇÕES[/B]','',4,__icon__,'',desc_configuracoes,'','','','','','','','','','','','','','','','')
    xbmcplugin.endOfDirectory(addon_handle)

class contribuicao(xbmcgui.WindowDialog):
    def __init__(self):
        self.image = xbmcgui.ControlImage(440, 120, 400, 400, pix_icon)
        self.text = xbmcgui.ControlLabel(x=150,y=548,width=1100,height=25,label='[B]SE ESSE ADD-ON LHE AGRADA, FAÇA UMA CONTRIBUIÇÃO VIA PIX ACIMA E GANHE ACESSO VIP[/B]',textColor='white')
        self.text2 = xbmcgui.ControlLabel(x=218,y=579,width=1100,height=25,label='[B]NÃO ESQUEÇA DE ENVIAR COMPROVANTE PELO WHATSAPP +55 48 9194-1409[/B]',textColor='white')
        self.text3 = xbmcgui.ControlLabel(x=495,y=610,width=1000,height=25,label='[B]PRESSIONE VOLTAR PARA SAIR[/B]',textColor='white')
        self.addControl(self.image)
        self.addControl(self.text)
        self.addControl(self.text2)
        self.addControl(self.text3)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
subtitle=None

try:
    url=urllib.unquote(params["url"])
    #url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
    pass

try:
    #name=urllib.unquote(params["name"])
    name=urllib.unquote_plus(params["name"])
except:
    pass

try:
    #iconimage=urllib.unquote(params["iconimage"])
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass

try:
    mode=int(params["mode"])
except:
    pass

try:
    #fanart=urllib.unquote(params["fanart"])
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass

try:
    #description=urllib.unquote(params["description"])
    description=urllib.unquote_plus(params["description"])
except:
    pass

try:
    subtitle=urllib.unquote_plus(params["subtitle"])
except:
    pass

try:
    fav_mode=int(params["fav_mode"])
except:
    pass

if mode==None:
    xbmcplugin.setContent(addon_handle, 'movies')
    check_addon()
    parental_password()
    SKindex()
    SetView('List')

elif mode==1:
    #condicao = check_painel()
    #url = base64.b16decode(base64.b32decode(codecs.decode(url, '\x72\x6f\x74\x31\x33')))
    #url = base64.b64decode(url)
    url = base64.b64decode(base64.b16decode(url))
    try:
        url = url.decode('utf-8')
    except:
        pass
    getData(url, fanart)
    xbmcplugin.endOfDirectory(addon_handle,cacheToDisc=False)

#elif mode==2:
#    getChannelItems(name,url,fanart)
#    xbmcplugin.endOfDirectory(addon_handle)

#elif mode==3:
#    getSubChannelItems(name,url,fanart)
#    xbmcplugin.endOfDirectory(addon_handle)


#Configurações
elif mode==4:
    xbmcaddon.Addon().openSettings()
    #xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATUALIZAR AS CONFIGURAÇÕES')
    #xbmc.executebuiltin("XBMC.Container.Refresh()")

#Link Vazio
elif mode==5:
    xbmc.executebuiltin("Container.Refresh()")

elif mode==6:
    ytbmode = addon.getSetting('ytbmode')
    if int(ytbmode) == 0:
        pluginquerybyJSON(url)
    elif int(ytbmode) == 1:
        getPlaylistLinksYoutube(url)
    else:
        youtube(url)
    xbmcplugin.endOfDirectory(addon_handle)

#elif mode==7:
#    Pesquisa()

elif mode==9:
    #xbmcgui.Dialog().ok(titulo_vip, vip_dialogo)
    xbmcaddon.Addon().openSettings()
    #xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATUALIZAR AS CONFIGURAÇÕES')
    #xbmc.executebuiltin("XBMC.Container.Refresh()")

elif mode==10:
    adult(name, url, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==11:
    playlist(name, url, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)

#elif mode==12:
#    CheckUpdate(True)
#    xbmc.executebuiltin("XBMC.Container.Refresh()")

elif mode==13:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,fav_mode,subtitle,iconimage,fanart,description)

elif mode==14:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)

elif mode==15:
    #xbmcplugin.setContent(addon_handle, 'movies')
    getFavorites()
    #xbmcplugin.endOfDirectory(addon_handle)

elif mode==16:
    individual_player(name, url, iconimage, description, subtitle)
    #xbmcplugin.endOfDirectory(addon_handle)

elif mode==17:
    youtube_live_player(name, url, iconimage, description, subtitle)
    #xbmcplugin.endOfDirectory(addon_handle)

elif mode==18:
    m3u8_player(name, url, iconimage, description, subtitle)
    #xbmcplugin.endOfDirectory(addon_handle)

elif mode==19:
    xbmcgui.Dialog().textviewer('Informação: '+name, description)

elif mode==21:
    try:
        url = base64.b16decode(base64.b32decode(url))
    except:
        pass
    try:
        url = url.decode('utf-8')
    except:
        pass
    if re.search("Adult",name,re.IGNORECASE) or re.search("A Casa das Brasileirinhas",name,re.IGNORECASE):
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        arquivo = os.path.join(addon_data_path, "password.txt")
        keyboard = xbmcaddon.Addon().getSetting("keyboard")
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            get_m3u8_2(name,url)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
            xbmcplugin.endOfDirectory(addon_handle)
    else:
        get_m3u8_2(name,url)

elif mode==22:
    entrar()

elif mode==23:
    vencimento()

elif mode==24:
    # abrir links free
    url = base64.b64decode(base64.b16decode(url))
    try:
        url = url.decode('utf-8')
    except:
        pass
    #get data free
    getData_free(url, fanart)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==25:
    try:
        url = base64.b16decode(base64.b32decode(url))
    except:
        pass
    try:
        url = url.decode('utf-8')
    except:
        pass
    if re.search("Adult",name,re.IGNORECASE) or re.search("A Casa das Brasileirinhas",name,re.IGNORECASE):
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        arquivo = os.path.join(addon_data_path, "password.txt")
        keyboard = xbmcaddon.Addon().getSetting("keyboard")
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            get_m3u8_2_free(name,url)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
            xbmcplugin.endOfDirectory(addon_handle)
    else:
        get_m3u8_2_free(name,url)

elif mode==26:
    dialog_contribuicao = contribuicao()
    dialog_contribuicao.doModal()
