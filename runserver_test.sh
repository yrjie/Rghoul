alias python=/usr/local/bin/python2.7
#export PYTHONPATH=$PYTHON:/usr/lib/python2.7/site-packages/
logF=log/`date +"%Y%m%d"`.log
python manage.py runserver --insecure 100.72.102.16:80 >>$logF 2>&1
