# -*- coding: utf-8 -*-

def index():
    '''
    accesible sólo al tesorero
    '''

    response.title = 'Alumnos'

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


def deuda():
    '''
    Esto es lo que ve el alumno
    '''

    alumno = request.get_vars.alumno
    
    alumno_data = db.alumno(alumno) or redirect(URL(f='index'))

    response.title = 'Deudas'
    response.subtitle = '%s %s %s' % (alumno_data.nombre.capitalize(), 
                                      alumno_data.apellido_paterno.capitalize(),
                                      alumno_data.apellido_materno.capitalize())

    

    deuda_sum = db.deuda.total.coalesce_zero().sum()

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



def pago():
    deuda = request.get_vars.deuda
    alumno = request.get_vars.alumno

    db.pago.deuda.default = deuda
    db.pago.alumno.default = alumno
    db.pago.deuda.writable = False
    db.pago.deuda.readable = False
    db.pago.alumno.writable = False
    db.pago.alumno.readable = False

    form = SQLFORM(db.pago)

    form.vars.deuda = deuda
    form.vars.alumno = alumno

    if form.process().accepted:
        msg = 'Se han abonado {0} a "{1}"'
        response.flash = msg.format(form.vars.monto, db.deuda(form.vars.deuda).nombre)
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


    return {'form': form, 'pagos': pagos}

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()

