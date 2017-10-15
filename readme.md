### Wikipedia page crawler in Python

#### crawler-gevent.py 

Web page crawler implemented using gevent and cooperative multithreading.

Sample runs:

```
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c1 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin                                      <<<
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 1, visited link limit: 100
python crawler-gevent.py -c1 -l100   18.84s user 0.56s system 50% cpu 38.199 total
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c2 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin                                      <<<
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 2, visited link limit: 100
python crawler-gevent.py -c2 -l100   19.92s user 0.54s system 65% cpu 31.111 total
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c3 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin                                      <<<
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 3, visited link limit: 100
python crawler-gevent.py -c3 -l100   15.34s user 0.44s system 69% cpu 22.797 total
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c4 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin                                      <<<
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 4, visited link limit: 100
python crawler-gevent.py -c4 -l100   18.63s user 0.47s system 76% cpu 24.846 total
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c5 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin                                      <<<
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 5, visited link limit: 100
python crawler-gevent.py -c5 -l100   17.70s user 0.46s system 78% cpu 23.221 total
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c10 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 10, visited link limit: 100
python crawler-gevent.py -c10 -l100   18.55s user 0.43s system 85% cpu 22.321 total
(crawler) ➜  python-crawler-example git:(master) ✗ time python crawler-gevent.py -c100 -l100 https://en.wikipedia.org/wiki/Alexander_Pushkin
start crawling from https://en.wikipedia.org/wiki/Alexander_Pushkin
concurrency level: 100, visited link limit: 100
python crawler-gevent.py -c100 -l100   43.14s user 1.05s system 93% cpu 47.103 total
```