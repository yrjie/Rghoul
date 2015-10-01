if [ $# -lt 1 ]
then
    echo 'Usage: dateFolder'
    exit
fi

export PATH=$PATH:~/bin/
#convert -resize 450x600 static/data/20150903/lunch9/P1100508_1.JPG static/data/20150903/lunch9/P1100508_1.JPG
#find $1 -name '*.JPG' -exec convert -rotate 90 {} {} \;
find $1 -name '*.JPG' -cmin -90 -exec convert -auto-orient {} {} \;
find $1 -name '*.JPG' -cmin -90 -exec convert -resize 600x800 {} {} \;
find $1 -name '.DS_Store' -exec rm {} \;
scp -r $1 azureuser@gcsdJP:~/Rghoul/static/data/
#curl http://rakuten-ghoul.xyz/update/
curl http://gcsd-id-mars-japan.cloudapp.net/thisisupdate/

#rsync -av 1.jpg azureuser@gcsdJP:/home/azureuser/Rghoul/static/data/
#ln -fs ../images/BEEF.jpg 1.jpg
