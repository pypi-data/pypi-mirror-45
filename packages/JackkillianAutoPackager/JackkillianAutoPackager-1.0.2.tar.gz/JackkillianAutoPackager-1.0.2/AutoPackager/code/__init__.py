name='JackkillianAutoPackager'
version='1.0.2'
quick_docs = """
JackkillianAutoPackager
=======================
Pip: pip install JackkillianAutoPackager
GitHub: https://github.com/Jackkillian/Jackkillian-Auto-Packager/
Wiki: https://github.com/Jackkillian/Jackkillian-Auto-Packager/wiki/
Bugs/Issues: https://github.com/Jackkillian/Jackkillian-Auto-Packager/issues
Author: Jackkillian
Version: 1.0.2
License: MIT
Ratings: 5/5 ("Offically" rated by 1 person)
"""
import JackkillianAutoPackager
print('Welcome to JackkillianAutoPackager. To run, do:')
print('\timport JackkillianAutoPackager as Packager')
print('\tPackager.main()')
print('Quick docs:')
print(quick_docs)
run = input('Would you like to run? (y/n): ')
if run.lower() == 'y':
    JackkillianAutoPackager.main()
else:
    print('OK')
