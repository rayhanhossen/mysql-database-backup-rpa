import logging
import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(filename=f'./logs/app_{datetime.now().strftime("%d_%m_%Y")}.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# MySQL database credentials
mysql_host = os.environ.get("MYSQL_HOST")
mysql_port = os.environ.get("MYSQL_PORT")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
databases = os.environ.get("MYSQL_DATABASES")

# Backup directory (change this to the directory where you want to store backups)
backup_dir = os.environ.get("BACKUP_DIR")

# MysqlDump exe location
mysql_dump_loc = os.environ.get("MYSQL_DUMP_LOC")

# Get current datetime
now = datetime.now()

# Backup filename prefix
backup_filename_prefix = now.strftime('%Y-%m-%d_%I_%M_%p')

for database in databases.split(","):
    try:
        # Backup filename
        backup_filename = f"{database}_{backup_filename_prefix}.sql"

        # MySQL dump command
        dump_cmd = fr"{mysql_dump_loc} --host={mysql_host} --port={mysql_port} --user={mysql_user} --password={mysql_password} {database} > {os.path.join(backup_dir, backup_filename)}"

        # Execute MySQL dump command
        result = subprocess.run(dump_cmd, shell=True, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            print("error->", result.stderr)
            logging.error(result.stderr)
        else:
            print("output->", result.stdout)
            print(f"Backup of {database} saved to {backup_dir}")
            logging.info(msg=f"Backup of {database} saved to {backup_dir}")
    except Exception as e:
        print(e)
        logging.error(e)
