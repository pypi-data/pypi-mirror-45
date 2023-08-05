if __name__ == '__main__':
    import sys
    from common_utils.log import init_stream_log
    logger = init_stream_log()
    if len(sys.argv) > 2:
        func = getattr(sys.modules[__name__], sys.argv[1])
        func(*sys.argv[2:])
    else:
        print >> sys.stderr, sys.argv[0] + 'cmd [cmd_args]'
        logger.info(sys.argv[0] + 'cmd [cmd_args]')