algo=(`cat random_migrations.txt | cut -d " " -f 1 | sort -u`)
threshold=(`cat random_migrations.txt | cut -d " " -f 14 | sort -u`)
migrations=(`wc -l random_migrations.txt | cut -d " " -f 1 | sort -u`)
time=(`cat random_migrations.txt | cut -d " " -f 19 | sort -u`)

echo $algo $threshold $migrations $time >> runtime_data.txt

algo=(`cat bestfit_migrations.txt | cut -d " " -f 1 | sort -u`)
threshold=(`cat bestfit_migrations.txt | cut -d " " -f 14 | sort -u`)
migrations=(`wc -l bestfit_migrations.txt | cut -d " " -f 1 | sort -u`)
time=(`cat bestfit_migrations.txt | cut -d " " -f 19 | sort -u`)

echo $algo $threshold $migrations $time >> runtime_data.txt