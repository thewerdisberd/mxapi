import logging
import getopt
import sys
import requests

def handle_query_api_error(logger, e):
    logger.debug('Error running query_api {0}'.format(e))
    logging.info('There was an error querying the API')
    logger.debug('Exiting due to error with query_api')
    sys.exit(2)

def handle_parse_data_error(logger, e):
    logger.debug('Error running parse_data'.format(e))
    logging.info('There was an error parsing the returned data')
    logger.debug('Exiting due to error with parse_data')
    sys.exit(2)

def query_api(logger, apikey, command, argument, option=None):

    logger.debug('Entering query_api')
    url = 'https://mxtoolbox.com/api/v1/Lookup/' + command
    if option == None:
        params = {'argument': argument}
        logger.debug('No option chosen in query_api')
    else:
        params = {'argument': argument, 'port': option}
        logger.debug('{0} option chosen in query_api'.format(option))
    headers = {'Authorization': apikey}
    logger.debug('Trying api request')
    try:
        r = requests.get(url, headers=headers, params=params)
    except Exception as e:
        raise
    logger.debug('Finished making api request')
    data = r.text
    return data

def parse_data(logger, command, data):
    logger.debug('Entering parse_data')
    if command == 'a' or command == 'ptr':
        logger.debug('Parsing {0} data'.format(command))
        for x in range(len(json_data['Information'])):
            print('Record {0}'.format(x + 1))
            print('Domain Name:  {0}'.format(json_data['Information'][x]['Domain Name']))
            print('IP Address:   {0}'.format(json_data['Information'][x]['IP Address']))
            print('Record Type:  {0}'.format(json_data['Information'][x]['Type']))
            print()
    if command == 'tcp':
        logger.debug('Parsing {0} data'.format(command))
        print('Scanned: {0}'.format(json_data['CommandArgument']))
        for x in range(len(json_data['Information'])):
            print('Result: {0}'.format(json_data['Information'][x]['Summary']))
            print()
    if command == 'blacklist':
        logger.debug('Parsing {0} data'.format(command))
        print('{0} is on {1} blacklists:'.format(json_data['CommandArgument'], len(json_data['Failed'])))
        for x in range(len(json_data['Failed'])):
            print('    {0}'.format(json_data['Failed'][x]['Name']))
    if command == 'ping':
        logger.debug('Parsing {0} data'.format(command))
        print('Sent ping to {0}'.format(json_data['CommandArgument']))
        for x in range(len(json_data['Information'])):
            print('Status:     {0}'.format(json_data['Information'][x]['Reply']))
            print('IP Address: {0}'.format(json_data['Information'][x]['IP Address']))
            time = json_data['Information'][x]['Time'].replace('&lt;', '')
            print('Time (ms):  {0}'.format(time))
            print()
    if command == 'scan':
        logger.debug('Parsing {0} data'.format(command))
        print('Open ports on {0}'.format(json_data['CommandArgument']))
        for x in range(len(json_data['Information'])):
            if json_data['Information'][x]['Result'] == "Open":
                print('{0} {1}'.format(json_data['Information'][x]['Name'], json_data['Information'][x]['Port']))

def main():

    # Declare variables
    command = ''
    argument = ''
    option = ''

    # Congfigure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_log = logging.FileHandler('mxapi.log')
    file_log.setLevel(logging.DEBUG)
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)
    file_format = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)s:%(levelname)-8s %(message)s')
    console_format = logging.Formatter('[%(asctime)s] %(levelname)-8s - %(message)s')
    file_log.setFormatter(file_format)
    console_log.setFormatter(console_format)
    logger.addHandler(file_log)
    logger.addHandler(console_log)

    # Parse options
    try:
      opts, args = getopt.getopt(sys.argv[1:], 'hc:a:o:', ['help'])
    except getopt.GetoptError as e:
        msg, opt = e
        logger.error('{0} is an invalid option'.format(opt))
        print('Usage:\n\tmxapi.py -c <command> -a <argument> [-o <option>]')
        logger.debug('An invalid option was chosen, {0} - Message: {1}'.format(opt, msg))
        logger.debug('Exiting due to bad option')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-c':
            command = arg
            logger.debug('Set command to {0}'.format(arg))
        elif opt == '-a':
            argument = arg
            logger.debug('Set argument to {0}'.format(arg))
        elif opt == '-u':
            option = arg
            logger.debug('Set option to {0}'.format(arg))
        elif (opt == '--help') or (opt == '-h'):
            print('Usage:\n\tmxapi.py <command> -q <query> -o <option>')
            logger.debug('Only help was run')
            logger.debug('Exiting due to help being run')
            sys.exit(2)

    # Get apikey
    try:
        f = open('apikey.txt', 'r')
    except Exception as e:
        logger.debug('Unable to open apikey.txt - Error: {0}'.format(e))
        logging.info('Unable to open apikey.txt')
        logger.debug('Exiting due to error opening apikey.txt')
        sys.exit(2)
    try:
        apikey = f.read()
    except Exception as e:
        logger.debug('Unable to read apikey - Error: {0}'.format(e))
        logging.info('Unable to read apikey')
        logger.debug('Exiting due to error reading apikey.txt')
        sys.exit(2)
    if '\n' in apikey:
        apikey.replace('\n', '')
        logger.debug('apikey had \\n removed')
    elif '\r\n' in apikey:
        apikey.replace('\r\n', '')
        logger.debug('apikey had \\r\\n removed')

    # Run program
    if command == 'a':
        logger.debug('{0} was the chosen command'.format(command))
        try:
            data = query_api(apikey, command, argument)
        except Exception as e:
            handle_query_api_error(logger, e)
        try:
            parse_data(command, data)
        except Exception as e:
            handle_parse_data_error(logger, e)
        logger.debug('Finished running {0} command'.format(command))
    elif command == 'ptr':
        logger.debug('{0} was the chosen command'.format(command))
        try:
            data = query_api(apikey, command, argument)
        except Exception as e:
            handle_query_api_error(logger, e)
        try:
            parse_data(command, data)
        except Exception as e:
            handle_parse_data_error(logger, e)
        logger.debug('Finished running {0} command'.format(command))
    elif command == 'tcp':
        logger.debug('{0} was the chosen command'.format(command))
        try:
            data = query_api(apikey, command, argument, option=option)
        except Exception as e:
            handle_query_api_error(logger, e)
        try:
            parse_data(command, data)
        except Exception as e:
            handle_parse_data_error(logger, e)
        logger.debug('Finished running {0} command'.format(command))
    elif command == 'blacklist':
        logger.debug('{0} was the chosen command'.format(command))
        try:
            data = query_api(apikey, command, argument)
        except Exception as e:
            handle_query_api_error(logger, e)
        try:
            parse_data(command, data)
        except Exception as e:
            handle_parse_data_error(logger, e)
        logger.debug('Finished running {0} command'.format(command))
    elif command == 'ping':
        logger.debug('{0} was the chosen command'.format(command))
        try:
            data = query_api(apikey, command, argument)
        except Exception as e:
            handle_query_api_error(logger, e)
        try:
            parse_data(command, data)
        except Exception as e:
            handle_parse_data_error(logger, e)
        logger.debug('Finished running {0} command'.format(command))
    elif command == 'scan':
        logger.debug('{0} was the chosen command'.format(command))
        try:
            data = query_api(apikey, command, argument)
        except Exception as e:
            handle_query_api_error(logger, e)
        try:
            parse_data(command, data)
        except Exception as e:
            handle_parse_data_error(logger, e)
        logger.debug('Finished running {0} command'.format(command))

main()
