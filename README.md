<div align="center"><img src="https://github.com/shou5374/carm/blob/master/static/common/images/logo_mini.png" width="400"/></div>

# CARM : Car managemet system


# Environment
```sh
$ conda create -n py37-carm python==3.7  
$ conda activate py37-carm  
$ pip install -r requirements.txt  
```
※ 上記はローカル環境のみを想定. 場合によっては以下を実行する必要あり  
```sh
$ sudo apt-get install libgtk-3-dev  
```

※ SECRET_KEYは各自設定  

# Init Database

```sh
$ bash init_db.sh  
```
※ 必要に応じてスーパーユーザの設定を変更  

## License

MIT License (see `LICENSE` file).
