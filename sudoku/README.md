# sudoku 

数独を量子アニーリングで解いてみる。

## 実行方法

```bash
(quantum-annealing-leap-playground) $ python main.py --help
Usage: main.py [OPTIONS]

Options:
  --filename TEXT                 [default: problem.txt]
  --solver-name TEXT              [default: qpu]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

* `--filename` : 数独の問題が記述されているテキストファイルを指定します
* `--solver-name` : 使用するソルバーを指定します（`qpu | tabu | sa | kerberos` が指定可能）

## 実行例

```bash
(quantum-annealing-leap-playground) $ python main.py \
  --filename ./problems/4x4/problem-00.txt \
  --solver-name qpu
3 1 4 2
2 4 1 3
1 3 2 4
4 2 3 1
bqm energy:  0.0
The solution is correct
```
