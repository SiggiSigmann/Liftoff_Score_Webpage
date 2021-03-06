#!/bin/bash
path_to_backup="/home/ubuntu/backup_Liftoff"

#create backup
docker exec server_db_1 mysqldump -u root --password="1234567" LIFTOFF_DATA > "${path_to_backup}/backup_$(date +"%Y_%m_%d_%I_%M_%p").sql"

#delete older file
find $path_to_backup -name "backup*.sql" -type f -mtime +20 -delete
find $path_to_backup -name "output*.txt" -type f -mtime +20 -delete

#load backupscript
#cat backup_date.sql | docker exec -i server_db_1 mysql -u root --password=1234567 LIFTOFF_DATA
