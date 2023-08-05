import argparse
import asyncio
import logging.config
import multiprocessing
import operator
import os
import signal
import sys
import time
from functools import partial, reduce
from urllib.parse import splittype  # type: ignore
from urllib.request import urlopen

from . import utils
from .core import command, plugin
from .core.config import Config
from .core.context import Context, GroupResolver

parser = argparse.ArgumentParser(prefix_chars='-+')

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('+g', '++groups', nargs='+', action='append',
                   metavar='GROUP', help='Run groups')
group.add_argument('-g', '--groups', nargs='*', action='append',
                   dest='exclude_groups',
                   metavar='GROUP', help='Run all exclude groups')

parser.add_argument('-i', '--interact', action='store_true')
parser.add_argument('-I', '--interact-kernel', action='store_true')
parser.add_argument('-l', '--logging', help='logging level')


class PidFileType(argparse.FileType):
    def __call__(self, string):
        f = super().__call__(string)
        with f:
            f.write(str(os.getpid()))
        return f


parser.add_argument(
    '--pid-file', help='Process ID file',
    type=PidFileType('w'))

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


context = Context(Config())


def main(*config_files, args=None, config_dirs=(),
         commands=(), config_dict=None):
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
    context.config.search_dirs.extend(config_dirs)

    plugins = plugin.search_plugins()
    for i in plugins:
        i.add_arguments(parser)

    if args is None:
        args, argv = parser.parse_known_args()
        cmds = list(commands)
        while argv and not argv[0].startswith('-'):
            cmds.append(argv.pop(0))
        if getattr(args, 'config', None):
            config_files += tuple(args.config)
        if getattr(args, 'config_stdin', None):
            assert not args.interact, 'Can not be used --config-stdin' \
                                      ' with --interact'
            config_dict = utils.load_from_fd(sys.stdin.buffer)
        if args.logging:
            logging.basicConfig(level=args.logging.upper())
    else:
        cmds, argv = list(commands), []

    config = context.config
    plugins.extend(plugin.search_plugins(*cmds))
    for p in plugins:
        config.load(*p.configs)
        config.update(p.get_config())
    cmds = [cmd for cmd in cmds if cmd not in sys.modules]

    config.load(*config_files)
    config_dict and config.update(config_dict)

    def sum_g(list_groups):
        if list_groups:
            return set(reduce(operator.add, list_groups))

    run = partial(
        loop_run,
        group_resolver=GroupResolver(
            include=sum_g(args.groups),
            exclude=sum_g(args.exclude_groups),
            all_groups=args.exclude_groups is not None,
            default=True,
        ), cmds=cmds, argv=argv, ns=args)

    try:
        if args.interact:
            from .core.interact import shell
            args.print = lambda *args: None
            shell(run)
        elif args.interact_kernel:
            from .core.interact import kernel
            kernel(run)
        else:
            run()
    finally:
        sig = signal.SIGTERM
        while multiprocessing.active_children():
            for p in multiprocessing.active_children():
                os.kill(p.pid, sig)
            time.sleep(0.3)
            print('killall children')
            sig = signal.SIGKILL


def loop_run(
    conf=None, future=None,
    group_resolver=None,
    ns=None, cmds=None,
    argv=None, loop=None,
):
    loop = loop or asyncio.get_event_loop()
    if conf:
        context.set_config(conf)
    if loop is not None:
        context.set_loop(loop)
    if group_resolver is not None:
        context.set_group_resolver(group_resolver)

    cmds = cmds or ['run_forever']
    with utils.monkey_close(loop), context:
        if future is not None:
            future.set_result(context)
        for cmd in cmds:
            try:
                result = command.run(cmd, context, argv=argv, ns=ns)
            except command.CommandNotFound:
                print('Command {} not found'.format(cmd))
                continue
            if result is not None:
                print('{} => {}'.format(cmd, result))
        if hasattr(loop, 'shutdown_asyncgens'):
            loop.run_until_complete(loop.shutdown_asyncgens())


class UriType(argparse.FileType):
    def __call__(self, string):
        t, path = splittype(string)
        if not t:
            return super().__call__(string)
        return urlopen(string)


def main_with_conf(*args, **kwargs):
    parser.add_argument(
        '-c', '--config', nargs='+',
        type=UriType('r', encoding='utf-8'))
    parser.add_argument('--config-stdin', action='store_true')
    main(*args, **kwargs)


if __name__ == '__main__':
    main_with_conf()
