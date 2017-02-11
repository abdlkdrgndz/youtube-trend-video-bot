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
        limits, info_list = 7, []
        bs = BeautifulSoup(content, 'html.parser')
        avt_start   = bs.find_all('a', 'yt-uix-tile-link', limit=limits)                                # avt = all video titles starting attract
        acn_start   = bs.find_all('a', 'g-hovercard', limit=limits)                                   # acn = all channel name starting attract
        av          = bs.find_all('ul', 'yt-lockup-meta-info', limit=limits)                            # av =  all views and uploaded time select starting
        img         = bs.find_all('img', attrs={'width' : 196, 'height' : 110}, limit=limits)                               # img = all video images attract
        link        = bs.find_all('a', 'yt-uix-tile-link', limit=limits)                                # link = all video links attract

        #zip details append new list
        avt, acn, imgs, links = [], [], [], []
        for x in avt_start:
            avt.append(x.get_text())

        for y in acn_start:
            acn.append(y.get_text())

        for z in img:
            imgs.append(z.get('src'))

        for q in link:
            links.append(q.get('href'))


        music_details = zip(avt, acn, av, links, imgs)  #implode all datas

        # Html render.
        final_time = datetime.datetime.now().strftime('%H:%M:%S')
        return render_to_response("index.html", {'music_details': music_details, 'start_time' : start_time, 'final_time' : final_time }, content_type=RequestContext(request))

    else:
        return HttpResponse('Sayfaya bağlantı sağlanamadı.')
