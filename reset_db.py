# reset_db.py

from app import app, db

# Uygulama bağlamını aç
with app.app_context():
    # Mevcut tabloları sil
    db.drop_all()
    # Yeni tabloları oluştur
    db.create_all()
    print("Veritabanı sıfırlandı ve yeniden oluşturuldu.")

