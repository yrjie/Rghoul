if [ $# -lt 1 ]
then
    echo 'Usage: auto script'
    exit 1
fi

infile=static/piclst/`date +'%Y%m%d'`.txt
imgDir=static/images/

python3 downloadPic.py $infile
find $imgDir -name '*.jpg' -mmin -5 -exec convert -resize 640x480 {} {} \;
find $imgDir -name '*.jpg' -mmin -5 -exec scp {} azureuser@gcsdJP:~/Rghoul/$imgDir \;
