from re import search
from .models import newPage
from django.shortcuts import redirect, render,HttpResponseRedirect
import markdown2
from . import util
from thefuzz import fuzz
from random import choice
from django import forms

class newpage(forms.ModelForm):
    class Meta:
        model=newPage
        fields="__all__"
        widgets={
            'content': forms.Textarea(attrs={'rows':25,'cols':100}),
            'title':forms.TextInput(attrs={'size':'100'})
        }

def index(request):
    if request.GET.get('q'):
        listentries=util.list_entries()
        query=request.GET['q']
        sublist=[]
        for entry in listentries:
            subratio= fuzz.partial_ratio(query.lower(),entry.lower())
            ratio= fuzz.ratio(query.lower(),entry.lower())
            
            if ratio==100:
                ser= util.get_entry(query)
                html= markdown2.markdown(ser)
                return render(request, "encyclopedia/entry.html", {
                    "title":query,
                    "content":html
                })
            
            else:
                if subratio==100:
                    sublist.append(entry)

        if sublist:
            return render(request, "encyclopedia/result.html", {
                "query":query,
                "results":sublist })
        else:
            return render(request, "encyclopedia/notfound.html", {
                "message": f"Error: wiki page titled '{query}' not found"
                })


    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
    })

def create(request):
    if request.method =="POST":
        form=newpage(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            sear=util.get_entry(title)
            if sear:
                return render(request, "encyclopedia/notfound.html", {
            "message": f"Error: wiki page titled '{title}' already exit"
        })
            else:
                util.save_entry(title,content)
                ser= util.get_entry(title)
                if ser:
                    html= markdown2.markdown(ser)
                    return render(request, "encyclopedia/entry.html", {
                    "title":title,
                    "content":html
        })
    form=newpage()        
    return render(request, "encyclopedia/create.html", {
        "form":form
    })

def random(request):
    name= choice(util.list_entries())
    rand=util.get_entry(name)
    html= markdown2.markdown(rand)
    return render(request, "encyclopedia/entry.html", {
        "title":name,
        "content":html
                })

def topic(request, title):
    sear= util.get_entry(title)
    if sear:
        html= markdown2.markdown(sear)
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":html
        })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "message": f"Error: wiki page titled '{title}' not found"
        })

def editpage(request, title):
    con=util.get_entry(title)
    form=newpage(initial={'title':title ,'content':con})
    return render(request, "encyclopedia/edit.html", {
            "title":title,
            "form":form
    })

def savepage(request):
    if request.method =="POST":
        form=newpage(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            util.save_entry(title,content)
    form=newpage()        
    sear= util.get_entry(title)
    if sear:
        html= markdown2.markdown(sear)
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":html
        })