Django Form Designer (AI Fork)
******************************

Acknowledgements
================

This project is a fork of https://github.com/samluescher/django-form-designer .
Thanks, @samluescher!

This fork is compatible with Django 1.7+ and Python 2.7+.

General
=======

A Django admin app with a GUI to create complex forms without any programming skills;
complete with logging, validation, and redirects.

**Key features**:

* Design contact forms, search forms etc from the Django admin, without writing any code
* Form data can be logged and CSV-exported, sent via e-mail, or forwarded to any web address
* Integration with `Django CMS <http://www.django-cms.org>`_: Add forms to any page
* Use drag & drop to change the position of your form fields
* Fully collapsible admin interface for better overview over your form
* Implements many form fields included with Django (TextField, EmailField, DateField etc)
* Validation rules as supplied by Django are fully configurable (maximum length, regular
  expression etc)
* Customizable messages and labels
* Supports POST and GET forms
* Signals on form render, submission, success, error.
* Supports google reCAPTCHA service


Basic setup
===========

- Add ``form_designer`` to your ``INSTALLED_APPS`` setting::

        INSTALLED_APPS = (
            ...
            'form_designer',
        )

- For basic usage, add URLs to your URL conf. For instance, in order to make a form named
  ``example-form`` available under ``http://domain.com/forms/example-form``,
  add the following line to your project's ``urls.py``::

    urlpatterns = patterns('',
        (r'^forms/', include('form_designer.urls')),
        ...
    )

  .. Note::
     If you are using the form_designer plugin for Django CMS for making forms
     public, this step is not necessary.


Using Django Form Designer with Django CMS
==========================================

- Add ``form_designer.contrib.cms_plugins.form_designer_form`` to your ``INSTALLED_APPS``
  setting::

        INSTALLED_APPS = (
            ...
            'form_designer.contrib.cms_plugins.form_designer_form',
        )

You can now add forms to pages created with Django CMS.


Optional requirements
=====================

The form_designer admin interface requires jQuery and the jQuery UI Sortable
plugin to make building forms a lot more user-friendly. The two Javascript
files are bundled with form_designer. If you want to use you own jquery.js
instead because you're already including it anyway, define JQUERY\_JS in your
settings file. For instance::

    JQUERY_JS = 'jquery/jquery-latest.js'

Running tests
=============

Use `tox`.
