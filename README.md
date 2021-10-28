# 量子アニーラ実験検証

量子アニーリングについて理解を深めるための実験検証リポジトリ。
以下環境で動作を確認しています。

* ubuntu 20.04 LTS
* python == 3.9.4

D-Wave社のクラウドサービス [leap](https://cloud.dwavesys.com/leap/) のアカウントが必要です。
また、leapのAPIアクセストークンが必要で、以下の環境変数を定義しておいてください。

```bash
$ export DWAVE_API_TOKEN=********************
```

必要なパッケージは以下でインストールしてください。

```bash
$ pipenv install --dev
```

pythonの仮想環境に切り替えて、適当なプロジェクトに移動してください。

```bash
$ pipenv shell
(quantum-annealing-leap-playground) $ cd sudoku
```
