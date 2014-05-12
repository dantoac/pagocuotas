# coding: utf8

def numfmt(value, places=0, curr='$', sep='.', dp='',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    from decimal import Decimal
    value = str(value)
    value = Decimal(value)
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


DEUDA_TOTAL_ESTE_ANO = db(db.deuda.finaliza.year() == request.now.year).select(db.deuda.monto.sum()).first()[db.deuda.monto.sum()]


def _infoalumno(alumno_id):

    from gluon.storage import Storage

    data = db((db.alumno.id == alumno_id)
              #& (db.alumno.apoderado == db.apoderado.id)
          ).select(cacheable=True).first()

    info = {'nombre_completo' : '{0} {1} {2}'.format(data.nombre, data.apellido_paterno, data.apellido_materno),
            'apoderado': ','.join(['{0} {1}'.format(db.auth_user(a).first_name, db.auth_user(a).last_name) for a in data.apoderados])
    }

    return Storage(info)
