from setuptools import setup
setup(name='rtsp_curl',
      version='0.2',
      description='What the module does',
      url='https://github.com/madyel/rtsp_curl',
      author='MaDyEl',
      author_email='madyel@countermail.com',
      license='MIT',
      packages=['madyel'],
      install_requires=['scanf>=1.5.2',
                        'pycurl==7.43.0.2'])