<div align="center"><img src="https://github.com/shou5374/carm/blob/master/static/common/images/logo_mini.png" width="400"/></div>

# CARM : Car managemet system
下記のリンクからサイトにアクセス可能です  
https://carm.jp

# Maintenance
* 20-11-20 EC2上でのみ日報の文字化け

# Environment
* Ubuntu 18.04 LTS (それ以外はrequirements.txtに記載)  

```sh
$ bash bin/setup.sh --create
$ bash bin/setup.sh --install
$ bash bin/setup.sh --start
```
※ 上記はローカル環境のみを想定. 場合によっては以下を実行する必要あり 
```sh
$ sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info 
```

※ SECRET_KEYは各自設定  

# Initialize Database

```sh
$ bash bin/setup.sh --start
```
※ 必要に応じてスーパーユーザの設定を変更 

# Other
* carm.jpの各種設定はデフォルトのものと異なります. そのため試用で管理画面に移ることはできません.  
* グループを作成すると自動的に作成者がグループリーダーになります.  リーダーはメンバー管理や車両追加などの権限が与えられます.
* グループ内で車両管理が可能です. 初期ユーザは共有グループ「Independent」に所属することになります.

## How to use
* Sign upからアカウントを新規作成 (もしくは"admin@example.com", "pass"でアクセス)
* トップページ
  * 使用期間による絞り込み：対象車両を使用したい期間を指定することで、その期間内で予約の入っていない車両のみ表示される    
  * 車種による絞り込み：車両追加時に設定できる車種での絞り込みが可能. ハートマーク（保存）からお気に入り登録ができ、それによる絞り込みも可能.  
  * 予約ボタンから対象車両の予約ページへ遷移します.
* ヘッダ右上のアカウントボタン  
  * クリックすることで各機能へのリンク一覧が表示されます. ユーザの権限に応じて表示される内容が異なります.  
* Group作成  
  * グループの作成が可能. 作成後自動的にリーダになります.  
* Group管理・検索  
  * 作成済みグループを青枠内で検索可能です. 検索ヒットした場合、該当グループに対して参加申請も可能です.  
  * オレンジ枠は所属グループ一覧です. 所属グループが複数の場合、どのグループをアクティブ化するかを選択できます. グループリーダはメンバー管理画面への遷移が可能です. 
  * メンバー管理画面では他ユーザからのグループ参加申請一覧、及び参加済みメンバーを表示可能です. どちらも削除することが可能です.
* Book
  * 自分の予約した車両情報一覧が表示されます. 運転日報を作成するための各情報を入力できます. 
  * 日報ボタンをクリックすることで登録された情報をもとに運転日報が生成されます. 実行するサーバ環境によってはWeasyPrintが正しく動作しないかもしれません.
* Car管理
  * グループリーダのみヘッダ右上のアカウント情報に表示されます. 車両の追加が可能です.
  * 写真サイズはあまり大きめのものは好ましくないため、上限サイズは低いままにしてあります. エラー画面になるようであれば、画像サイズを小さくして再度試してください.  


## License

MIT License (see `LICENSE` file).
