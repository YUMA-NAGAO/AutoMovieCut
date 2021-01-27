# ・環境構築手順
## FFmpegの導入
使用したバージョン
4.3.1を使用しました。
バージョンの差異による環境構築失敗の防止のために、(GoogleDrive)[https://drive.google.com/file/d/1Qz5n41LnCyioVHJBpL-K2_zUVJx560Qy/view?usp=sharing]に今回使用したバージョンを誰でもアクセスできるようにします。

### Windowsの場合
[このサイト](https://rikoubou.hatenablog.com/entry/2019/11/07/144533)を参考にすると、導入が容易です。わからない場合は、「ffmpeg windows」などで調べてみてください。

1. ffmpeg-4.3.1-2021-01-01-full_build.7z」を解凍　※7zipで解凍してください
1. 解凍してできた「ffmpeg-4.3.1-2021-01-01-full_build」を「C:\Program Files」の中にコピー
1. システムの環境変数に「C:\Program Files\ffmpeg-4.3.1-2021-01-01-full_build\bin」を追加　※[環境変数の追加の仕方](https://www.atmarkit.co.jp/ait/articles/1805/11/news035.html)を参照
1. パソコンの再起動	
1. コマンドプロンプトを起動して「ffmpeg -version」を入力してバージョンが表示されれば成功
	
### Macの場合
1. Homebrewをインストール　※[ここ](https://codelab.website/mac-homebrew/)を参照
	
1. ターミナルに「brew install ffmpeg」
	


# 【動画の自動カット】

1. MovieCut内のinputフォルダに動画を入れる
2. funcフォルダのcut_movie.pyを実行
3. カットしたい音量の閾値を入力(デフォルトが-33dBでそのままエンターを押すとデフォルトで編集される)
4. outputフォルダに無音部分をカットした動画が保存

# 【動画の自動カットと合成】
1. MovieCut内のinputフォルダに動画を入れる
2. funcフォルダのcut_movie.pyを実行
3. カットしたい音量の閾値を入力(デフォルトが-33dBでそのままエンターを押すとデフォルトで編集される)

4. cutフォルダに無音部分をカットした動画が保存

5. mergedフォルダに動画をつなぎ合わせたものが生成

## 参考サイト
1. [Windows10にffmpegをインストールする](https://rikoubou.hatenablog.com/entry/2019/11/07/144533)
1. [環境変数の追加の仕方](https://www.atmarkit.co.jp/ait/articles/1805/11/news035.html)

1. [MacにHomebrewをインストールする](https://codelab.website/mac-homebrew/)