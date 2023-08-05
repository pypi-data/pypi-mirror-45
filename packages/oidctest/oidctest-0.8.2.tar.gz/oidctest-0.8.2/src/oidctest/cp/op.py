import json
from http.cookies import SimpleCookie

from future.backports.urllib.parse import urlparse

import logging

import cherrypy
import cherrypy_cors
from cherrypy import url
from jwkest import as_bytes
from jwkest import as_unicode
from oic.oauth2 import Message
from otest.events import EV_ENDPOINT
from otest.events import EV_FAULT
from otest.events import EV_REQUEST
from otest.events import EV_RESPONSE
from otest.events import FailedOperation
from otest.events import Operation
from otest.flow import ABBR

from oidctest.cp import init_events
from oidctest.cp import write_events
from oidctest.cp.op_handler import init_keyjar
from oidctest.cp.op_handler import write_jwks_uri

logger = logging.getLogger(__name__)


def handle_error():
    cherrypy.response.status = 500
    cherrypy.response.body = [
        "<html><body>Sorry, an error occured</body></html>"
    ]


def set_content_type(resp, content_type):
    if ('Content-type', content_type) in resp.headers:
        return

    _headers = [h for h in resp.headers if h[0] != 'Content-type']
    _headers.append(('Content-type', content_type))
    resp.headers = _headers


def conv_response(op, resp):
    _stat = resp.status_code
    for typ, val in resp.headers:
        if typ == 'Set-Cookie':
            cherrypy.response.cookie.load(val)

    if _stat < 300:
        op.events.store(EV_RESPONSE, resp.message)
        cherrypy.response.status = _stat
        for key, val in resp.headers:
            if key == 'Set-Cookie':
                continue
            cherrypy.response.headers[key] = val
        return as_bytes(resp.message)
    elif 300 <= _stat < 400:
        op.events.store('Redirect', resp.message)
        raise cherrypy.HTTPRedirect(resp.message, status=302)
    else:
        logger.debug("Error - Status:{}, message:{}".format(_stat, resp.message))
        op.events.store(EV_FAULT, resp.message)
        raise cherrypy.HTTPError(_stat, message=resp.message)


def store_request(op, where):
    _ev = Operation(where, path=url())

    try:
        op.events.store(EV_REQUEST, _ev)
    except Exception as err:
        raise


def parse_resource(resource):
    """

    :param resource:
    :return: A tuple: op_id and test_id
    """
    p = urlparse(resource)
    if p[0] == 'acct':
        loc, dom = p[2].split('@', 1)  # Should I check the domain part ?
        _x = loc.split('.')
        if len(_x) == 2:
            return _x
        elif len(_x) > 2:
            return '.'.join(_x[0:-1]), _x[-1]
        else:
            raise ValueError('Need both op_id and test_id, got {}'.format(_x))
    elif p[0] in ['http', 'https']:
        _x = p[2][1:].split('/')  # skip leading '/'
        if len(_x) >= 2:
            return _x[:2]  # only return the first two parts
        else:
            _txt = 'Need both op_id and test_id, got {}'.format(_x)
            logger.error(_txt)
            raise ValueError(_txt)
    else:
        return None


class WebFinger(object):
    def __init__(self, srv, version=''):
        self.srv = srv
        self.version = version

    @cherrypy.expose
    def index(self, resource, rel):
        ev = init_events('/.well-known/webfinger',
                         'Test tool version:{}'.format(self.version))
        ev.store(EV_REQUEST, Operation('WebFinger', resource=resource, rel=rel))

        if rel != 'http://openid.net/specs/connect/1.0/issuer':
            ev.store(EV_FAULT,
                     FailedOperation('Webfinger', error='unknown rel', rel=rel))
            try:
                op_id, test_id = parse_resource(resource)
            except (ValueError, TypeError):
                logger.error('webfinger resource specification faulty')
                raise cherrypy.HTTPError(
                    400, 'webfinger resource specification faulty')
            else:
                write_events(ev, op_id, test_id)
            raise cherrypy.NotFound()

        try:
            op_id, test_id = parse_resource(resource)
        except (ValueError, TypeError):
            logger.error('webfinger resource specification faulty')
            raise cherrypy.HTTPError(
                400, 'webfinger resource specification faulty')
        else:
            _path = '/'.join([op_id, test_id])

        cnf = cherrypy.request.config
        subj = resource
        _base = cnf['base_url']
        dummy = None

        # introducing an error
        if 'rp-discovery-webfinger-http-href' in resource:
            _base = _base.replace('https', 'http')
        if 'rp-discovery-webfinger-unknown-member' in resource:
            dummy = "foobar"

        if _base.endswith('/'):
            href = '{}{}'.format(_base, _path)
        else:
            href = '{}/{}'.format(_base, _path)

        ev.store(EV_RESPONSE,
                 Operation('Webfinger', href=href, subj=resource, dummy=dummy))
        write_events(ev, op_id, test_id)
        resp = self.srv.response(subj, href, dummy=dummy)
        cherrypy.response.headers['Content-Type'] = 'application/jrd+json'
        return as_bytes(resp)


