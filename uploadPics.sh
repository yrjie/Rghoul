if [ $# -lt 1 ]
then
    echo 'Usage: dateFolder'
    exit
fi

scp -r $1 azureuser@gcsd:~/Rghoul/static/
curl http://rakuten-ghoul.xyz/update/
