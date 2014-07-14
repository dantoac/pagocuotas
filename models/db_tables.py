# coding: utf8

db._common_fields.append(auth.signature)

db.define_table('alumno',
                Field('nombre', 'string'), #, length=10),
                Field('apellido_paterno'), #, length=10),
                Field('apellido_materno'),# , length=10),
                format = '%(nombre)s %(apellido_paterno)s %(apellido_materno)s'
                )


db.define_table('apoderado',
                Field('usuario', 'reference auth_user'),
                Field('alumno', 'reference alumno'),
            )


db.define_table('deuda',
                Field('nombre'),
                Field('monto','integer',
                      represent = lambda v,r: numfmt(v)),
                Field('cuotas', 'integer', label='Número de cuotas'),
                Field('comienza','date', default=request.now.date()),
                Field('finaliza','date', default=request.now.date()),
                Field('infoextra', 'text',
                      label = 'Información Extra'),
                Field('total', 'integer', 
                      compute = lambda r: r.monto * r.cuotas,
                      represent = lambda v,r: numfmt(v),
                  ),
                format = lambda r: '%(nombre)s (%(total)s)' % dict(
                    nombre = r.nombre,
                    total = numfmt(r.total)
                )
                )


db.define_table('pago',
                Field('alumno', 'reference alumno'),
                Field('deuda', 'reference deuda'),
                Field('monto', 'integer', label='Monto a pagar',
                      represent = lambda v,r: numfmt(v)),
                Field('fecha', 'date', default = request.now.date(),
                      label = 'Fecha de Pago'),
                #Field('mes', compute = lambda r: r.fecha.month),
                Field('infoextra', 'text', 
                      label = 'Información Extra'),
                format = '%(fecha)s: %(monto)s'
                )


db.pago._enable_record_versioning()

db.define_table('documento_pago',
                Field('pago', 'reference pago'),
                Field('adjuntar', 'upload')
                )


def porcentaje(total, porcion):

    porciento = porcion * 100 / total

    return porciento
