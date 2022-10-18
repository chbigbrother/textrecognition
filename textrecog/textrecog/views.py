#-*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.http import JsonResponse
from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import smart_str
import datetime, json
from datetime import timedelta
import os
import datetime, json, csv, math

# Create your views here.
def home(request):

    return render(request, 'main/index.html')



def draw_text(request):
    filename_list = []
    for f_name in os.listdir('.'):
        if f_name.startswith('data_collection'):
            filename_list.append((f_name, os.path.getctime(f"{''}{f_name}")))
    sorted_file_list = sorted(filename_list, key=lambda x: x[1], reverse=True)
    if len(sorted_file_list) == 0:
        cnt = 1
    else:
        recent_file = sorted_file_list[0]
        recent_file_name = recent_file[0]
        recent_file_name_cnt = recent_file_name[:-4]
        cnt = int(recent_file_name_cnt[int(recent_file_name_cnt.rfind('_'))+1:]) + 1

    if request.GET['type'] == 'label':
        f = open('./data_labeling_' + str(cnt) + '.txt', 'w')
        # for i in request.GET['input_text']:
        for i in request.GET['input_text'].split(' '):
            print(i)
            if i == ' ':
                continue;
            f.write(i + '\n')
        f.close()
        f = open('./data_collection_' + str(cnt) + '.txt', 'w')
        f.close()
    elif request.GET['type'] == 'append':
        add_text_collection(request.GET['list_cnt'])
        add_text_label(request.GET['input_len'], request.GET['stroke_cnt'].replace('[', '').replace(']', '').replace(',', ' '))
    else:
        if len(sorted_file_list) == 0:
            recent_file_name = "data_collection_1.txt"
            f = open(recent_file_name, 'w')
            f.write(request.GET['input_text'] + '\n')
        else:
            f = open(recent_file_name, 'a')
            f.write(request.GET['input_text'] +'\n')
    f.close()

    return JsonResponse({"message": 'success'})

def add_text_collection(list_cnt):
    filename_list = []
    for f_name in os.listdir('.'):
        if f_name.startswith('data_collection'):
            filename_list.append((f_name, os.path.getctime(f"{''}{f_name}")))
    sorted_file_list = sorted(filename_list, key=lambda x: x[1], reverse=True)
    recent_file = sorted_file_list[0]
    recent_file_name = recent_file[0]
    new_text_content = ''
    with open(recent_file_name, 'r') as r:
        lines = r.readlines()
        for i, l in enumerate(lines):
            if l.find("value") > 0:
                new_string = list_cnt
            else:
                new_string = l.strip()

            if new_string:
                new_text_content += new_string + '\n'
            else:
                new_text_content += '\n'

    with open(recent_file_name, 'r+') as r:
        r.truncate()

    f = open(recent_file_name, 'a')
    f.truncate()
    f.write(new_text_content)
    f.close()

    return JsonResponse({"message": 'success'})

def add_text_label(input_len, label_list):
    filename_list = []
    for f_name in os.listdir('.'):
        if f_name.startswith('data_labeling'):
            filename_list.append((f_name, os.path.getctime(f"{''}{f_name}")))
    sorted_file_list = sorted(filename_list, key=lambda x: x[1], reverse=True)
    recent_file = sorted_file_list[0]
    recent_file_name = recent_file[0]

    new_text_content = ''
    with open(recent_file_name, 'r') as r:
        lines = r.readlines()
        for i, l in enumerate(lines):
            if i == int(input_len):
                new_string = label_list + " " + l # label_list
            else:
                new_string = l

            if new_string:
                new_text_content += new_string
            else:
                new_text_content += '\n'

    with open(recent_file_name, 'r+') as r:
        r.truncate()

    f = open(recent_file_name, 'a')
    f.truncate()
    f.write(new_text_content)
    f.close()


    return JsonResponse({"message": 'success'})