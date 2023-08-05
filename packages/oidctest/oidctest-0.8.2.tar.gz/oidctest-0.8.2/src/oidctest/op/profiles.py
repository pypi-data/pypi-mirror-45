from otest import Done
from otest.func import set_request_args
from otest.operation import Note

from oidctest.op.oper import AccessToken
from oidctest.op.oper import AsyncAuthn
from oidctest.op.oper import Discovery
from oidctest.op.oper import DisplayUserInfo
from oidctest.op.oper import Registration
from oidctest.op.oper import SyncAuthn
from oidctest.op.oper import UserInfo
from oidctest.op.oper import Webfinger
from oidctest.testfunc import check_endpoint

__author__ = 'roland'

PMAP = {"C": "Basic",
        "I": "Implicit (id_token)", "IT": "Implicit (id_token+token)",
        "CI": "Hybrid (code+id_token)", "CT": "Hybrid (code+token)",
        "CIT": "Hybrid (code+id_token+token)"}

PROFILEMAP = {
    Webfinger: {"C": {}, "I": {}, "IT": {}, "CI": {}, "CT": {}, "CIT": {}},
    Discovery: {"C": {}, "I": {}, "IT": {}, "CI": {}, "CT": {}, "CIT": {}},
    Done: {"C": {}, "I": {}, "IT": {}, "CI": {}, "CT": {}, "CIT": {}},
    Note: {"C": {}, "I": {}, "IT": {}, "CI": {}, "CT": {}, "CIT": {}},
    SyncAuthn: {
        "C": {set_request_args: {"response_type": ["code"],
                                 "scope": ["openid"]},
              check_endpoint: "authorization_endpoint"},
        "I": {set_request_args: {"response_type": ["id_token"],
                                 "scope": ["openid"]}},
        # "T": {set_request_args: {"response_type": ["token"],
        #                          "scope": ["openid"]}},
        "IT": {set_request_args: {"response_type": ["id_token", "token"],
                                  "scope": ["openid"]}},
        "CI": {set_request_args: {"response_type": ["code", "id_token"],
                                  "scope": ["openid"]}},
        "CT": {set_request_args: {"response_type": ["code", "token"],
                                  "scope": ["openid"]}},
        "CIT": {set_request_args:
                    {"response_type": ["code", "id_token", "token"],
                     "scope": ["openid"]}},
    },
    AsyncAuthn: {
        "C": {set_request_args: {"response_type": ["code"],
                                 "scope": ["openid"]}},
        "I": {set_request_args: {"response_type": ["id_token"],
                                 "scope": ["openid"]}},
        #"T": {set_request_args: {"response_type": ["token"],
        #                         "scope": ["openid"]}},
        "IT": {set_request_args: {"response_type": ["id_token", "token"],
                                  "scope": ["openid"]}},
        "CI": {set_request_args: {"response_type": ["code", "id_token"],
                                  "scope": ["openid"]}},
        "CT": {set_request_args: {"response_type": ["code", "token"],
                                  "scope": ["openid"]}},
        "CIT": {set_request_args:
                    {"response_type": ["code", "id_token", "token"],
                     "scope": ["openid"]}},
    },
    AccessToken: {
        "C": {},
        "I": {},
        "IT": {},
        "CI": {},
        "CT": {},
        "CIT": {},
    },
    UserInfo: {
        "C": {},
        "I": {},
        "IT": {},
        "CI": {},
        "CT": {},
        "CIT": {},
    },
    DisplayUserInfo: {
        "C": {},
        "I": {},
        "IT": {},
        "CI": {},
        "CT": {},
        "CIT": {},
    },
    Registration: {
        "C": {
            set_request_args: {
                "response_types": ["code"],
                "grant_types": ["authorization_code"]}},
        # don't register any
        # "token_endpoint_auth_method": {},
        # "userinfo_signed_response_alg": {},
        # "id_token_signed_response_alg": {},
        # "request_object_signing_alg": {},

        "I": {
            set_request_args: {
                "response_types": ["id_token"],
                "grant_types": ["implicit"],
                # don't register any
                # "token_endpoint_auth_method": {},
                # "userinfo_signed_response_alg": {},
                # "id_token_signed_response_alg": {},
                # "request_object_signing_alg": {},
            }},
        "IT": {
            set_request_args: {
                "response_types": ["id_token token"],
                "grant_types": ["implicit"],
                # don't register any
                # "token_endpoint_auth_method": {},
                # "userinfo_signed_response_alg": {},
                # "id_token_signed_response_alg": {},
                # "request_object_signing_alg": {},
            }},
        "CI": {
            set_request_args: {
                "response_types": ["code id_token"],
                "grant_types": ["authorization_code", "implicit"],
                # don't register any
                # "token_endpoint_auth_method": {},
                # "userinfo_signed_response_alg": {},
                # "id_token_signed_response_alg": {},
                # "request_object_signing_alg": {},
            }
        },
        "CT": {
            set_request_args: {
                "response_types": ["code token"],
                "grant_types": ["authorization_code", "implicit"],
                # don't register any
                # "token_endpoint_auth_method": {},
                # "userinfo_signed_response_alg": {},
                # "id_token_signed_response_alg": {},
                # "request_object_signing_alg": {},
            }
        },
        "CIT": {
            set_request_args: {
                "response_types": ["code id_token token"],
                "grant_types": ["authorization_code", "implicit"],
                # don't register any
                # "token_endpoint_auth_method": {},
                # "userinfo_signed_response_alg": {},
                # "id_token_signed_response_alg": {},
                # "request_object_signing_alg": {},
            }
        }
    }
}

CRYPT = {"n": "none", "s": "signing", "e": "encryption"}
SUBPROF = {"n": "none", "s": "sign", "e": "encrypt"}
