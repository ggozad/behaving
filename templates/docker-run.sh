cd behaving
./bin/supervisord
xvfb-run -a --server-args="-screen 0 2048x1024x16" ./bin/behave $1