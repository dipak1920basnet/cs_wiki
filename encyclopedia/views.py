from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

from . import util

import markdown2
from django import forms
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def call(request, name):
    content = util.get_entry(name)
    if content == None:
        return render(request, "encyclopedia/error.html",
                      {
                          "message":f" requested page {name} was not found. "
                      })
    
    return render(request, "encyclopedia/entry.html",{
        "title":name,
        "entrie":markdown2.Markdown().convert(content)
    })

def random_entry(request):
    content_list = util.list_entries()
    m = random.choice(content_list)
    return redirect('encyclopedia:call',name=m)

def search(request):
    if request.method == "POST":
        available_entry = util.list_entries()  # Get the list of entries
        record_to_show = []
        task = request.POST.get("q","") # Get the searched query
        for i in available_entry:
            if (task.lower()).capitalize() == (i.lower()).capitalize():
                return redirect('encyclopedia:call',(i.lower()).capitalize())  #Go to the pages if the query matches
            if task.lower() in i.lower().capitalize():
                record_to_show.append(i) # Append if it is available
            elif task.lower().capitalize() in i.lower().capitalize():
                record_to_show.append(i)
    if len(record_to_show) == 0:
            return redirect('encyclopedia:call',task)
    return render(request, "encyclopedia/index.html", {
        "entries": record_to_show
    }) 


class AddContent(forms.Form):
    ## Adding a title to the page
    new_title = forms.CharField(label="Enter Title:",widget=forms.Textarea(attrs = {
            'rows':'2%',
            'cols':'200%',
            'style': 'width: auto; height: auto;',
            'placeholder':'Enter your title here...',
            'class':"form-control",
        }))
    
    ## Adding a content to the page
    new_content = forms.CharField(
        widget=forms.Textarea(attrs = {
            'rows':15,
            'cols':'200%',
            'style': 'width: auto; height: auto;',
            'placeholder':'Enter your description here...',
            'class':"form-control",
        }),
        label="Add Content:")
    
def create_content(request):
    if request.method == "POST":
        # Take in the data the user submitted:
        form = AddContent(request.POST)

        if form.is_valid():
            new_title = form.cleaned_data["new_title"]  ## Get the title
            new_content = form.cleaned_data["new_content"]  ## Get the content
            if new_title in util.list_entries():
                return render(request, "encyclopedia/error.html",
                      {
                          "message":f" Requested page {new_title} is already available. "
                      })
            else:
                util.save_entry(new_title,new_content)
                return redirect('encyclopedia:call',new_title)

    return render(request, "encyclopedia/add.html",{
        "form":AddContent()
    })

def edit_page(request,name):
    content = util.get_entry(name)
    return render(request, f"encyclopedia/edit.html",
                  {
                      "title":name,
                      "content":content
                  })

def go_edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        title=(title.lower()).capitalize()
        return redirect('encyclopedia:edit',title)
    
def save_edit(request):
    if request.method == "POST":
        title = (request.POST.get("title")).lower().capitalize()
        content = request.POST.get("content")
        util.save_entry(title, content)
    return redirect('encyclopedia:call',name=title)
