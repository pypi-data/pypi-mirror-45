Disclaimer
==========

I'm tired of console measuring of memory usage
```bash
while true; do
ps -C <ProgramName> -o pid=,%mem=,vsz= >> /tmp/mem.log
gnuplot /tmp/show_mem.plt
sleep 1
done &
```

Description
===========

- Measuring and graphing memory usage of local processes
- Supported python versions are `3.5+`
- Python3.7 is a preferable interpreter

![alt text](https://raw.githubusercontent.com/parikls/mem_usage_ui/master/mem_usage_ui.png)


Installation
============

- run `pip3 install mem_usage_ui` or `pip install mem_usage_ui`

Usage
=====

- Run in shell: `mem_usage_ui`
- Default browser will be opened automatically
- Running on `http://localhost:8080`


Contributing
===========

Backend part
------------

- Install requirements: `pip install -r requirements.txt`
- Run app: `python -m mem_usage_ui --debug=True`

Frontend part
-------------

- Go to frontend directory: `cd frontend`
- Install dependencies: `npm install`
- Create (and watch) dev build - `npm run dev`

Pull request
------------

- Before pull request please create a production build `npm run prod`

