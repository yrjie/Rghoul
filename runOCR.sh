if [ $# -lt 1 ]
then
    echo 'Usage: auto script'
    exit 1
fi

find static/data/ -name "P*.JPG" |xargs -n1 sh -c 'file=`basename $0`; tesseract $0 ~/test/name/${file%.*}'
