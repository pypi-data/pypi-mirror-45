import asyncio
import functools
import itertools
import sys
import os

import appdirs
import aiohttp
import stringcase
import thesaurus

from ruamel import yaml
from colorama import Fore

from precept import format_table, CliApp, Argument, Command, spinner, colorize

from top_drawer._version import __version__
from top_drawer._validations import validate_pypi, validate_npm

UNDONE = 'undone'


def get_synonyms(word, definition=0, relevance=(1, 2, 3)):
    w = thesaurus.Word(word)
    synonyms = w.synonyms(definition,
                          relevance=list(relevance))
    if definition == 'all' or isinstance(definition, list):
        synonyms = set(itertools.chain(*synonyms))

    return synonyms


def format_valid(valid):
    if valid:
        return colorize('VALID', fg=Fore.GREEN)
    return colorize('INVALID', fg=Fore.RED)


class TopDrawer(CliApp):
    """
    Search for synonyms and validate if the name is available on pypi or npm.
    """
    _prog_name = 'top-drawer'
    _version = __version__

    def __init__(self):
        super().__init__()
        self._cache_file = os.path.join(
            appdirs.user_cache_dir(self._prog_name),
            'validations.yml'
        )

    def read_cached_names(self):
        if os.path.exists(self._cache_file):
            self.logger.debug(f'Using cache file: {self._cache_file}')
            with open(self._cache_file) as f:
                cached_names = yaml.load(f, Loader=yaml.RoundTripLoader)
        else:
            os.makedirs(os.path.dirname(self._cache_file), exist_ok=True)
            cached_names = {}
        return cached_names

    def write_cached_names(self, obj):
        self.logger.debug(f'Writing cache file: {self._cache_file}')
        with open(self._cache_file, 'w+') as cf:
            yaml.dump(obj, cf, Dumper=yaml.RoundTripDumper)

    @Command(
        Argument(['word'], {
            'help': 'The word to generate synonyms for'
        }),
        Argument(['-c', '--casing'], {
            'choices': ['snakecase', 'spinalcase'],
            'default': 'spinalcase',
            'help': 'The casing to apply to synonyms'
        }),
        Argument(['--pypi'], {
            'help': 'Disable validation on pypi',
            'action': 'store_false'
        }),
        Argument(['--npm'], {
            'help': 'Disable validation on npm',
            'action': 'store_false'
        }),
        Argument(['-f', '--full'], {
            'help': 'Include the invalids in the output',
            'action': 'store_true'
        }),
        Argument(['--definition'], {
            'help': 'Set to a number representing the tab of the search result'
                    ' on thesaurus.com or `all`.',
            'default': '0'
        }),
        description='Search for valid synonyms of the provided word.'
    )
    async def search(self, word, casing, pypi, npm, full, definition):
        ns = {
            'message': '',
            'done': False
        }

        def message():
            return ns['message']

        def is_done():
            return ns['done']

        cached_names = self.read_cached_names()

        async def operate():
            await asyncio.sleep(0.001)  # Make the spinner start
            casing_method = getattr(stringcase, casing)
            synonyms = [
                casing_method(x)
                for x in get_synonyms(
                    word,
                    int(definition)
                    if definition != 'all' else definition
                )
            ]

            self.logger.debug(f'Found {len(synonyms)} synonyms')
            validations = {
                s: {
                    'pypi': UNDONE,
                    'npm': UNDONE
                }
                for s in synonyms
            }

            def _done(future, synonym='', validator=''):
                validations[synonym][validator] = future.result()

            ns['message'] = 'Validating synonyms ...'
            async with aiohttp.ClientSession() as session:
                tasks = []
                for s in synonyms:
                    cached = cached_names.get(s)

                    if cached:
                        validations[s] = cached

                    if validations[s]['pypi'] == UNDONE and pypi:
                        t = asyncio.ensure_future(validate_pypi(
                            session, s
                        ))
                        # noinspection PyTypeChecker
                        t.add_done_callback(
                            functools.partial(_done,
                                              synonym=s,
                                              validator='pypi')
                        )
                        tasks.append(t)

                    if validations[s]['npm'] == UNDONE and npm:
                        t = asyncio.ensure_future(validate_npm(
                            session, s
                        ))
                        # noinspection PyTypeChecker
                        t.add_done_callback(
                            functools.partial(_done,
                                              synonym=s,
                                              validator='npm')
                        )
                        tasks.append(t)
                await asyncio.gather(*tasks)
                updated_cache = cached_names.copy()
                updated_cache.update(validations)
                self.write_cached_names(updated_cache)

            ns['done'] = True
            await asyncio.sleep(0.30)  # Wait for the spinner...
            print('\n\n', file=sys.stderr)
            valids = [
                k for k, v in validations.items()
                if (not pypi or v['pypi']) and (not npm or v['npm'])
            ]
            self.logger.debug(f'{len(valids)} valid out of {len(synonyms)}')
            await asyncio.sleep(0.30)
            if not valids:
                print('No valid results!')
                sys.exit(1)
            if not full:
                print('\n'.join(format_table(valids)))
            else:
                def formatter(key):
                    value = validations.get(key.strip())  # The key is centered
                    if (not pypi or value['pypi']) and \
                            (not npm or value['npm']):
                        fore = Fore.GREEN
                    else:
                        fore = Fore.RED
                    return colorize(key, fg=fore)
                print('\n'.join(format_table(
                    list(validations.keys()), formatting=formatter)))

        sp = spinner(is_done, message=message)
        op = operate()
        await asyncio.gather(sp, op)

    @Command(
        Argument(['word'], {
            'help': 'The word to generate synonyms'
        }),
        Argument(['--pypi'], {
            'help': 'Disable validation on pypi',
            'action': 'store_false'
        }),
        Argument(['--npm'], {
            'help': 'Disable validation on npm',
            'action': 'store_false'
        }),
        description='Validate a name is available'
    )
    async def validate(self, word, pypi, npm):
        cached_names = self.read_cached_names()
        cached = cached_names.setdefault(word, {})

        async with aiohttp.ClientSession() as session:
            if pypi:
                pypi_valid = cached.get('pypi')
                if pypi_valid is None or pypi_valid == UNDONE:
                    pypi_valid = await validate_pypi(session, word)
                    cached_names[word]['pypi'] = pypi_valid
                print(f'pypi: {format_valid(pypi_valid)}')
            if npm:
                npm_valid = cached.get('npm')
                if npm_valid is None or npm_valid == UNDONE:
                    npm_valid = await validate_npm(session, word)
                    cached_names[word]['npm'] = npm_valid
                print(f'npm: {format_valid(npm_valid)}')

        self.write_cached_names(cached_names)

    @Command(
        description='Clear the validations cache.'
    )
    async def clear_cache(self):
        os.remove(self._cache_file)


def cli():
    c = TopDrawer()
    c.start()


if __name__ == '__main__':
    cli()
