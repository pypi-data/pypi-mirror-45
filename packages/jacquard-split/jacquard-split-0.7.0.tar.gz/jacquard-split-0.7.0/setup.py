from setuptools import setup, find_packages

import os
import sys

# This monstrous hack is to support /etc generation for the Debian package
# with fpm.
if sys.argv[1] == 'install' and os.environ.get('JACQUARD_DEBIAN_HACK'):
    def debian_etc_hack(root):
        import pathlib
        root_path = pathlib.Path(root)
        config_dir = root_path / 'etc' / 'jacquard'

        try:
            config_dir.mkdir(parents=True)
        except FileExistsError:
            pass
        try:
            (config_dir / 'plugins').mkdir()
        except FileExistsError:
            pass

        with (config_dir / 'config.cfg').open('wb') as f_out:
            with open('debian.cfg', 'rb') as f_in:
                config_file = f_in.read()
                f_out.write(config_file)

        try:
            (root_path / 'var' / 'jacquard').mkdir(parents=True)
        except FileExistsError:
            pass

    debian_etc_hack(sys.argv[3])
    del debian_etc_hack


with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='jacquard-split',
    version='0.7.0',
    url='https://github.com/prophile/jacquard',
    description="Split testing server",
    long_description=long_description,

    author="Alistair Lynn",
    author_email="alistair@alynn.co.uk",

    keywords = (
        'ab-testing',
        'e-commerce',
        'experiments',
        'jacquard',
        'metrics',
        'redis',
        'science',
        'split-testing',
        'testing',
        'zucchini',
    ),
    license='MIT',

    zip_safe=False,

    packages=find_packages(),

    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business',
    ),

    install_requires=(
        'redis',
        'werkzeug',
        'python-dateutil',
        'pyyaml',
        'sqlalchemy',
    ),

    setup_requires=(
        'pytest-runner',
    ),

    tests_require=(
        'pytest',
        'redis==2.10.6',
        'fakeredis==0.16.0',
        'hypothesis<4',
    ),

    entry_points={
        'console_scripts': (
            'jacquard = jacquard.cli:main',
        ),
        'jacquard.storage_engines': (
            'dummy = jacquard.storage.dummy:DummyStore',
            'redis = jacquard.storage.redis:RedisStore',
            'redis-cloned = jacquard.storage.cloned_redis:ClonedRedisStore',
            'file = jacquard.storage.file:FileStore',
        ),
        'jacquard.commands': (
            'storage-dump = jacquard.storage.commands:StorageDump',
            'storage-flush = jacquard.storage.commands:StorageFlush',
            'storage-import = jacquard.storage.commands:StorageImport',
            'storage-export = jacquard.storage.commands:StorageExport',
            'set-default = jacquard.users.commands:SetDefault',
            'override = jacquard.users.commands:Override',
            'clear-overrides = jacquard.users.commands:OverrideClear',
            'runserver = jacquard.service.commands:RunServer',
            'launch = jacquard.experiments.commands:Launch',
            'conclude = jacquard.experiments.commands:Conclude',
            'load-experiment = jacquard.experiments.commands:Load',
            'rollout = jacquard.buckets.commands:Rollout',
            'settings-under-experiment = jacquard.experiments.commands:SettingsUnderActiveExperiments',
            'bugpoint = jacquard.commands_dev:Bugpoint',
        ),
        'jacquard.commands.list': (
            'experiments = jacquard.experiments.commands:ListExperiments',
        ),
        'jacquard.commands.show': (
            'user = jacquard.users.commands:Show',
            'defaults = jacquard.users.commands:Show',
            'directory-entry = jacquard.directory.commands:ShowDirectoryEntry',
            'experiment = jacquard.experiments.commands:Show',
        ),
        'jacquard.directory_engines': (
            'dummy = jacquard.directory.dummy:DummyDirectory',
            'django = jacquard.directory.django:DjangoDirectory',
            'union = jacquard.directory.union:UnionDirectory',
        ),
        'jacquard.http_endpoints': (
            'root = jacquard.service.endpoints:Root',
            'user = jacquard.service.endpoints:User',
            'experiments-overview = jacquard.service.endpoints:ExperimentsOverview',
            'experiment = jacquard.service.endpoints:ExperimentDetail',
            'experiment-partition = jacquard.service.endpoints:ExperimentPartition',
            'defaults = jacquard.service.endpoints:Defaults',
        ),
    },
)