class Configuration(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["GET", "OPTIONS"])
    def index(self, op):
        if cherrypy.request.method == "OPTIONS":
            logger.debug('Request headers: {}'.format(cherrypy.request.headers))
            cherrypy_cors.preflight(
                allowed_methods=["GET"],
                allowed_headers=['Authorization', 'content-type'],
                allow_credentials=True, origins='*'
            )
        else:
            store_request(op, 'ProviderInfo')
            resp = op.providerinfo_endpoint()
            if resp.status_code < 300:
                set_content_type(resp, 'application/json')
            return conv_response(op, resp)


class Registration(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["POST", "OPTIONS"])
    def index(self, op):
        if cherrypy.request.method == "OPTIONS":
            logger.debug('Request headers: {}'.format(cherrypy.request.headers))
            cherrypy_cors.preflight(
                allowed_methods=["POST"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'ClientRegistration')
            if cherrypy.request.process_request_body is True:
                _request = cherrypy.request.body.read()
            else:
                raise cherrypy.HTTPError(400,
                                         'Missing Client registration body')
            logger.debug('request_body: {}'.format(_request))
            resp = op.registration_endpoint(as_unicode(_request))
            if resp.status_code < 300:
                set_content_type(resp, 'application/json')
            return conv_response(op, resp)


class Authorization(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["GET", "OPTIONS"])
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["GET"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'AuthorizationRequest')
            logger.debug('AuthorizationRequest: {}'.format(kwargs))
            op.events.store(EV_REQUEST, kwargs)
            resp = op.authorization_endpoint(kwargs)
            return conv_response(op, resp)


class Token(object):
    _cp_config = {"request.methods_with_bodies": ("POST", "PUT")}

    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["POST", "OPTIONS"])
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["POST"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'AccessTokenRequest')
            try:
                authn = cherrypy.request.headers['Authorization']
            except KeyError:
                authn = None
            logger.debug('Authorization: {}'.format(authn))
            resp = op.token_endpoint(as_unicode(kwargs), authn, 'dict')
            if resp.status_code < 300:
                set_content_type(resp, 'application/json')
            return conv_response(op, resp)


class UserInfo(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["GET", "POST", "OPTIONS"])
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["GET", "POST"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'UserinfoRequest')
            args = {'request': kwargs}
            if cherrypy.request.process_request_body is True:
                _req = cherrypy.request.body.read()
                if _req:  # The request is either in kwargs or in body
                    args['request'] = _req

            try:
                args['authn'] = cherrypy.request.headers['Authorization']
            except KeyError:
                pass

            #kwargs.update(args)
            resp = op.userinfo_endpoint(**args)
            #if resp.status_code < 300:
            #    set_content_type(resp, 'application/json')
            return conv_response(op, resp)


