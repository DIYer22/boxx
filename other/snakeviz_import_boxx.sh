python -c "from cProfile import run; run('import boxx','/tmp/cProfile.result')"

snakeviz /tmp/cProfile.result
