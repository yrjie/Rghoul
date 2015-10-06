if [ $# -lt 1 ]
then
    echo 'Usage: infile'
    exit 1
fi

imgDir=static/images/

python3 downloadPic.py $1
find $imgDir -name '*.jpg' -mmin -5 -exec convert -resize 640x480 {} {} \;
find $imgDir -name '*.jpg' -mmin -5 -exec scp {} azureuser@gcsdJP:~/Rghoul/$imgDir \;
