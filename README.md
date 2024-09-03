# piwigo-exporter

Want to leave piwigo? Here is  tool to export all your albums in structured directories in your file system.

## Install
> python3 -m venv .

> source bin/activate

> pip install -r requirement.txt


## launch the export

>python src/main.py --dbuser <DB_USER> --dbpassword <DB_PASSWORD> --dbhost <DB_HOSTNAME> --dbname <DB_NAME> --src_path <SRC_PATH>

`SRC_PATH` is the directory containing upload, local, galeries. In common install, it is `/var/www` 

Directories will be created in ./data/