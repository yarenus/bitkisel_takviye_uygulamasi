from app import db, Supplement
from app import app

with app.app_context():
    # Veritabanını sıfırlamak istiyorsan önce:
    db.drop_all()
    db.create_all()

    # Örnek takviye verileri
    takviye1 = Supplement(
        name="Omega-3",
        purpose="Kalp sağlığını destekler",
        side_effects="Kan sulandırıcı etki yapabilir",
        interaction_warning="Kan sulandırıcı ilaçlarla etkileşime girebilir"
    )

    takviye2 = Supplement(
        name="Melatonin",
        purpose="Uyku düzenini destekler",
        side_effects="Sabah sersemliği yapabilir",
        interaction_warning="Uyku ilaçlarıyla birlikte kullanılması önerilmez"
    )

    takviye3 = Supplement(
        name="Zencefil",
        purpose="Bağışıklığı güçlendirir",
        side_effects="Mide rahatsızlığı yapabilir",
        interaction_warning="Kan basıncı ilaçları ile etkileşime girebilir"
    )

    # Verileri ekleyip kaydet
    db.session.add_all([takviye1, takviye2, takviye3])
    db.session.commit()

    print("Veriler başarıyla eklendi.")
