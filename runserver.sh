#alias python=/usr/local/bin/python2.7
#export PYTHONPATH=$PYTHON:/usr/lib/python2.7/site-packages/
logF=log/`date +"%Y%m%d"`.log
#python manage.py runserver --insecure 100.74.102.130:80 >>$logF 2>&1
if [[ -z $VCAP_APP_PORT ]]  # is empty
then
    VCAP_APP_PORT=5000
fi
echo 'running at ' 0.0.0.0:$VCAP_APP_PORT
python manage.py runserver --insecure 0.0.0.0:$VCAP_APP_PORT >>$logF 2>&1
