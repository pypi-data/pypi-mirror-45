from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'vkhealth',
  version = '0.3',
  description = 'Module that shows the health of VKontakte platform.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages = ['vkhealth'],
  author = 'Daniil Chizhevskij',
  author_email = 'daniilchizhevskij@gmail.com',
  url = 'https://github.com/DaniilChizhevskii/vkhealth',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
  ],
)