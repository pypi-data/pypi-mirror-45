from distutils.core import setup

setup(
  name = 'twitce',         
  packages = ['twitce'],   
  version = '0.1',      
  license='MIT',        
  description = 'Gather userinformation from twitter',   
  author = 'Wouter Molhoek',                   
  author_email = 'woutermolhoek@hotmail.com',      
  url = 'https://github.com/WouterMolhoek/twitse',   
  download_url = 'https://github.com/WouterMolhoek/twitse/archive/0,1.tar.gz',   
  keywords = ['Twitter', 'Python', 'BeautifilSoup'],   
  install_requires=[            
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)