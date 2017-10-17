#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


class CLIOpts(object):

    options = None

    def __init__(self):
        self.options = self.parse_options()

    @staticmethod
    def parse_options():
        """
        parse CLI options into options dict
        :return: dict
        """
        argparser = argparse.ArgumentParser(
            description='ClickHouse data reader',
            epilog='==============='
        )

        argparser.add_argument(
            '--config-file',
            type=str,
            default='',
            help='Path to config file. Default - not specified'
        )
        argparser.add_argument(
            '--dry',
            action='store_true',
            help='Dry mode - do not do anything that can harm. '
            'Useful for debugging. '
        )
        argparser.add_argument(
            '--daemon',
            action='store_true',
            help='Daemon mode - go to background. '
        )
        argparser.add_argument(
            '--pid-file',
            type=str,
            default='/tmp/reader.pid',
            help='pid file to be used by app in daemon mode'
        )

        argparser.add_argument(
            '--src-server-id',
            type=int,
            default=1,
            help='server_id to be used when reading from src'
        )
        argparser.add_argument(
            '--src-host',
            type=str,
            default='127.0.0.1',
            help='host to be used when reading from src'
        )
        argparser.add_argument(
            '--src-port',
            type=int,
            default=3306,
            help='port to be used when reading from src'
        )
        argparser.add_argument(
            '--src-user',
            type=str,
            default='root',
            help='username to be used when reading from src'
        )
        argparser.add_argument(
            '--src-password',
            type=str,
            default='',
            help='password to be used when reading from src'
        )
        argparser.add_argument(
            '--src-only-schemas',
            type=str,
            default='',
            help='comma-separated list of schemas to be used when reading from src'
        )
        argparser.add_argument(
            '--src-only-tables',
            type=str,
            default='',
            help='comma-separated list of tables to be used when reading from src'
        )
        argparser.add_argument(
            '--src-wait',
            action='store_true',
            help='Wait for new records to come'
        )
        argparser.add_argument(
            '--src-resume',
            action='store_true',
            help='Resume reading from previous position'
        )

        argparser.add_argument(
            '--dst-host',
            type=str,
            default='192.168.74.230',
            help='host to be used when writing to dst'
        )
        argparser.add_argument(
            '--dst-port',
            type=int,
            default=9000,
            help='port to be used when writing to dst'
        )
        argparser.add_argument(
            '--dst-user',
            type=str,
            default='default',
            help='username to be used when writing to dst'
        )
        argparser.add_argument(
            '--dst-password',
            type=str,
            default='',
            help='password to be used when writing to dst'
        )

        args = argparser.parse_args()

        # build options
        return {
            'app-config': {
                'config-file': args.config_file,
                'dry': args.dry,
                'daemon': args.daemon,
                'pid_file': args.pid_file,
            },

            'reader-config': {
                'connection_settings': {
                    'host': args.src_host,
                    'port': args.src_port,
                    'user': args.src_user,
                    'passwd': args.src_password,
                },
                'server_id': args.src_server_id,
                'only_schemas': [x for x in args.src_only_schemas.split(',') if x] if args.src_only_schemas else None,
                'only_tables': [x for x in args.src_only_tables.split(',') if x] if args.src_only_tables else None,
                'blocking': args.src_wait,
                'resume_stream': args.src_resume,
            },

            'writer-config': {
                'host': args.dst_host,
                'port': args.dst_port,
                'user': args.dst_user,
                'password': args.dst_password,
            },
        }