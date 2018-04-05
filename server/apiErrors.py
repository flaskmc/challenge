from customExceptions import InputError
from flask import Blueprint, jsonify

apiErrors = Blueprint('apiErrors', __name__)

@apiErrors.app_errorhandler(InputError)
def handle_input_error(error):
    status_code = 400
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'InputError',
            'message': 'Input parameter values are invalid. Please try with different input.'
        }
    }

    #!!! ADD LOGGING !!!
    
    return jsonify(response), status_code


@apiErrors.app_errorhandler(Exception)
def handle_unexpected_error(error):
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred. Please try again later.'
        }
    }

    #!!! ADD LOGGING !!!

    return jsonify(response), status_code