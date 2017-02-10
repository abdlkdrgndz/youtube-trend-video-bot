# -*- coding: utf-8 -*-
# Author :  Abdulkadir Gündüz
import re

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from bs4 import BeautifulSoup
from django.template import RequestContext
import  requests
import datetime

# Create your views here.


def index(request):
    start_time = datetime.datetime.now().strftime('%H:%M:%S')
    connect = requests.get('https://www.youtube.com/feed/trending')
    if connect:
        content = connect.text
        limits, info_list = 4, []
        bs = BeautifulSoup(content, 'html.parser')
        avt_start   = bs.find_all('a', 'yt-uix-tile-link', limit=limits)                                # avt = all video titles starting attract
        acn_start   = bs.find_all('a', 'g-hovercard', limit=(limits))                                   # acn = all channel name starting attract
        av          = bs.find_all('ul', 'yt-lockup-meta-info', limit=limits)                            # av =  all views and uploaded time select starting
        img         = bs.select('span.yt-thumb-simple img', limit=limits)                               # img = all video images attract
        link        = bs.find_all('a', 'yt-uix-tile-link', limit=limits)                                # link = all video links attract

        #music details for dictionary. This dictionary music infos saving. start.
        music_details = {'music_info' : [
                               [],[],[],[],[],
                            ]
                         }
        # end.
        #for a in range(limits):
            #music_details['music_info'].append(info_list)

        #all video titles append music_details list
        number= 0
        for x,y,z,t,q in zip(avt_start, acn_start, av, img, link):
            number += 1
            music_details['music_info'][number].append(x.get('title'))
            music_details['music_info'][number].append(y.get_text())
            music_details['music_info'][number].append(z.get_text()[10:])
            music_details['music_info'][number].append(z.get_text()[:10])
            music_details['music_info'][number].append(t.get('src'))
            music_details['music_info'][number].append(q.get('href'))

        merhaba  = "Ben yazılım geliştirici Emre Sarıdiken"


        # Html render.
        final_time = datetime.datetime.now().strftime('%H:%M:%S')
        return render_to_response("index.html", {'music_details': music_details, 'start_time' : start_time, 'final_time' : final_time }, content_type=RequestContext(request))

    else:
        return HttpResponse('Sayfaya bağlantı sağlanamadı.')
