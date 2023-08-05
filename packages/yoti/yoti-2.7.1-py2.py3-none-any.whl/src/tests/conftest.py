# -*- coding: utf-8 -*-
from os.path import dirname, join, abspath

import pytest
from yoti_python_sdk import Client
from yoti_python_sdk.crypto import Crypto

FIXTURES_DIR = join(dirname(abspath(__file__)), 'fixtures')
PEM_FILE_PATH = join(FIXTURES_DIR, 'sdk-test.pem')
ENCRYPTED_TOKEN_FILE_PATH = join(FIXTURES_DIR, 'encrypted_yoti_token.txt')
AUTH_KEY_FILE_PATH = join(FIXTURES_DIR, 'auth_key.txt')
AUTH_DIGEST_FILE_PATH = join(FIXTURES_DIR, 'auth_digest.txt')

YOTI_CLIENT_SDK_ID = '737204aa-d54e-49a4-8bde-26ddbe6d880c'


@pytest.fixture(scope='module')
def client():
    return Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


@pytest.fixture(scope='module')
def crypto():
    with open(PEM_FILE_PATH, 'rb') as pem_file:
        return Crypto(pem_file.read())


@pytest.fixture(scope='module')
def encrypted_request_token():
    with open(ENCRYPTED_TOKEN_FILE_PATH, 'rb') as token_file:
        return token_file.read()


@pytest.fixture(scope='module')
def decrypted_request_token():
    return 'd1JtHdjH-2c161003-cbaf-4080-b2a8-5a6d86577334-3f9d9a9a-' \
           '470c-48e5-8ceb-25cf86674ba4'


@pytest.fixture(scope='module')
def x_yoti_auth_key():
    with open(AUTH_KEY_FILE_PATH, 'r') as auth_key_file:
        return auth_key_file.read()


@pytest.fixture(scope='module')
def x_yoti_auth_digest():
    with open(AUTH_DIGEST_FILE_PATH, 'r') as auth_digest_file:
        return auth_digest_file.read()
