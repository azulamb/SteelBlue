# SteelBlue

SteelBlueはシンプルはWebファイラーです。
以下のような機能を持たせることを目標としています。

* ドラッグ&ドロップによる簡易アップロード。
* 簡易ビューワーによる主要なファイルの表示。
* シンプルで軽量なファイラー。

今現在最低限のアップロード機能とファイル閲覧などが可能です。

## 設置

以下のファイルに実行権限を与えてください。

* index.cgi
* downloader.cgi
* uploader.cgi

また以下のファイルもセットでアップロードしてください。

* FileViewer.pm
* setting.pl
* style.css
* upload.js

設定については基本的にsetting.plを編集してください。

## 備考

JavaScriptはTypeScriptを使って書き直しました。
また、諸事情により XMLHttpRequest.prototype.sendAsBinary の定義部分でエラーが発生していますが、一応生成できているので良しとします。何とかしたいです。