class Claims(object):
    @cherrypy.expose
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["GET"], origins='*',
                allowed_headers='Authorization')
        else:
            try:
                authz = cherrypy.request.headers['Authorization']
            except KeyError:
                authz = None
            try:
                assert authz.startswith("Bearer")
            except AssertionError:
                op.events.store(EV_FAULT, "Bad authorization token")
                cherrypy.HTTPError(400, "Bad authorization token")

            tok = authz[7:]
            try:
                _claims = op.claim_access_token[tok]
            except KeyError:
                op.events.store(EV_FAULT, "Bad authorization token")
                cherrypy.HTTPError(400, "Bad authorization token")
            else:
                # one time token
                del op.claim_access_token[tok]
                _info = Message(**_claims)
                jwt_key = op.keyjar.get_signing_key()
                op.events.store(EV_RESPONSE, _info.to_dict())
                cherrypy.response.headers["content-type"] = 'application/jwt'
                return as_bytes(_info.to_jwt(key=jwt_key, algorithm="RS256"))


class CheckSessionIframe(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["GET", "OPTIONS", "POST"])
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["GET", "POST"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'CheckSessionIframe')
            logger.debug('CheckSessionIframe: {}'.format(kwargs))
            if cherrypy.request.method == "POST":
                _req = cherrypy.request.body.read()
                kwargs = json.loads(as_unicode(_req))
                # will contain client_id and origin
                if kwargs['client_id'] not in op.cdb:
                    return b'error'
                # Should have some intelligent check for origin
                return b'ok'
            else:
                doc = open('templates/check_session_iframe.html').read()
                return as_bytes(doc)


class EndSession(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["GET", "OPTIONS"])
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["GET"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'EndSessionRequest')
            logger.debug('EndSessionRequest: {}'.format(kwargs))
            # op.events.store(EV_REQUEST, kwargs)
            cookie = cherrypy.request.cookie
            _info = Message(**kwargs)
            resp = op.end_session_endpoint(_info.to_urlencoded(), cookie=cookie)
            # Normally the user would here be confronted with a logout
            # verification page. We skip that and just assumes she said yes.

            return conv_response(op, resp)


LOGOUT_HTML_HEAD = """
<!DOCTYPE html>
<head>
  <meta charset="utf-8">
  <title>Logout</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <style>
    iframe{visibility:hidden;position:absolute;left:0;top:0;height:0;width:0;border:none}
  </style>
</head>
"""
LOGOUT_HTML_BODY = """
<body>
  <script>
    var loaded = 0;
    var iframes = {size};
    function redirect() {
      window.location.replace("{postLogoutRedirectUri}");
    }
    function frameOnLoad() {
      loaded += 1;
      if (loaded === iframes) {
        redirect();
      }
    }
    Array.prototype.slice.call(document.querySelectorAll('iframe')).forEach(function (element) {
      element.onload = frameOnLoad;
    });
    setTimeout(redirect, {timeout});
  </script>
  {frames}
</body>
</html>
"""


class Logout(object):
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["OPTIONS", "POST", "GET"])
    def index(self, op, **kwargs):
        if cherrypy.request.method == "OPTIONS":
            cherrypy_cors.preflight(
                allowed_methods=["POST", "GET"], origins='*',
                allowed_headers=['Authorization', 'content-type'])
        else:
            store_request(op, 'Logout')
            logger.debug('LogoutRequest: {}'.format(kwargs))
            op.events.store(EV_REQUEST, kwargs)

            # Normally the user would here be confronted with a logout
            # verification page. We skip that and assumes she said yes.

            _info = op.unpack_signed_jwt(kwargs['sjwt'])
            logger.debug("SJWT unpacked: {}".format(_info))
            try:
                res = op.do_verified_logout(alla=True, **_info)
            except Exception as err:
                logger.exception(err)
                raise cherrypy.HTTPError(message=err)

            try:
                _iframes = res['iframe']
            except KeyError:
                _iframes = []

            _body = LOGOUT_HTML_BODY.replace('{size}', str(len(_iframes)))
            _body = _body.replace('{frames}',''.join(_iframes))
            _body = _body.replace('{timeout}', '30')
            _body = _body.replace('{postLogoutRedirectUri}',
                                  _info['redirect_uri'])

            try:
                cookies = res['cookie']
            except KeyError:
                pass
            else:
                for tag, val in cookies:
                    cherrypy.response.cookie.load(val)

            return as_bytes("\n".join([LOGOUT_HTML_HEAD, _body]))


