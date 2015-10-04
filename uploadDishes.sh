if [ $# -lt 1 ]
then
    echo 'Usage: dateFolder'
    exit
fi

export PATH=$PATH:~/bin/

staticDir=static/data/

today=`date +"%Y%m%d"`
mkdir -p $staticDir/$today/lunch9
mkdir -p $staticDir/$today/lunch22
mkdir -p $staticDir/$today/dinner9
mkdir -p $staticDir/$today/dinner22

imgDir = static/images/

python updateMenu.py 1
# find $imgDir -name '*.jpg' -cmin -30 -exec convert -auto-orient {} {} \;
numImg = `find $imgDir -name '*.jpg' -mmin -30 |wc -l`
find $imgDir -name '*.jpg' -mmin -30 -exec convert -resize 640x480 {} {} \;
find $imgDir -name '*.jpg' -mmin -30 -exec scp {} azureuser@gcsdJP:~/Rghoul/$imgDir \;
echo INFO: uploaded $numImg images

find $1 -name '.DS_Store' -exec rm {} \;
scp -r $1 azureuser@gcsdJP:~/Rghoul/$staticDir
