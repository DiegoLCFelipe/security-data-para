from datetime import datetime

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

now = datetime.now()

class LogHandler:

  def __init__(self, error_file_path='error.log', info_file_path='info.log'):
    self._error_file_path = error_file_path
    self._error_file = open(self._error_file_path, 'w')
    self._info_file_path = info_file_path
    self._info_file = open(self._info_file_path, 'w')

  def log_info_timestamp(self, info_message):
    self._log_info(f'{now.strftime("%d/%m/%Y %H:%M:%S")} - {info_message}')

  def log_error_timestamp(self, error_message):
    self._log_error(f'{now.strftime("%d/%m/%Y %H:%M:%S")} - {error_message}')

  def _log_error(self, error_message):
    print(f'{FAIL}Logging error: {error_message}{ENDC}')
    self._error_file.write(error_message)
    self._error_file.write('\n')

  def _log_info(self, info_message):
    print(f'{OKGREEN}Logging info: {info_message}{ENDC}')
    self._info_file.write(info_message)
    self._info_file.write('\n')
    
