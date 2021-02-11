# ex) bash bin/setup.sh --crate

proj_name=carm

OPT=`getopt -o cirsl -l create,reset,install,start,launch -- "$@"`
if [ $? != 0 ] ; then
    exit 1
fi
eval set -- "$OPT"

while true
do
    case $1 in
        -c | --create)
            # -create のときの処理
            mkdir -p checkpoints
            conda create -n $proj_name python==3.7
            echo "次のコマンドを実行してください：conda activate $proj_name"
            shift
            ;;
        -i | --install)
            # -install のときの処理
            pip install -r bin/requirements.txt
            python bin/get_secret_key.py
            shift
            ;;
        -r | --reset)
            # -reset のときの処理
            echo "現環境が$proj_nameでないことを確認し、$proj_nameである場合はconda deactivateを実行してください"
            conda remove -n $proj_name --all
            shift
            ;;
        -s | --start)
            # -start のときの処理
            source bin/init_db.sh
            python manage.py runserver
            shift
            ;;
        -l | --launch)
            # -launch のときの処理
            python manage.py runserver
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Internal error!" 1>&2
            exit 1
            ;;
    esac
done
