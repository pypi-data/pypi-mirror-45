from setuptools import setup, find_packages

def readme():
	with open('README.md') as f:
		README = f.read()
	return README

setup(name='msg91-sms',
      version='1.0.1',
      # packages=find_packages(),
      description="A simple and easy to use Python package to send SMS using MSG91 SMS API.",
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://www.codespeedy.com/',
      author='CodeSpeedy Technology Pvt. Ltd.',
      license='MIT',
      keywords='msg91-sms msg91 sms',
      packages=["msg91_sms"],
      python_requires='>=3.4',
      install_requires=['requests','json'],  # Optional

       # project_urls={  # Optional
       #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
       #     'Funding': 'https://donate.pypi.org',
       #     'Say Thanks!': 'http://saythanks.io/to/example',
       #     'Source': 'https://github.com/pypa/sampleproject/',
       # },

      )