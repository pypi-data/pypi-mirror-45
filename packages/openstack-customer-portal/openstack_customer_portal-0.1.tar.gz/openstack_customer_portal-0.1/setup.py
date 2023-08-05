from distutils.core import setup
setup(
  name = 'openstack_customer_portal',         # How you named your package folder (MyLib)
  packages = ['openstack_customer_portal'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'openstack portal for customer, focus on monitoring',   # Give a short description about your library
  author = 'hoa ngo',                   # Type in your name
  author_email = 'ngohoa211@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ngohoa211/openstack_customer_portal',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ngohoa211/openstack_customer_portal/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['MONITOR', 'OPENSTACK', 'PORTAL'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
)