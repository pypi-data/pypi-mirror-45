#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""cli: Command line argument parser."""

from __future__ import print_function

import sys
import argparse

from snippy.constants import Constants as Const
from snippy.config.source.base import ConfigSourceBase
from snippy.content.parser import Parser
from snippy.meta import __homepage__
from snippy.meta import __version__


class Cli(ConfigSourceBase):
    """Command line argument parser."""

    ARGS_COPYRIGHT = (
        'Snippy version ' + __version__ + ' - license GNU AGPLv3 or later',
        'Copyright 2017-2019 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
        'Homepage ' + __homepage__
    )
    ARGS_USAGE = ('snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]')
    ARGS_CATEGORY = (
        '  --snippets                    operate snippets (default)',
        '  --solutions                   operate solutions',
        '  --references                  operate references',
        '  --all                         operate all content (search only)'
    )
    ARGS_EDITOR = (
        '  -c, --content CONTENT         define example content',
        '  -b, --brief BRIEF             define content brief description',
        '  -g, --groups [GROUP,...]      define comma separated list of groups',
        '  -t, --tags [TAG,...]          define comma separated list of tags',
        '  -l, --links [LINK ...]        define space separated list of links',
        '  -d, --digest DIGEST           idenfity content with digest',
        '  -u, --uuid UUID               idenfity content with uuid',
        '  --editor                      use vi editor to manage content',
        '  --no-editor                   do not use vi editor',
    )
    ARGS_SEARCH = (
        '  --scat [CATEGORY,...]         search keywords only from categories',
        '  --sall [KW,...]               search keywords from all fields',
        '  --stag [KW,...]               search keywords only from tags',
        '  --sgrp [KW,...]               search keywords only from groups',
        '  --filter REGEXP               filter search result with regexp',
        '  --limit INT                   maximum number of search results',
        '  --no-ansi                     remove ANSI characters from output'
    )
    ARGS_MIGRATE = (
        '  -f, --file FILE               define file for operation',
        '  --defaults                    migrate category specific defaults',
        '  --template                    migrate category specific template',
    )
    ARGS_EPILOG = (
        'symbols:',
        '    $    snippet',
        '    :    solution',
        '    >    reference',
        '    @    group',
        '    #    tag',
        '',
        'examples:',
        '    Import default content.',
        '      $ snippy import --snippets --defaults',
        '      $ snippy import --solutions --defaults',
        '      $ snippy import --references --defaults',
        '',
        '    List all snippets.',
        '      $ snippy search --snippets --sall .',
        '',
        '    List more examples.',
        '      $ snippy --help examples',
        '') + ARGS_COPYRIGHT

    ARGS_EXAMPLES = (
        'examples:',
        '    Creating new content:',
        '      $ snippy create --snippets --editor',
        '      $ snippy create --snippets -c \'docker ps\' -b \'list containers\' -t docker,moby',
        '',
        '    Searching and filtering content:',
        '      $ snippy search --snippets --sall docker,moby',
        '      $ snippy search --snippets --sall .',
        '      $ snippy search --snippets --sall . --no-ansi | grep \'\\$\' | sort',
        '      $ snippy search --solutions --sall .',
        '      $ snippy search --solutions --sall . | grep -Ev \'[^\\s]+:\'',
        '      $ snippy search --all --sall . --filter \'\\$?.*docker\'',
        '      $ snippy search --all --sall . --no-ansi | grep -E \'[0-9]+\\.\\s\'',
        '',
        '    Updating content:',
        '      $ snippy update --snippets -d 44afdd0c59e17159',
        '      $ snippy update --snippets -c \'docker ps\'',
        '',
        '    Deleting content:',
        '      $ snippy delete --snippets -d 44afdd0c59e17159',
        '      $ snippy delete --snippets -c \'docker ps\'',
        '',
        '    Migrating default content:',
        '      $ snippy import --snippets --defaults',
        '      $ snippy import --solutions --defaults',
        '      $ snippy import --references --defaults',
        '',
        '    Migrating content templates:',
        '      $ snippy export --solutions --template',
        '      $ snippy import --solutions --template',
        '      $ snippy import --solutions -f solution-template.txt',
        '',
        '    Migrating specific content:',
        '      $ snippy export -d eb792f8015ace749',
        '      $ snippy import -d eb792f8015ace749 -f howto-debug-elastic-beats.mkdn',
        '',
        '    Migrating content:',
        '      $ snippy export --snippets -f snippets.yaml',
        '      $ snippy export --snippets -f snippets.json',
        '      $ snippy export --snippets -f snippets.text',
        '      $ snippy import --snippets -f snippets.yaml',
        '      $ snippy export --solutions -f solutions.yaml',
        '      $ snippy import --solutions -f solutions.yaml',
        '') + ARGS_COPYRIGHT

    def __init__(self, args):
        super(Cli, self).__init__(self.__class__.__name__)
        if args is None:
            args = []
        args = args[1:]  # Remove the first option that is the program name.
        self._read_conf(args)

    def _read_conf(self, args):  # pylint: disable=too-many-statements,too-many-locals
        """Parse command line arguments.

        Args:
            args (list): Command line arguments from sys.argv.

        Returns:
            dict: Command line arguments.
        """

        arguments = {}
        parser = CustomArgumentParser(
            prog='snippy',
            add_help=False,
            usage=Cli.ARGS_USAGE,
            epilog=Const.NEWLINE.join(Cli.ARGS_EPILOG),
            formatter_class=argparse.RawTextHelpFormatter
        )

        # content options
        content = parser.add_argument_group(title='content category', description=Const.NEWLINE.join(Cli.ARGS_CATEGORY))
        content_meg = content.add_mutually_exclusive_group()
        content_meg.add_argument('--snippet', '--snippets', action='store_const', dest='category', const='snippet', help=argparse.SUPPRESS)
        content_meg.add_argument('--solution', '--solutions', action='store_const', dest='category', const='solution', help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        content_meg.add_argument('--reference', '--references', action='store_const', dest='category', const='reference', help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        content_meg.add_argument('--all', action='store_const', dest='category', const='all', help=argparse.SUPPRESS)
        content_meg.set_defaults(category=Const.SNIPPET)

        # editing options
        options = parser.add_argument_group(title='edit options', description=Const.NEWLINE.join(Cli.ARGS_EDITOR))
        options.add_argument('-c', '--content', type=Parser.to_unicode, dest='data', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('-b', '--brief', type=Parser.to_unicode, default=Const.EMPTY, help=argparse.SUPPRESS)
        options.add_argument('-g', '--groups', nargs='*', type=Parser.to_unicode, default=Const.DEFAULT_GROUPS, help=argparse.SUPPRESS)
        options.add_argument('-t', '--tags', nargs='*', type=Parser.to_unicode, default=[], help=argparse.SUPPRESS)
        options.add_argument('-l', '--links', nargs='*', type=Parser.to_unicode, default=[], help=argparse.SUPPRESS)
        options.add_argument('-d', '--digest', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('-u', '--uuid', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        options.add_argument('--editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('--no-editor', action='store_true', default=False, help=argparse.SUPPRESS)
        options.add_argument('--format', nargs='?', choices=(Const.CONTENT_FORMAT_MKDN, Const.CONTENT_FORMAT_TEXT), default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long

        # search options
        search = parser.add_argument_group(title='search options', description=Const.NEWLINE.join(Cli.ARGS_SEARCH))
        search_meg = search.add_mutually_exclusive_group()
        search_meg.add_argument('--sall', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search_meg.add_argument('--stag', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--scat', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--sgrp', nargs='*', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--filter', type=Parser.to_unicode, dest='search_filter', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        search.add_argument('--limit', type=int, default=Cli.LIMIT_DEFAULT_CLI, help=argparse.SUPPRESS)

        # migration options
        migrat = parser.add_argument_group(title='migration options', description=Const.NEWLINE.join(Cli.ARGS_MIGRATE))
        migrat_meg = migrat.add_mutually_exclusive_group()
        migrat_meg.add_argument('-f', '--file', type=Parser.to_unicode, dest='filename', default='', help=argparse.SUPPRESS)
        migrat_meg.add_argument('--defaults', action='store_true', default=False, help=argparse.SUPPRESS)
        migrat_meg.add_argument('--template', action='store_true', default=False, help=argparse.SUPPRESS)

        # support options
        support = parser.add_argument_group(title='support options')
        support.add_argument('-v', '--version', nargs=0, action=CustomVersionAction, help=argparse.SUPPRESS)
        support.add_argument('-vv', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        support.add_argument('-q', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        support.add_argument('--debug', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        support.add_argument('--profile', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        support.add_argument('--no-ansi', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        support.add_argument('--log-json', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        support.add_argument('--log-msg-max', type=int, default=argparse.SUPPRESS, help=argparse.SUPPRESS)

        # server options
        server = parser.add_argument_group(title='server options')
        server.add_argument('--server-host', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-minify-json', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-base-path-rest', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-ssl-cert', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-ssl-key', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-ssl-ca-cert', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-readonly', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--server-healthcheck', action='store_true', default=argparse.SUPPRESS, help=argparse.SUPPRESS)

        # storage options
        server.add_argument('--storage-path', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-type', type=Parser.to_unicode, choices=Const.STORAGES, default=argparse.SUPPRESS, help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long
        server.add_argument('--storage-host', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-user', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-password', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-database', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-ssl-cert', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-ssl-key', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        server.add_argument('--storage-ssl-ca-cert', type=Parser.to_unicode, default=argparse.SUPPRESS, help=argparse.SUPPRESS)

        # The Argparse module will exit with support options help or version
        # and when argument parsing fails. The --no-ansi flag is needed before
        # custom help action. Because of this, help and positional arguments
        # are not included when the first set of options is parsed to read the
        # needed flags for the custom help command.
        #
        # Positional arguments are not included into the first parsing in
        # order to get the --help <option> combination to work. The <option>
        # after the --help would be parsed as positional argument and that
        # would fail the parsing.
        #
        # There is a custom shortcut to allow quick search without any search
        # options. When the shortcut is used, the search is made based on the
        # ``--sall`` option.
        try:
            arguments, unknown_args = parser.parse_known_args(args)
            arguments = vars(arguments)

            # positional arguments
            operations = ('create', 'search', 'update', 'delete', 'export', 'import')
            parser.add_argument('operation', nargs='?', choices=operations, metavar='  {create,search,update,delete,export,import}')

            # support options
            support.add_argument('-h', '--help', nargs='?', action=CustomHelpAction, no_ansi=arguments.get('no_ansi', False), help=argparse.SUPPRESS)  # noqa pylint: disable=line-too-long

            # Positional arguments and support options that are not yet parsed.
            valid_args = operations + ('-h', '--help')

            if self._use_search_shortcut(unknown_args, valid_args):
                arguments = vars(parser.parse_known_args(args)[0])
                arguments['sall'] = unknown_args[1:]
            else:
                arguments = vars(parser.parse_args(args))
            arguments['failure'] = False
            arguments['failure_message'] = ''
        except SystemExit:
            # The Argparse module will automatically print ``--help`` when the
            # SystemExit exception is thrown. The pass from here is for clean
            # exit.
            #
            # Do not add ``--help`` as a default command in Dockerfile after
            # the entrypoint. It can be that all Docker container options are
            # set from environment variables. Default help command makes it
            # hard to handle command line option parsing failures combined with
            # environment variables.
            arguments['failure'] = True
            arguments['failure_message'] = parser.snippy_failure_message
            self._logger.debug('cli: {}'.format(arguments['failure_message']))

        self._set_editor(arguments)
        self._set_format(arguments)

        # Using the tool from command line always updates existing content if
        # it exists (merge). This prevents updating empty values on top of
        # already created content attributes. The example below defines only
        # `tags` attribute on top of existing content.
        #
        # $ snippy update -d f3fd167c64b6f97e --tags new,tags,from,cli
        #
        # The merge option has relevance only in API configuration source
        # where it allows different behaviour between PUT and PATCH methods.
        arguments['merge'] = True
        self.init_conf(arguments)

        # In case of command line usage, tool help is printed if there were
        # no commnad line arguments.
        #
        # In case of server usage, it is normal to configure the server from
        # environment variables and no help is needed.
        if not self.run_server and not args:
            parser.print_help(sys.stdout)
            self.failure = True
            self.failure_message = 'no command line arguments'

    @staticmethod
    def _use_search_shortcut(unknown_args, valid_args):
        """Test if a search shortcut is used.

        Decide if shorcut for content search is used. The argument parsing is
        made in two phases. This method is intended to be used between the
        first and second phase. The unknown arguments are from the first phase
        and the valid arguments are to be validated in the last phase.

        Args:
            unknown_args (list): List of unknown arguments.
            valid_args (list): List of valid arguments.

        Returns:
            bool: True if search shortcut is used.
        """

        if not set(unknown_args).issubset(valid_args) and unknown_args and unknown_args[0] == 'search':
            return True

        return False

    @staticmethod
    def _set_editor(arguments):
        """Enforce editor implicitly.

        The no-editor option always prevents implicit usage of editor.
        In other cases, editor is used by default for create and update
        operations.

        Only if user provided mandatory links for reference or data for
        other content types in create operation, editor is not used by
        default.

        Args:
            arguments (dict): Command line arguments.
        """

        if arguments['failure'] or arguments['no_editor']:
            arguments['editor'] = False
            return

        if arguments['operation'] in (Cli.CREATE, Cli.UPDATE):
            if arguments['category'] == Const.REFERENCE:
                if not arguments['links']:
                    arguments['editor'] = True
            else:
                if 'data' not in arguments:
                    arguments['editor'] = True

    @staticmethod
    def _set_format(arguments):
        """Enforce editor implicitly.

        The default is text format when searching content from command line.
        All other cases default to Markdown format. If user defined the format
        option, it overrides this setting.

        Args:
            arguments (dict): Command line arguments.
        """

        if arguments['failure']:
            arguments['format'] = Const.CONTENT_FORMAT_MKDN
            return

        if 'format' not in arguments and arguments['operation'] == Cli.SEARCH:
            arguments['format'] = Const.CONTENT_FORMAT_TEXT
        elif 'format' not in arguments:
            arguments['format'] = Const.CONTENT_FORMAT_MKDN


class CustomArgumentParser(argparse.ArgumentParser):
    """Customized Argument Parser to get the failure string."""

    def __init__(self, *args, **kwargs):
        """Store custom attrbite to get the error message."""

        self.snippy_failure_message = ''
        super(CustomArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """Store error message to custom attribute."""

        self.snippy_failure_message = message
        super(CustomArgumentParser, self).error(message)


class CustomHelpAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised help action.

    Custom treatment for parameters after the ``--help```option.
    """

    def __init__(self, *args, **kwargs):
        """Store the ``--no-ansi`` option as a custom attribute."""

        self._no_ansi = kwargs.pop('no_ansi', False)
        super(CustomHelpAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised help."""

        if values == 'examples':
            print(Const.NEWLINE.join(Cli.ARGS_EXAMPLES))
        elif values == 'tests':
            from snippy.devel.reference import Reference

            ansi = not self._no_ansi
            test = Reference()
            test.print_tests(ansi)
        else:
            parser.print_help()

        parser.exit()


class CustomVersionAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Customised version action."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Customised version

        Argparse and Python versions below 3.4 print to stderr. In order to
        have consistent functionality between supported Python versions, the
        version must be explicitly printed into stdout.
        """

        print(__version__)

        parser.exit()
