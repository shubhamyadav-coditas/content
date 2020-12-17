"""
Bitcoin Abuse Integration for Cortex XSOAR - Unit Tests file
"""

from BitcoinAbuse import *
import json
import io

SERVER_URL = 'https://www.bitcoinabuse.com/api/'

client = BitcoinAbuseClient(
    api_key='',
    verify=False,
    proxy=False
)


def util_load_json(path):
    with io.open(path, mode='r', encoding='utf-8') as f:
        return json.loads(f.read())


def test_report_address_command_success(requests_mock):
    """
    Given:
     - Valid bitcoin address to report

    When:
     - Reporting the valid address to Bitcoin Abuse Api succeeded

    Then:
     - Ensure the command runs successfully
     - Verify expected results are returned.
    """
    mock_response = util_load_json('test_data/successful_bitcoin_report_address_response.json.json')
    valid_report_address = util_load_json('test_data/valid_bitcoin_report_address.json')
    requests_mock.post(
        'https://www.bitcoinabuse.com/api/reports/create',
        json=mock_response
    )
    assert report_address_command(client,
                                  valid_report_address) == 'Bitcoin address 12xfas41 by abuse bitcoin user ' \
                                                           'blabla@blabla.net was reported to ' \
                                                           'BitcoinAbuse API'


def test_report_address_command_failure(requests_mock):
    """
    Given:
     - Valid bitcoin address to report

    When:
     - Reporting the valid address to Bitcoin Abuse Api failed

    Then:
     - Ensure the command fails to run
     - Verify expected results are returned.
    """
    mock_response = util_load_json('test_data/failure_bitcoin_report_address_response.json.json')
    valid_report_address = util_load_json('test_data/valid_bitcoin_report_address.json.json.json')
    requests_mock.post(
        'https://www.bitcoinabuse.com/api/reports/create',
        json=mock_response
    )
    try:
        report_address_command(client, valid_report_address)
        raise AssertionError('report address command should fail when not given success response from api')
    except DemistoException as error:
        assert error.message == f'bitcoin report address did not succeed, response was {mock_response}'


def test_report_address_command_success_type_other(requests_mock):
    """
    Given:
     - Valid bitcoin address with abuse_type 'other' to report

    When:
     - Reporting the valid address to Bitcoin Abuse Api succeeded

    Then:
     - Ensure the command runs successfully
     - Verify expected results are returned.
    """
    mock_response = util_load_json('test_data/successful_bitcoin_report_address_response.json.json')
    valid_report_address_other_type = util_load_json(
        'test_data/valid_bitcoin_report_address_with_other_abuse_type.json.json.json')
    requests_mock.post(
        'https://www.bitcoinabuse.com/api/reports/create',
        json=mock_response
    )
    assert report_address_command(client,
                                  valid_report_address_other_type) == 'Bitcoin address 12xfas41 by abuse bitcoin ' \
                                                                      'user blabla@blabla.net was reported to ' \
                                                                      'BitcoinAbuse API'


def test_report_address_command_failure_type_other():
    """
    Given:
     - Bitcoin address with abuse_type 'other' missing abuse_type_other description to report

    When:
     - Trying to report the address to Bitcoin Abuse Api

    Then:
     - Ensure the command fails to run
     - Verify error message which indicates missing abuse_type_other is returned
    """
    invalid_report_address_other_type_missing = util_load_json(
        'test_data/invalid_bitcoin_report_address_other_type_missing.json.json')
    try:
        report_address_command(client, invalid_report_address_other_type_missing)
        raise AssertionError('report address command should fail when type is other and no abuse_type_other was given')
    except DemistoException as error:
        assert error.message == 'Bitcoin Abuse: abuse_type_other is mandatory when abuse type is other'


def test_report_address_command_failure_unknown_type():
    """
    Given:
     - Bitcoin address with unknown abuse_type

    When:
     - Trying to report the address to Bitcoin Abuse Api

    Then:
     - Ensure the command fails to run
     - Verify error message which indicates the abuse_type is unknown
    """
    failure_report_address_unknown_type = util_load_json(
        'test_data/invalid_bitcoin_report_address_unknown_type.json.json.json')
    try:
        report_address_command(client, failure_report_address_unknown_type)
        raise AssertionError('report address command should fail when not given a known type')
    except DemistoException as error:
        assert error.message == 'Bitcoin Abuse: invalid type of abuse, please insert a correct abuse type'


def test_first_fetch_url():
    """
    Given:
     - Request for url to fetch indicators

    When:
     - Trying to fetch indicators for first time

    Then:
     - Ensure the url returned is according to initial_fetch_interval param
    """
    assert build_fetch_indicators_url_prefix(False, '30d') == 'download/30d'


def test_fetch_url_after_first_fetch():
    """
    Given:
     - Request for url to fetch indicators

    When:
     - Trying to fetch indicators again after first fetch

    Then:
     - Ensure the url returned is 'download/1d' because first fetch was already made
    """
    assert build_fetch_indicators_url_prefix(True, '30d') == 'download/1d'
