import logging

# Configure the error logger
error_log_filename = 'error_log.log'
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

error_handler = logging.FileHandler(error_log_filename)
error_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
error_logger.addHandler(error_handler)

# Configure the info logger
info_log_filename = 'info_log.log'
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)

info_handler = logging.FileHandler(info_log_filename)
info_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
info_logger.addHandler(info_handler)

# Configure the debug logger
debug_log_filename = 'debug_log.log'
debug_logger = logging.getLogger('debug_logger')
debug_logger.setLevel(logging.DEBUG)

debug_handler = logging.FileHandler(debug_log_filename)
debug_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
debug_logger.addHandler(debug_handler)