from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import falcon


UNMARSHAL_PROBLEM_VERSION = '0.3.0'
UNMARSHAL_PROBLEM_TYPE_URI = (
    'https://pypi.org/project/falcon-oas/'
    + UNMARSHAL_PROBLEM_VERSION
    + '/#unmarshal-error'
)


class _Problem(falcon.HTTPError):
    """Represent predefined problem type of RFC 7807."""

    def __init__(self, http_error):
        super(_Problem, self).__init__(
            http_error.status,
            title=http_error.title,
            description=http_error.description,
        )

    def to_dict(self, obj_type=dict):
        obj = obj_type()
        obj['title'] = self.status[4:]
        obj['status'] = int(self.status[:3])
        if self.description is not None:
            obj['detail'] = self.description
        return obj


class UnmarshalProblem(falcon.HTTPError):
    def __init__(self, unmarshal_error):
        super(UnmarshalProblem, self).__init__(
            falcon.HTTP_BAD_REQUEST, title='Unmarshal Error'
        )
        self.unmarshal_error = unmarshal_error

    def to_dict(self, obj_type=dict):
        obj = obj_type()
        obj['type'] = UNMARSHAL_PROBLEM_TYPE_URI
        obj['title'] = self.title
        obj['status'] = int(self.status[:3])
        obj.update(self.unmarshal_error.to_dict(obj_type=obj_type))
        return obj


def serialize_problem(req, resp, problem):
    """Serialize the given instance of Problem."""
    preferred = req.client_prefers(
        ('application/json', 'application/problem+json')
    )
    if preferred is None:
        preferred = 'application/json'

    resp.data = problem.to_json().encode('utf-8')
    resp.content_type = preferred
    resp.append_header('Vary', 'Accept')


def http_error_handler(error, req, resp, params):
    raise _Problem(error)


def undocumented_media_type_handler(error, req, resp, params):
    raise _Problem(falcon.HTTPBadRequest())


def security_error_handler(error, req, resp, params):
    raise _Problem(falcon.HTTPForbidden())


def unmarshal_error_handler(error, req, resp, params):
    raise UnmarshalProblem(error)
