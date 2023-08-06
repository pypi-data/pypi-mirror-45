#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Radim Rehurek <radimrehurek@seznam.cz>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Run with:

sudo python ./setup.py install
"""

import os
import platform
import sys
import warnings
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

if sys.version_info[:2] < (2, 7) or (sys.version_info[:1] == 3 and sys.version_info[:2] < (3, 5)):
    raise Exception('This version of gensim needs Python 2.7, 3.5 or later.')

# the following code is adapted from tornado's setup.py:
# https://github.com/tornadoweb/tornado/blob/master/setup.py
# to support installing without the extension on platforms where
# no compiler is available.


class custom_build_ext(build_ext):
    """Allow C extension building to fail.

    The C extension speeds up word2vec and doc2vec training, but is not essential.
    """

    warning_message = """
********************************************************************
WARNING: %s could not
be compiled. No C extensions are essential for gensim to run,
although they do result in significant speed improvements for some modules.
%s

Here are some hints for popular operating systems:

If you are seeing this message on Linux you probably need to
install GCC and/or the Python development package for your
version of Python.

Debian and Ubuntu users should issue the following command:

    $ sudo apt-get install build-essential python-dev

RedHat, CentOS, and Fedora users should issue the following command:

    $ sudo yum install gcc python-devel

If you are seeing this message on OSX please read the documentation
here:

http://api.mongodb.org/python/current/installation.html#osx
********************************************************************
"""

    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(
                self.warning_message +
                "Extension modules" +
                "There was an issue with your platform configuration - see above.")

    def build_extension(self, ext):
        name = ext.name
        try:
            build_ext.build_extension(self, ext)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(
                self.warning_message +
                "The %s extension module" % (name,) +
                "The output above this warning shows how the compilation failed.")

    # the following is needed to be able to add numpy's include dirs... without
    # importing numpy directly in this script, before it's actually installed!
    # http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        # https://docs.python.org/2/library/__builtin__.html#module-__builtin__
        if isinstance(__builtins__, dict):
            __builtins__["__NUMPY_SETUP__"] = False
        else:
            __builtins__.__NUMPY_SETUP__ = False

        import numpy
        self.include_dirs.append(numpy.get_include())


model_dir = os.path.join(os.path.dirname(__file__), 'gensim', 'models')
gensim_dir = os.path.join(os.path.dirname(__file__), 'gensim')

cmdclass = {'build_ext': custom_build_ext}

WHEELHOUSE_UPLOADER_COMMANDS = {'fetch_artifacts', 'upload_all'}
if WHEELHOUSE_UPLOADER_COMMANDS.intersection(sys.argv):
    import wheelhouse_uploader.cmd
    cmdclass.update(vars(wheelhouse_uploader.cmd))


LONG_DESCRIPTION = u"""
==============================================
POSPair Word Embeddings
==============================================

Gensim is a Python library for *topic modelling*, *document indexing* and *similarity retrieval* with large corpora.
Target audience is the *natural language processing* (NLP) and *information retrieval* (IR) community.

POSPair Word Embedding is created by modifying Gensim library according to POSPair, generating more meaningful and efficient word embeddings.

"""

distributed_env = ['Pyro4 >= 4.27']

win_testenv = [
    'pytest',
    'pytest-rerunfailures',
    'mock',
    'cython',
    'pyemd',
    'testfixtures',
    'scikit-learn',
    'Morfessor==2.0.2a4',
]

linux_testenv = win_testenv[:]

if sys.version_info < (3, 7):
    linux_testenv.extend([
        'tensorflow <= 1.3.0',
        'keras >= 2.0.4, <= 2.1.4',
        'annoy',
    ])

ext_modules = [
    Extension('gensim.models.word2vec_inner',
        sources=['./gensim/models/word2vec_inner.c'],
        include_dirs=[model_dir]),
    Extension('gensim.models.doc2vec_inner',
        sources=['./gensim/models/doc2vec_inner.c'],
        include_dirs=[model_dir]),
    Extension('gensim.corpora._mmreader',
        sources=['./gensim/corpora/_mmreader.c']),
    Extension('gensim.models.fasttext_inner',
        sources=['./gensim/models/fasttext_inner.c'],
        include_dirs=[model_dir]),
    Extension('gensim.models._utils_any2vec',
        sources=['./gensim/models/_utils_any2vec.c'],
        include_dirs=[model_dir]),
    Extension('gensim._matutils',
        sources=['./gensim/_matutils.c']),
]

if not (os.name == 'nt' and sys.version_info[0] < 3):
    extra_args = []
    system = platform.system()

    if system == 'Linux':
        extra_args.append('-std=c++11')
    elif system == 'Darwin':
        extra_args.extend(['-stdlib=libc++', '-std=c++11'])

    ext_modules.append(
        Extension('gensim.models.word2vec_corpusfile',
                  sources=['./gensim/models/word2vec_corpusfile.cpp'],
                  language='c++',
                  extra_compile_args=extra_args,
                  extra_link_args=extra_args)
    )

    ext_modules.append(
        Extension('gensim.models.fasttext_corpusfile',
                  sources=['./gensim/models/fasttext_corpusfile.cpp'],
                  language='c++',
                  extra_compile_args=extra_args,
                  extra_link_args=extra_args)
    )

    ext_modules.append(
        Extension('gensim.models.doc2vec_corpusfile',
                  sources=['./gensim/models/doc2vec_corpusfile.cpp'],
                  language='c++',
                  extra_compile_args=extra_args,
                  extra_link_args=extra_args)
    )

setup(
    name='POSPairWordEmbeddings',
    version='0.0.4',
    description='POSPair Word Embeddings- Python framework for fast Vector Space Modelling',
    long_description=LONG_DESCRIPTION,

    ext_modules=ext_modules,
    cmdclass=cmdclass,
    packages=find_packages(),

    author=u'Jim Macwan',
    author_email='jimmacwan94@gmail.com',

    url='https://github.com/jmacwan/POSPair',
    download_url='https://github.com/jmacwan/POSPair',
    
    license='LGPLv2.1',

    keywords='Singular Value Decomposition, SVD, Latent Semantic Indexing, '
        'LSA, LSI, Latent Dirichlet Allocation, LDA, '
        'Hierarchical Dirichlet Process, HDP, Random Projections, '
        'TFIDF, word2vec',

    platforms='any',

    zip_safe=False,

    classifiers=[  # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],

    test_suite="gensim.test",
    setup_requires=[
        'numpy >= 1.11.3'
    ],
    install_requires=[
        'numpy >= 1.11.3',
        'scipy >= 0.18.1',
        'six >= 1.5.0',
        'smart_open >= 1.2.1',
    ],
    tests_require=linux_testenv,
    extras_require={
        'distributed': distributed_env,
        'test-win': win_testenv,
        'test': linux_testenv,
        'docs': linux_testenv + distributed_env + ['sphinx', 'sphinxcontrib-napoleon', 'plotly', 'pattern <= 2.6', 'sphinxcontrib.programoutput'],
    },

    include_package_data=True,
)
