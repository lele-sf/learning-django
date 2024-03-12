# Learning Django

## What is Django?
Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel.

### How to start a new project

- Run the following command:

```bash
$ django-admin startproject <project_name>
```

- This will create a new folder with the name of the project and inside it will have the following files:

```bash
project/
    manage.py
    project/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

1. manage.py: This is a command-line utility that lets you interact with your Django project in various ways. You can use it to create database tables, run development servers, create superusers for the admin interface, and more.

2. The inner project/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. project.urls).

3. settings.py: This file contains all the configuration of your project. It’s where you’ll define which database to use, where Django should look for static files, and more.

4. urls.py: This file is where you define the URL patterns for your Django project. URL patterns determine how URLs are mapped to views. The urls.py file can include patterns directly or include patterns from other apps. It essentially serves as the routing mechanism for your project. When a user requests a page from your website, Django matches the requested URL to a view function. The view function returns an HTTP response, which is then displayed to the user.

5. asgi.py (Asynchronous Server Gateway Interface): This file is used to deploy your Django application with an ASGI server. ASGI is an interface between web servers and Python web applications, designed to handle asynchronous operations. It allows Django to handle long-lived connections, such as WebSockets. This file is used when deploying your project with servers like Daphne or Uvicorn. If you’re not using an ASGI server, you won’t need this file.

6. wsgi.py (Web Server Gateway Interface): Similar to asgi.py, this file is used for deploying your Django application with a WSGI server. WSGI is a standard interface between web servers and Python web applications. It's the traditional way of deploying Django applications, and it's used with servers like Gunicorn. The wsgi.py file provides the entry point for WSGI servers to run your application. If you’re not using a WSGI server, you won’t need this file.

### Django URLs

In Django, the urlpatterns list in the urls.py file is where you define the URL patterns for your application. Each URL pattern is associated with a specific view that should handle the corresponding HTTP request.

``` python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

`path()` function: is used to define URL patterns or routes that your application will respond to. The path itself is a string representing the URL pattern you want to match. It specifies the part of the URL after the domain name. And it takes four arguments, two required: route and view, and two optional: kwargs, and name.

- path() argument: `route` - is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in urlpatterns and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches. In this case, the route is the part of the URL after the domain name. It matches a string that contains polls/ followed by a string that doesn’t contain a slash (e.g. “polls/34/”).

- path() argument: `view` - when Django finds a matching pattern, it calls the specified view function with an HttpRequest object as the first argument and any “captured” values from the route as keyword arguments. In this case, the `include()` function is used to include patterns from another URL configuration ("polls.urls" module).
    * `include()` function - is used to include other URL patterns. It is commonly used to organize URL patterns by splitting them into separate files or modules. It takes a string argument that contains the module where the URL patterns are defined. In this case, the module is "polls.urls". 

- path() argument: `kwargs` - allows you to pass additional keyword arguments to the view function. These can be used to provide extra context or configuration to the view. In this case, no kwargs are passed. 

- path() argument: `name` - allows you to assign a unique name to the URL pattern. This name can be used in templates or other parts of your code to refer to this specific URL, making it easier to maintain and change URLs in the future. In this case, no name is specified. But if you want to name this URL, you can do so by adding the name argument: `path("polls/", include("polls.urls"), name="polls_url")`.

### Django Models

A model is the single, definitive source of truth about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. The goal is to define your data model in one place and automatically derive things from it. Each model class corresponds to a database table, and each attribute of the class represents a field in the table.
    
``` python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publish_date = models.DateField()
    rating = models.IntegerField()
```

- `Author` and `Book` are subclasses of `django.db.models.Model`. Each model class represents a database table.
- Attributes like `name`, `birth_date`, `title`, `author`, `publish_date`, and `rating` are fields of the database table. Each field is represented by an instance of a Field class. For example, `name` is represented by `CharField`, `birth_date` is represented by `DateField`, and so on.
- `ForeignKey` establishes a many-to-one relationship between `Book` and `Author`. It indicates that each book is associated with exactly one author, but an author can have multiple books. The `on_delete=models.CASCADE` argument tells Django to delete the book if its author is deleted.

`makemigrations` command: when you create, update, or delete a model, you need to tell Django to update the database schema by running the `python manage.py makemigrations` command. This command compares the current state of the models in your application with the migration files, which are kept in the migrations directory inside each application. It then writes a new migration file if there are changes that need to be made to keep the models in sync with the database.

`migrate` command: to apply the migrations and create the database tables, you need to run the `python manage.py migrate` command. This command runs all the migrations that haven’t been applied yet and records them in the migrations table of the database. Django tracks which migrations have been applied using a special table in the database called django_migrations. Each time you run migrate, Django creates a new row in the table. It records the migration’s name and the date it was applied.

### Django ORM and QuerySets

Django `ORM` (Object-Relational Mapping) is a powerful tool that allows developers to interact with databases using high-level Python objects instead of directly writing SQL queries. It abstracts away the complexity of database interactions and provides a Pythonic interface for working with data. 

`QuerySets` are used to retrieve data from a database. A QuerySet is a collection of database queries that can be used to filter and retrieve data from the database. It allows you to read data from the database, filter it, order it, and more. 

`Django Shell` is a Python shell that has Django preloaded. It allows you to interact with your Django application and database using Python code. You can use it to test your models, run queries, and perform other tasks. To start the Django shell, run the `python manage.py shell` command.

Consider the following model:

``` python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```	

- Retrieving Data with QuerySets:

