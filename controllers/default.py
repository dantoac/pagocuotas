# -*- coding: utf-8 -*-

from gluon.storage import Storage

#response.title = 'Registro Pago de Cuotas'
#response.subtitle = '1º Básico B, Colegio Concepción Chiguayante'


def is_apoderado(user_id, alumno):
    if not db((db.apoderado.usuario == user_id)
              & (db.apoderado.alumno == alumno)).isempty():
        
        alumno_data = db.alumno(alumno)
        
        session.alumno = '%s %s %s' % (alumno_data.nombre.capitalize(), 
                                       alumno_data.apellido_paterno.capitalize(),
                                       alumno_data.apellido_materno.capitalize())

        session.alumno_id = alumno_data.id

    else:
        raise HTTP(404, 'No hay ningún alumno asociado a tu cuenta de usuario.')



def index():
    '''
    accesible sólo al tesorero
    '''


    if not auth.has_membership('Directiva'):
        redirect(URL(f='apoderado'))

    response.title += 'Alumnos'

    total_pagado_alumno = db.pago.monto.coalesce_zero().sum()

    alumnos = db().select(
        db.alumno.ALL,
        total_pagado_alumno,
        left = db.pago.on(db.pago.alumno == db.alumno.id),
        groupby = db.alumno.id
    )

    deuda_sum = db.deuda.total.coalesce_zero().sum()
    total_deuda = db(db.deuda).select(deuda_sum).first()[deuda_sum] 


    pagado_sum = db.pago.monto.coalesce_zero().sum()
    total_pagado = db(db.pago).select(pagado_sum).first()[pagado_sum]
    

    return {'alumnos': alumnos, 
            'total_deuda': total_deuda,
            'total_pagado': total_pagado,
            'total_pagado_alumno': total_pagado_alumno
    }

@auth.requires_login()
def apoderado():

    response.title = 'Mis Hijos'

    total_pagado_alumno = db.pago.monto.coalesce_zero().sum()

    total_deuda = sum([d.total for d in db(db.deuda).select(db.deuda.total)])
    
    alumnos = db((db.auth_user.id == auth.user.id)
                 & (db.apoderado.usuario == db.auth_user.id)
                 & (db.apoderado.alumno == db.alumno.id)
    ).select(
        db.alumno.ALL,
        db.deuda.ALL,
        total_pagado_alumno,
        left = db.pago.on((db.pago.alumno == db.alumno.id)
                          & (db.pago.deuda == db.deuda.id)),
        groupby = db.alumno.id,
    )

    response.subtitle = []
    

    return {'alumnos': alumnos,
            'total_pagado_alumno': total_pagado_alumno,
            'total_deuda': total_deuda}


@auth.requires_login()
def deuda():
    '''
    Esto es lo que ve el alumno
    '''

    if session.alumno_id and not request.get_vars.alumno:
        alumno = session.alumno_id
    elif request.get_vars.alumno != 'None':
        alumno = request.get_vars.alumno
    else:
        alumno = 0

    #alumno = request.get_vars.alumno if request.get_vars.alumno != 'None' else 0

    is_apoderado(auth.user.id, alumno)

    response.title += ': Deudas'

    #deuda_sum = db.deuda.total.coalesce_zero().sum()

    total_pagado_alumno = db.pago.monto.coalesce_zero().sum()

    deudas_alumno = db(db.alumno.id == alumno).select(
        db.alumno.ALL,
        db.deuda.ALL,
        total_pagado_alumno,
        left = db.pago.on((db.pago.alumno == db.alumno.id)
                          & (db.pago.deuda == db.deuda.id)),
        groupby = db.deuda.id
    )


    
    return {'deudas': deudas_alumno,
            'total_pagado_alumno': total_pagado_alumno
            }


#@auth.requires_membership(#'Directiva)
def pago():
    deuda = request.get_vars.deuda
    alumno = session.alumno_id

    if request.get_vars.deuda:
        response.title = 'Pagos para %s' % db.deuda(request.get_vars.deuda).nombre.capitalize()
    response.subtitle = session.alumno

    db.pago.deuda.default = deuda
    db.pago.alumno.default = alumno
    db.pago.deuda.writable = False
    db.pago.deuda.readable = False
    db.pago.alumno.writable = False
    db.pago.alumno.readable = False


    query = (db.pago.alumno == alumno) & (db.pago.deuda == deuda)

    pagos = db(query
       ).select(db.pago.monto,
                db.pago.fecha,
                db.pago.created_on,
                orderby = ~db.pago.fecha
       )


    form = SQLFORM.grid(query, user_signature=True)

    '''
    form.vars.deuda = deuda
    form.vars.alumno = alumno

    if form.process().accepted:
        msg = 'Se han abonado {0} a "{1}"'
        response.flash = msg.format(numfmt(form.vars.monto), db.deuda(form.vars.deuda).nombre)
        #redirect(URL(c='default', f='deuda', vars = {'alumno': form.vars.alumno}))

    elif form.errors:
        response.flash = form.errors

    
    pagos = db((db.pago.alumno == alumno)
               & (db.pago.deuda == deuda)
           ).select(db.pago.monto,
                    db.pago.fecha,
                    db.pago.created_on,
                    orderby = ~db.pago.fecha
           )

    '''
    deuda_sum = db.deuda.total.coalesce_zero().sum()
    total_deuda = db(db.deuda.id == deuda).select(deuda_sum).first()[deuda_sum]

    total_pago = sum([p.monto for p in pagos])

    return {'form': form, 
            'pagos': pagos,
            'total_pagado': total_pago,
            'total_deuda': total_deuda
    }

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()



def nuevo():
    objeto = request.args(0)
    _id = request.args(1)
                    
    form = SQLFORM(db[objeto], _id, 
                   _action = URL('default','nuevo', args=request.args),
                   showid = False,
    )

    if form.process().accepted:
        redirect(URL(c='default', f='index.html'))
    
    return {'form': form}


@auth.requires_membership('Directiva')
def admin():

    form = SQLFORM.smartgrid(db[request.args(0) or 'alumno'], 
                             #request.args[1:1],
                             #csv = False,
                             #linked_tables = 
                            
                             user_signature=False)

    
    easy_titles = {'auth_user': 'Usuarios',
                   'auth_group': 'Grupos de Acceso',
                   'auth_membership': 'Membresías',
                   'alumno': 'Alumnos',
                   'apoderado': 'Apoderados',
                   'deuda': 'Deudas',
                   'pago': 'Pagos',
                   'pago_archive': 'Histórico de Pagos',
                   'documento_pago': 'Documentos de Pago'
    }

    et = Storage(easy_titles)
        
    return {'form':form, 'et':et}