HTML_PRE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OpenID Connect Relying Party Certification</title>
<link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
<link href="/static/theme.css" rel="stylesheet">
<!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
<body>

    <div class="container" role="main">

        <div class="page-header">
            <div class="pull-left">
                <h2>OpenID Connect Relying Party Certification</h2>
            </div>
            <div class="pull-right">
                <a href="https://openid.net/certification"><img
                    class="img-responsive" src="/static/logo.png" /></a>
            </div>
            <div class="clearfix"></div>
        </div>
"""

HTML_POST = """
    </div>

    <script
        src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
</body>
</html>
"""

HTML_FOOTER = """
        <div id="footer" class="footer text-muted">
            <hr />
            <div class="pull-left">
                <ul class="list-inline">
                    <li>(C) 2017-2019 - <a href="https://openid.net/foundation">OpenID
                            Foundation</a></li>
                    <li>E-mail: <a href="mailto:certification@oidf.org">certification@oidf.org</a></li>
                    <li>Issues: <a
                        href="https://github.com/openid-certification/oidctest/issues">Github</a>
                    <li>
                </ul>
            </div>
            <div class="pull-right">
                <ul class="list-inline">
                    <li>Version: {}</li>
                </ul>
            </div>
        </div>
"""


def choice(profiles):
    keys = list(profiles.keys())
    keys.sort()

    line = [
        '<table class="table table-hover table-bordered" style="font-family:monospace;">',
        ]
    for k in keys:
        line.append('<tr>')
        line.append('  <td width="80%">{}</td>'.format(k))
        line.append('  <td class="text-center"><input type="radio" name="profile" value="{}"></td>'.format(
            profiles[k]))
        line.append('</tr>')
    line.append('</table>')
    return '\n'.join(line)


class Reset(object):
    def __init__(self, com_args, op_args):
        self.com_args = com_args
        self.op_args = op_args

    @cherrypy.expose
    def index(self, op):
        init_keyjar(op, self.op_args['keyjar'], self.com_args)
        write_jwks_uri(op, self.op_args, {})
        return b'OK'


class Root(object):
    def __init__(self, version=''):
        self.version = version

    @cherrypy.expose
    def index(self):
        response = [
            HTML_PRE,
            '<div class="jumbotron">',
            '  <p>',
            '    This is a tool for testing the compliance of an OpenID Connect Relying Party with the OpenID Connect specifications.',
            '    Before you start testing please read the ',
            '    <a href="https://openid.net/certification/rp_testing/" target="_blank">Conformance Testing for RPs</a> introduction guide.',
            '  </p>',
            '</div>',

            '<div class="panel panel-primary">',
            '  <div class="panel-heading">',
            '    <h3 class="panel-title">Response Types</h3>',
            '  </div>',
            '  <div class="panel-body">'
            '    <p>For a list of OIDC RP library tests per response_type choose your preference:</p>',
            '    <form action="list" class="col-md-6">',
            choice(ABBR),
            '        <div class="form-group">',
            '            <button type="submit" class="btn btn-primary">Submit</button>',
            '        </div>',
            '    </form>',
            '  </div>',
            '</div>',

            HTML_FOOTER.format(self.version),

            HTML_POST
        ]
        return '\n'.join(response)


class Provider(Root):
    _cp_config = {'request.error_response': handle_error}

    def __init__(self, op_handler, flows, version=''):
        Root.__init__(self, version)
        self.op_handler = op_handler
        self.flows = flows
        self.configuration = Configuration()
        self.registration = Registration()
        self.authorization = Authorization()
        self.token = Token()
        self.userinfo = UserInfo()
        self.claims = Claims()
        self.end_session = EndSession()
        self.logout = Logout()
        self.reset = Reset(self.op_handler.com_args, self.op_handler.op_args)
        self.check_session_iframe = CheckSessionIframe()

    def _cp_dispatch(self, vpath):
        # Only get here if vpath != None
        ent = cherrypy.request.remote.ip
        logger.info('ent:{}, vpath: {}'.format(ent, vpath))

        if vpath[0] == 'static':
            return vpath

        if len(vpath) >= 2:
            ev = init_events(cherrypy.request.path_info,
                             'Test tool version:{}'.format(self.version))
            oper_id = vpath.pop(0)
            test_id = vpath.pop(0)

            # verify test_id
            try:
                self.flows[test_id]
            except KeyError:
                raise cherrypy.HTTPError(400, 'Unknown TestID')

            if len(vpath):
                if len(vpath) == 1:
                    endpoint = vpath.pop(0)
                    op = self.op_handler.get(oper_id, test_id, ev, endpoint)[0]
                    op.events.store(EV_ENDPOINT, endpoint)
                    cherrypy.request.params['op'] = op
                    if endpoint == 'registration':
                        return self.registration
                    elif endpoint == 'authorization':
                        return self.authorization
                    elif endpoint == 'token':
                        return self.token
                    elif endpoint == 'userinfo':
                        return self.userinfo
                    elif endpoint == 'claim':
                        return self.claims
                    elif endpoint == 'reset':
                        return self.reset
                    elif endpoint == 'end_session':
                        return self.end_session
                    elif endpoint == 'logout':
                        return self.logout
                    elif endpoint == 'check_session_iframe':
                        return self.check_session_iframe
                    else:  # Shouldn't be any other
                        raise cherrypy.NotFound()
                if len(vpath) == 2:
                    a = vpath.pop(0)
                    b = vpath.pop(0)
                    endpoint = '{}/{}'.format(a, b)
                    if endpoint == ".well-known/openid-configuration":
                        op = self.op_handler.get(oper_id, test_id, ev,
                                                 endpoint)[0]
                        cherrypy.request.params['op'] = op
                        return self.configuration

        return self


class RelyingPartyInstance(object):
    
    def rp_3rd_party_init_login(self, op, client_id):
        if client_id in op.cdb:
            if 'initiate_login_uri' in op.cdb[client_id]:
                raise cherrypy.HTTPRedirect(op.cdb[client_id]['initiate_login_uri'])
            else:
                response = ['<pre>']
                response.append("no 3rd-party initiated login URI found for  " + client_id)
                response.append('</pre>')
                return '\n'.join(response)
        else:
            raise cherrypy.HTTPError(404, "client_id " + client_id + " not found in client database!")            
 
    @cherrypy.expose
    @cherrypy_cors.tools.expose_public()
    @cherrypy.tools.allow(
        methods=["GET", "OPTIONS"])
    def index(self, op, test_id, client_id):
        if cherrypy.request.method == "OPTIONS":
            logger.debug('Request headers: {}'.format(cherrypy.request.headers))
            cherrypy_cors.preflight(
                allowed_methods=["GET"],
                allowed_headers=['Authorization', 'content-type'],
                allow_credentials=True, origins='*'
            )
        else:
            if test_id == "rp-3rd_party-init-login":
                return self.rp_3rd_party_init_login(op, client_id)
            raise cherrypy.HTTPError(404, "no test handler found for test id: " + test_id)


class RelyingParty(object):
    def __init__(self, op_handler, version=''):
        self.version = version
        self.op_handler = op_handler
        self.instance = RelyingPartyInstance()

    @cherrypy.expose
    def index(self):
        response = [
            HTML_PRE,
            '<div class="jumbotron">',
            '  <p>',
            '    Add the Relying Party instance identifier to the path....',
            '  </p>',
            '</div>',

            HTML_FOOTER.format(self.version),

            HTML_POST
        ]
        return '\n'.join(response)

    def _cp_dispatch(self, vpath):
        # Only get here if vpath != None
        ent = cherrypy.request.remote.ip
        logger.info('ent:{}, vpath: {}'.format(ent, vpath))
        
        if len(vpath) >= 1:
            ev = init_events(cherrypy.request.path_info,
                             'Test tool version:{}'.format(self.version))
            # e.g https://rp-test:8080/rp/mod_auth_openidc/rp-3rd_party-init-login/OLtakKrycmtj
            rp_id = vpath.pop(0)
            test_id = vpath.pop(0)
            client_id = vpath.pop(0)

            endpoint = ''            
                    
            op = self.op_handler.get(rp_id, test_id, ev,
                                     endpoint)[0]
            cherrypy.request.params['op'] = op
            cherrypy.request.params['test_id'] = test_id
            cherrypy.request.params['client_id'] = client_id
            
            return self.instance            
        else:
            raise cherrypy.HTTPError(400, 'Unknown vpath stuffy')