``` python
# Import the model
>>> from mysite.models import Post

# Retrieve all posts
>>> all_posts = Post.objects.all()

# Retrieve a single post by its primary key
>>> post = Post.objects.get(pk=1)

# Retrieve a subset of posts using filters
>>> published_posts = Post.objects.filter(published=True)
>>> title_contains_word_posts = Post.objects.filter(title__contains="word")

# Retrieve a subset of posts using multiple filters
>>> published_and_title_contains_word_posts = Post.objects.filter(published=True, title__contains="word")

# Order the posts by a specific field
>>> ordered_posts = Post.objects.order_by("created_at")

# Exclude certain posts from the queryset (e.g., unpublished posts)
>>> published_posts = Post.objects.exclude(published=False)
```	

- Creating, Updating, and Deleting Data with QuerySets:

``` python
# Import the model
>>> from mysite.models import Post

# Create a new post
>>> new_post = Post(title="New Post", content="This is a new post.", published=True)
>>> new_post.save()

# Update an existing post
>>> post = Post.objects.get(pk=1)
>>> post.title = "Updated Title"
>>> post.save()

# Delete an existing post
>>> post = Post.objects.filter(title__startswith="New")
>>> post.delete()
```

### Django Admin

Django comes with a built-in admin interface that can be used to perform CRUD (Create, Read, Update, Delete) operations on the models in your application. The admin interface is a powerful tool that allows you to manage your application’s data without writing any code. It’s a great way to quickly prototype and manage your application’s data.

To use the admin interface, you need to create an admin user and register your models with the admin interface. You can run the `python manage.py createsuperuser` command to create an admin user. This command prompts you to enter a username, email address, and password for the admin user.

Once you've created an admin user, you can start the development server using the `python manage.py runserver` command. Then, you can access the admin interface by navigating to `http://localhost:8000/admin` in your web browser. You'll be prompted to log in using the admin user credentials you created earlier.

To display your models in the admin interface, you need to register them. This is done in the `admin.py` file in your app directory. Here's an example of how to register a model:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

### Django Views

A `view` is a Python function or class that takes a web request and returns a web response. It’s the heart of your web application and is responsible for processing the request, fetching data from the database, and returning an HTML page or other content. Views are the bridge between the data in your database and the presentation of that data to the user. 

When a user makes a request to your web application, Django uses the URL patterns in your `urls.py` file to determine which view to call. The view processes the request and returns an HTTP response, which is then displayed to the user.

Here’s how the request and URL patterns work together:

```python	
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('greet/', views.greet),
]

# views.py
from django.http import HttpResponse

def greet(request):
    return HttpResponse("Hello, world!")
```

In this example, when a user makes a request to `http://yourwebsite.com/greet/`, Django will match the `greet/` pattern in the URL to the `greet` view function. The view function processes the request and returns an HTTP response with the text "Hello, world!". This response is then displayed to the user.

### Django Templates

A `template` is an HTML file that contains placeholders for dynamic data. It’s used to generate the HTML content that’s returned to the user when they make a request to your web application. Templates allow you to separate the design and structure of your web pages from the Python code that generates the content.

Django templates use a special syntax to include dynamic content. Variables can be included using `{{ variable }}` syntax, and tags can be included using `{% tag %}` syntax.

Here’s an example of a simple Django template:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```

In this example, the `{{ name }}` placeholder will be replaced with the value of the `name` variable when the template is rendered.

Templates are typically rendered in views using the `render()` function. This function takes the request, the path to the template, and a context dictionary that maps placeholder names to values. Here’s an example of how to render a template in a view:

```python
from django.shortcuts import render

def greet(request):
    context = {'name': 'World'}
    return render(request, 'greet.html', context)
```

### Django Forms

A `form` is a web page element that allows users to input data and submit it to a web application. Forms are used to collect information from users, such as login credentials, search queries, and contact information. In Django, forms are used to process user input and validate it before saving it to the database.

How to create a simple form for a blog comment system:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
```

In this example, we have a `Post` model and a `Comment` model. The `Comment` is associated with a `Post` using a `ForeignKey` field. This allows us to create a one-to-many relationship between posts and comments (one post can have many comments).

```html
<form action="{% url 'add_comment' post.id %}" method="post">
    {% csrf_token %}
    <label for="author">Your name:</label><br>
    <input type="text" id="author" name="author"><br>
    <label for="text">Your comment:</label><br>
    <textarea id="text" name="text"></textarea><br>
    <input type="submit" value="Submit">
</form>
```

This is a simple HTML form that allows users to input their name and comment. The `action` attribute specifies the URL to which the form data will be submitted. The `method` attribute specifies the HTTP method to use when submitting the form (in this case, `post`). The `{% csrf_token %}` tag is used to include a CSRF token in the form, which helps protect against cross-site request forgery attacks.

In the HTML form, the `id` and `name` attributes in the input and textarea tags serve different purposes:

- The `id` attribute is used to uniquely identify an element in the HTML document. It’s often used to associate a label with a form control, and it can also be used to target an element with CSS or JavaScript.
- The `name` attribute is used to identify the form control when the form is submitted. It’s the name that will be used to access the data in the request object on the server side.

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment

def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    try:
        author = request.POST['author']
        text = request.POST['text']
    except KeyError:
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'error_message': "You didn't fill in all fields.",
        })
    else:
        Comment.objects.create(post=post, author=author, text=text)
        return HttpResponseRedirect(reverse('post_detail', args=(post.id,)))
```

This is the `view` that handles the form submission. It first fetches the `Post` object for which the comment is being added. If the `Post` doesn't exist, it raises a 404 error. It then tries to get the `author` and `text` fields from the POST data. If either field is missing, it re-renders the form with an error message. If both fields are present, it creates a new `Comment` object and saves it to the database. Finally, it redirects the user back to the post detail page.