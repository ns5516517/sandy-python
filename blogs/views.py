from django.shortcuts import render


# Create your views here.
def getAllBlogs(req):
    return render(req, "blogs.html")


def getOneBlog(req):
    return render(req, "blog_detail.html")
