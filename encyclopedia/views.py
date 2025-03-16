from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

from . import util

import markdown2

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
