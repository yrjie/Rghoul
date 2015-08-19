# if [ $# -lt 1 ]
# then
# 	echo 'Usage: Auto script'
# 	exit
# fi

git archive master | tar -x -C /Users/ruijie.yang/Applications/apache-tomcat-7.0.63/webapps/ghoul/
