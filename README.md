[![CC BY NC ND 2.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

This work is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Generic License][cc-by-nc-nd].

[![CC BY NC ND 2.0][cc-by-nc-nd-image]][cc-by-nc-nd]

[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/2.0/
[cc-by-nc-nd-image]: https://i.creativecommons.org/l/by-nc-nd/2.0/88x31.png
[cc-by-nc-nd-shield]: https://i.creativecommons.org/l/by-nc-nd/2.0/80x15.png


Make sure you have Python 3.8.
To try it for now clone and then do:
```
git clone https://github.com/brleinad/decret-o-matic.git
cd decret-o-matic
python3 -m venv venv
. ./venv/bin/activate 
#C:\> <venv>\Scripts\activate.bat on Windows
pip install -r requirements.txt
python decreto-o-manic.py
```

To generate the executable file first install pyinstaller:
```
pip install pysintaller
```
Then run pyinstaller using the .spec file.
```
pyinstaller --clean decret-o-matic.spec
```
and this will create the executable under dist/.
