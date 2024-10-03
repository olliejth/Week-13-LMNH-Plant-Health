source .env
sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -i ../short_term/schema.sql
sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -i seed_fake_data.sql
