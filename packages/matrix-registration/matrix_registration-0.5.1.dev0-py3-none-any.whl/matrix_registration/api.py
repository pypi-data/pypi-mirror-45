# Standard library imports...
import hashlib
import hmac
import logging
import yaml
from requests import exceptions
import re
import sys
from urllib.parse import urlparse

# Third-party imports...
from flask import Flask, abort, jsonify, request, make_response
from flask_httpauth import HTTPTokenAuth
from wtforms import Form, BooleanField, StringField, PasswordField, validators

# Local imports...
from .matrix_api import create_account
from . import config
from . import tokens


app = Flask(__name__)

auth = HTTPTokenAuth(scheme='SharedSecret')
logger = logging.getLogger(__name__)


re_mxid = re.compile(r'^@?[a-zA-Z_\-=\.\/0-9]+(:[a-zA-Z\-\.:\/0-9]+)?$')


def validate_token(form, token):
    """
    validates token

    Parameters
    ----------
    arg1 : Form object
    arg2 : str
        token name, e.g. 'DoubleWizardSki'

    Raises
    -------
    ValidationError
        Token is invalid

    """
    tokens.tokens.load()
    if not tokens.tokens.valid(token.data):
        raise validators.ValidationError('Token is invalid')


def validate_username(form, username):
    """
    validates username

    Parameters
    ----------
    arg1 : Form object
    arg2 : str
        username name, e.g: '@user:matrix.org' or 'user'
        https://github.com/matrix-org/matrix-doc/blob/master/specification/appendices/identifier_grammar.rst#user-identifiers
    Raises
    -------
    ValidationError
        Username doesn't follow mxid requirements
    """
    domain = urlparse(config.config.server_location).hostname
    re_mxid = r'^@?[a-zA-Z_\-=\.\/0-9]+(:' + \
              re.escape(domain) + \
              r')?$'
    err = "Username doesn't follow pattern: '%s'" % re_mxid
    if not re.search(re_mxid, username.data):
        raise validators.ValidationError(err)


def validate_password(form, password):
    """
    validates username

    Parameters
    ----------
    arg1 : Form object
    arg2 : str
        password
    Raises
    -------
    ValidationError
        Password doesn't follow length requirements
    """
    min_length = config.config.password['min_length']
    err = 'Password should be between %s and 255 chars long' % min_length
    if len(password.data) < min_length or len(password.data) > 255:
        raise validators.ValidationError(err)


class RegistrationForm(Form):
    """
    Registration Form

    validates user account registration requests
    """
    username = StringField('Username', [
        validators.Length(min=1, max=200),
        # validators.Regexp(re_mxid)
        validate_username
    ])
    password = PasswordField('New Password', [
        # validators.Length(min=8),
        validate_password,
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    token = StringField('Token', [
        validators.Regexp(r'^([A-Z][a-z]+)+$'),
        validate_token
    ])


@auth.verify_token
def verify_token(token):
    return token == config.config.shared_secret


@app.route('/register', methods=['POST'])
def register():
    """
    main user account registration endpoint

    to register an account you need to send a
    application/x-www-form-urlencoded request with
      - username
      - password
      - confirm
      - token
    as described in the RegistrationForm
    """
    logger.debug('an account registration started...')
    form = RegistrationForm(request.form)
    logger.debug('validating request data...')
    if form.validate():
        logger.debug('request valid')
        # remove sigil and the domain from the username
        username = form.username.data.rsplit(':')[0].split('@')[-1]
        logger.debug('creating account %s...' % username)
        # send account creation request to the hs
        try:
            account_data = create_account(form.username.data,
                                          form.password.data,
                                          config.config.server_location,
                                          config.config.shared_secret)
        except exceptions.ConnectionError as e:
            logger.error('can not connect to server_location',
                         exc_info=True)
            abort(500)
        except exceptions.HTTPError as e:
            resp = e.response
            error = resp.json()
            status_code = resp.status_code
            if status_code == 404:
                logger.error('no HS found at server_location')
            elif status_code == 403:
                logger.error('wrong registration secret')
            elif status_code == 400:
                # most likely this should only be triggered if a userid
                # is already in use
                return make_response(jsonify(error), 400)
            else:
                logger.error('failure communicating with HS',
                             exc_info=True)
            abort(500)
        logger.debug('account creation succeded!')
        tokens.tokens.use(form.token.data)
        return jsonify(access_token=account_data['access_token'],
                       home_server=account_data['home_server'],
                       user_id=account_data['user_id'],
                       status='success',
                       status_code=200)
    else:
        logger.debug('account creation failed!')
        resp = {'errcode': 'MR_BAD_USER_REQUEST',
                'error': form.errors}
        return make_response(jsonify(resp), 400)
        # for fieldName, errorMessages in form.errors.items():
        #     for err in errorMessages:
        #         # return error to user


# TODO: - ADJUST RETURN STATEMENTS
#       - DOCUMENTATION
@app.route('/token', methods=['GET', 'POST'])
@auth.login_required
def token():
    tokens.tokens.load()

    data = False
    one_time = False
    ex_date = None
    if request.method == 'GET':
        return str(tokens.tokens)
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            if 'ex_date' in data:
                ex_date = data['ex_date']
            if 'one_time' in data:
                one_time = data['one_time']
        return str(tokens.tokens.new(ex_date=ex_date,
                                     one_time=one_time))
    abort(400)


@app.route('/token/<token>', methods=['GET', 'PUT'])
@auth.login_required
def token_status(token):
    tokens.tokens.load()
    data = False
    if request.method == 'GET':
        return str(tokens.tokens.get_token(token))
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        if data:
            if data['disable'] and tokens.tokens.disable(token):
                return '{} disabled'.format(token)
            return '{} does not exist or is already disabled'.format(token)
    abort(400)
