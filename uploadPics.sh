if [ $# -lt 1 ]
then
    echo 'Usage: dateFolder'
    exit
fi

find . -name '.DS_Store' -exec rm {} \;
scp -r $1 azureuser@gcsd:~/Rghoul/static/
curl http://rakuten-ghoul.xyz/update/
