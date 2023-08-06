from distutils.version import LooseVersion
import argparse
import os
import re
import sys
import logging


log_format = '%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

log = logging.getLogger(__name__)


try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
conf = ConfigParser()

def get_args(arguments=None):
    parser = argparse.ArgumentParser(
        description='Helps to manage version using '
                    'a LooseVersion schema similar '
                    'to 1.1.1.dev1')

    parser.add_argument('-d', '--dev',
                        action='store_true',
                        dest='dev',
                        help='Increase version by one.')

    parser.add_argument('-p', '--patch',
                        action='store_true',
                        dest='patch',
                        help='Increase version by one.')

    parser.add_argument('-m', '--minor',
                        action='store_true',
                        dest='minor',
                        help='Increase version by one.')

    parser.add_argument('-M', '--major',
                        action='store_true',
                        dest='major',
                        help='Increase version by one.')

    parser.add_argument('--set',
                        action='store',
                        dest='set',
                        type=str,
                        default='0',
                        help='Set version to a certain value.')

    parser.add_argument('--release',
                        action='store_true',
                        dest='release',
                        help='Increase version by one.')

    args = parser.parse_args(args=arguments)
    if args.dev and args.release:
        parser.print_help()
        parser.exit()

    return args


class LooseVersionManager(LooseVersion):

    def __init__(self, vstring, files):
        super().__init__(vstring=vstring)
        self.files = files
        self.previous_version = self.vstring
        self.args = get_args()
        self._check_for_mismatch()

    def __call__(self):
        if self.args.dev:
            self._up_dev()
        elif self.args.patch:
            self._up_patch()
        elif self.args.minor:
            self._up_minor()
        elif self.args.major:
            self._up_major()
        elif self.args.set != '0':
            self._set()
        else:
            self._recompile()

    def _check_for_mismatch(self):
        for _file in self.files:
            this_folder = os.getcwd()
            with open(os.path.join(this_folder, _file), 'r') as f:
                try:
                    assert self.vstring in f.read()
                except AssertionError:
                    log.critical("File \"{:s}\" does not contain the "
                                 "correct version. Please fix it by hand."
                                 "".format(_file))
                    log.info("Valid version is: {:s}".format(self.vstring))
                    sys.exit(0)

    def _set(self):
        comparison = self._cmp(self.args.set)
        if comparison == 0:
            log.warning('The new version is the same as old. Nothing to do.')
            return
        else:
            self.parse(self.args.set)

            if comparison == -1:
                log.warning("Increasing version from {:s} to {:s}".format(
                    self.previous_version,
                    self.vstring))
            else:
                log.warning("Reducing version from {:s} to {:s}".format(
                    self.previous_version,
                    self.vstring))
            self._update_files()

    def _recompile(self):
        if self.args.release:
            if len(self.version) > 3:
                self.version = self.version[:3]

            new_version = '.'.join([str(i) for i in self.version])
        else:
            new_version = '.'.join([str(i) for i in self.version])
            new_version = re.sub('dev.', 'dev', new_version)

        assert isinstance(new_version, str)
        self.parse(vstring=new_version)
        self._update_files()
        log.debug('Recompile version: New version: {:s}'.format(self.vstring))

    def _update_files(self):
        for _file in self.files:
            log.debug('Updating version on: {:s} to {:s}'.format(_file,
                                                                 self.vstring))
            this_folder = os.getcwd()
            log.debug('This folder: {:s}'.format(this_folder))
            assert os.path.isfile(os.path.join(this_folder, _file))
            new_content = None
            with open(os.path.join(this_folder, _file), 'r') as f:
                content = f.read()
                new_content = re.sub(self.previous_version,
                                     self.vstring,
                                     content)
            assert new_content is not None

            with open(os.path.join(this_folder, _file), 'w') as f:
                f.write(new_content)

        self.previous_version = self.vstring

    def _up_dev(self):
        if len(self.version) == 3:
            self._up_patch()
            self.version.append('dev')
            self.version.append(1)
            self._recompile()
        elif len(self.version) == 5:
            if self.version[3] == 'dev' and isinstance(self.version[4], int):
                self.version[4] += 1
                self._recompile()

    def _reset_dev(self):
        if len(self.version) == 5:
            self.version[4] = 1

    def _up_patch(self):
        self.version[2] += 1
        if not self.args.dev:
            self._reset_dev()
        self._recompile()

    def _up_minor(self):
        self.version[1] += 1
        self.version[2] = 0
        self._reset_dev()
        self._recompile()

    def _up_major(self):
        self.version[0] += 1
        self.version[1] = 0
        self.version[2] = 0
        self._reset_dev()
        self._recompile()


def run():
    this_folder = os.getcwd()
    if os.path.isfile(os.path.join(this_folder, '.vmconf')):
        conf.read(['setup.cfg', os.path.join(this_folder, '.vmconf')])
        files = dict(conf.items('files'))
        file_list = files['files_to_edit'].split(" ")

        metadata = dict(conf.items('metadata'))

        version = LooseVersionManager(metadata['version'], files=file_list)

        version()
        log.info('Current version is: {:s}'.format(version.vstring))

    else:
        log.error('Expecting a ".vmconf" file in current directory')
        log.info('Creating an empty .vmconf file.')
        with open(os.path.join(this_folder, '.vmconf'), 'w') as f:
            f.write("[files]\nfiles_to_edit = setup.cfg version.py\n")


if __name__ == '__main__':
    run()

