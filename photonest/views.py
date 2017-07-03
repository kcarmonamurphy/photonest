from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from subprocess import check_output

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def folder(request):
    
    return HttpResponse("view image");

def photo(request):
    
    return HttpResponse("view image");

def metadata(request, filename):
    try:
        file = open("collection/" + filename, 'r')
        output = check_output(["exiftool", "-json", "collection/" + filename])
        context = {'filename': filename, 'output': output}
    except:
        raise Http404("File not found")


    return render(request, 'metadata.html', context)

