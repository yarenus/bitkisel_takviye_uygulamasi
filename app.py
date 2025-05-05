from flask import Flask , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template

import os



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'db.sqlite3')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Supplement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(200))
    side_effects = db.Column(db.String(200))
    interaction_warning = db.Column(db.String(200))

    def __repr__(self):
        return f'<Supplement {self.name}>'
    
@app.route('/add', methods=['GET', 'POST'])
def add_supplement():
    if request.method == 'POST':
        new = Supplement(
            name=request.form['name'],
            purpose=request.form.get('purpose'),
            side_effects=request.form.get('side_effects'),
            interaction_warning=request.form.get('interaction_warning')
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('list_supplements'))

    # GET isteğinde basit HTML formunu döner
    return '''
    <h1>Takviye Ekle</h1>
    <form method="POST">
      <label>Adı: <input type="text" name="name" required></label><br>
      <label>Kullanım Amacı: <input type="text" name="purpose"></label><br>
      <label>Yan Etkiler: <input type="text" name="side_effects"></label><br>
      <label>Etkileşim Uyarısı: <input type="text" name="interaction_warning"></label><br>
      <button type="submit">Kaydet</button>
    </form>
    <p><a href="{{ url_for('list_supplements') }}">Tümünü Gör</a></p>
    '''

@app.route('/supplements')
def list_supplements():
    supplements = Supplement.query.all()
    html = '<h1>Takviyeler</h1>'
    html += '<p><a href="' + url_for('add_supplement') + '">Yeni Ekle</a></p>'
    for s in supplements:
        html += f'''
        <div style="margin-bottom:20px;">
          <h2>{s.name}</h2>
          <ul>
            <li><strong>Amacı:</strong> {s.purpose or '-'}</li>
            <li><strong>Yan Etkiler:</strong> {s.side_effects or '-'}</li>
            <li><strong>Etkileşim Uyarısı:</strong> {s.interaction_warning or '-'}</li>
          </ul>
        </div>
        <hr>'''
    return html

@app.route('/supplements')
def get_supplements():
    supplements = Supplement.query.all()
    data = [
        {
            'id': s.id,
            'name': s.name,
            'purpose': s.purpose,
            'side_effects': s.side_effects,
            'interaction_warning': s.interaction_warning
        }
        for s in supplements
    ]
    return jsonify(data)


@app.route('/')
def home():
    return "Bitkisel Takviye Uygulamasına Hoş Geldiniz!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

