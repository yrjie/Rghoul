if [ $# -lt 1 ]
then
    echo 'Usage: rootDateFolder'
    exit
fi

mkdir -p $1/lunch9
mkdir -p $1/lunch22
mkdir -p $1/dinner9
mkdir -p $1/dinner22
