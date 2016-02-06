# Instructions

Environment Setup
-----------------

0. Install git [Learning git by doing](https://try.github.io/levels/1/challenges/1)
1. Install Python 2.7
2. Install pip  '''bash $sudo easy_install pip '''
3. Install [virtualenv](https://virtualenv.readthedocs.org/en/latest/#) '''bash $sudo pip install virtualenv'''


Project Setup
-------------

1. Create a virtualenv for the project 
```bash
cd myenvironments
virtualenv myvirtualenv
```

2. Git clone the project in a folder you would like 
```bash
cd myprojects
git clone myproject
```

3. Work in your virtual environment 
```bash
cd myproject
source /path/to/myvirtualenv/bin/activate
# now you are in your virtualenv
# and can install dependencies
pip install -r requirements.txt
```
