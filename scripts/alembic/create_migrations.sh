read -p "Enter name of migration: " message
docker exec tg_bot alembic revision --autogenerate -m "$message"
sudo chmod +777 /infrastructure/migrations/versions/*

# sudo sh scripts/alembic/create_migrations.sh