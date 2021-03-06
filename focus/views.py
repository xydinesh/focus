from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    FocusModel,
    )

from pyramid.httpexceptions import (
exception_response,
HTTPMethodNotAllowed,
HTTPBadRequest,
HTTPFound)

import datetime
import pytz

class FocusView(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='focus_save', renderer='templates/report_page.mako')
    @view_config(route_name='focus', renderer='templates/report_page.mako')
    def focus_view(self):
        request = self.request
        if request.method == 'POST':
            focus = request.params.get('focus', 0)
            productivity = request.params.get('productivity', 0)
            motivation = request.params.get('motivation', '0')
            energy = request.params.get('energy', 0)
            create_time = datetime.datetime.now(tz=pytz.timezone('EST'))
            fm = FocusModel(focus=focus, motivation=motivation,
                            productivity=productivity, energy=energy, create_time=create_time)
            DBSession.add(fm)
            return HTTPFound(location='focus')
        focus_values = DBSession.query(FocusModel).order_by(FocusModel.create_time.desc()).limit(10)
        return {'project': 'focus', 'values': focus_values}

@view_config(route_name='home', renderer='templates/mytemplate.mako')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'focus'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_focus_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
