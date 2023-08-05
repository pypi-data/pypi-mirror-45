from pathlib import Path
import shutil
import os


class Command:
    @classmethod
    def exec(cls, cmd='help', *args):
        return getattr(cls(), cmd, Command.help)(*args)

    @staticmethod
    def create_setup(*args):
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write('''import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Detail see: https://packaging.python.org/tutorials/packaging-projects/#creating-setup-pypip install -i https://test.pypi.org/simple/ pysetup
setuptools.setup(
    name='<package_name>',
    version='<version>',
    author='<author>',
    author_email='<author_email>',
    description='<description>',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='<url>',
    packages=setuptools.find_packages(exclude=('<directory_name>',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['<package_name>'],
    entry_points={
        'console_scripts': ['<command>=<package>.<filename>:<function>']
    },
)
''')
        return 'Successful!'

    @staticmethod
    def upload(*args):
        if len(args) == 2: username, password = args
        else: return 'Error: please check the command.'
        Command.package()
        result = os.popen(f'twine upload -u {username} -p {password} dist/*')
        return result.read()

    @staticmethod
    def upload_test(*args):
        if len(args) == 2: username, password = args
        else: return 'Error: please check the command.'
        Command.package()
        result = os.popen(f'twine upload -u {username} -p {password} --repository-url https://test.pypi.org/legacy/ dist/*')
        return result.read()

    @staticmethod
    def help(*args):
        return '''Command list:
        create_setup --- Create _setup.py file.
        upload <username> <password> --- Upload to https://upload.pypi.org/legacy.
        upload_test <username> <password> --- Upload to https://test.pypi.org/legacy.
        help --- Show command list.
        package --- Package project(create build, dist, *.egg-info file).
        remove_package --- Remove packaged file(remove build, dist, *.egg-info file).
        '''

    @staticmethod
    def package(*args):
        assert Path('setup.py').exists(), 'The setup.py not found.'
        if os.system('python setup.py sdist bdist_wheel') != 0:
            raise Exception('Error: please check the setup.py file')
        return 'Successful!'

    @staticmethod
    def remove_packaged(*args):
        for p in [Path('build'), Path('dist'), *Path.cwd().glob('*.egg-info')]:
            if p.exists(): shutil.rmtree(p)
        return 'Successful!'
