# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = ''#A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                #  _class="brand",_href="http://www.web2py.com/")
response.title = 'Pago de Cuotas'
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Daniel Aguayo <daniel@nim.io>'
#response.meta.keywords = 'web2py, python, framework'
#response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Inicio'), False, URL(c='default', f='index'), []),
    (T('Administrar'), False, URL(c='default', f='admin'), []),

    
]


