from distutils.version import LooseVersion
import argparse
import os
import re
import sys


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
        print(self.args)

    def __call__(self):
        if self.args.dev:
            self._up_dev()
        elif self.args.patch:
            self._up_patch()
        elif self.args.minor:
            self._up_minor()
        elif self.args.major:
            self._up_major()
        else:
            self._recompile()

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
        print('recompile version ', self.version, self.vstring)

    def _update_files(self):
        for _file in self.files:
            print(_file, self.vstring)
            this_folder = os.path.abspath(os.path.dirname(__file__))
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


if __name__ == '__main__':

    file_list = ['setup.cfg', 'goodman_pipeline/version.py']
    conf.read([os.path.join(os.getcwd(), 'setup.cfg')])
    metadata = dict(conf.items('metadata'))
    print(metadata['version'])

    ver = LooseVersionManager(metadata['version'], files=file_list)

    # ver.up_dev()
    ver()
    print(ver)


