# coding: utf8

db.define_table('alumno',
                Field('nombre', 'string', length=10),
                Field('apellido_paterno', length=10),
                Field('apellido_materno', length=10),
                Field('apoderados', 'list:reference auth_user'),
                format = '%(nombre)s %(apellido_paterno)s %(apellido_materno)s'
                )


db.define_table('deuda',
                Field('nombre'),
                Field('monto','integer'),
                Field('cuotas', 'integer', label='Número de cuotas'),
                Field('comienza','date', default=request.now.date()),
                Field('finaliza','date', default=request.now.date()),
                Field('infoextra', 'text',
                      label = 'Información Extra'),
                Field('total', 'integer', compute = lambda r: r.monto * r.cuotas),
                auth.signature,
                format = '%(nombre)s ($%(total)s)'
                )


db.define_table('pago',
                Field('alumno', 'reference alumno'),
                Field('deuda', 'reference deuda'),
                Field('monto', 'integer', label='Monto a pagar'),
                Field('fecha', 'date', default = request.now.date(),
                      label = 'Fecha de Pago'),
                #Field('mes', compute = lambda r: r.fecha.month),
                Field('infoextra', 'text', 
                      label = 'Información Extra'),
                auth.signature,
                format = '%(ano)s-%(mes)s: %(monto)s'
                )


db.define_table('documento_pago',
                Field('pago', 'reference pago'),
                Field('adjuntar', 'upload')
                )
