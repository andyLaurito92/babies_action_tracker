today=$(date +%F)
sqlite3 instance/baby_actions.db ".backup backups/baby_actions_$today.db.bak"
