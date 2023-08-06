from setuptools import setup, Extension, find_packages

module = Extension('x11_client',
                   define_macros=[('MAJOR_VERSION', '1'),
                                  ('MINOR_VERSION', '4')],
                   include_dirs=['/usr/include', 'ext'],
                   libraries=['X11', 'Xtst'],
                   library_dirs=['/usr/lib'],
                   headers=['ext/x11_client.h'],
                   sources=['ext/x11_client.c'])

setup(name='X11Client',
      version='1.4',
      description='X11 client',
      author='Diego Rubin',
      author_email='rubin.diego@gmail.com',
      url='http://github.com/diegorubin/X11Client',
      packages=find_packages(),
      long_description='''
       X11 Client
''',
      ext_modules=[module])
