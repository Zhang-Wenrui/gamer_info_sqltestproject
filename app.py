from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# 设置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'players.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 玩家模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    game_id = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Player {self.username}>'

# 创建数据库表
with app.app_context():
    db.create_all()

# 路由：首页
@app.route('/')
def index():
    players = Player.query.all()
    return render_template('index.html', players=players)

# 路由：添加玩家
@app.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        username = request.form['username']
        game_id = request.form['game_id']
        level = request.form['level']
        score = request.form['score']
        
        # 检查用户名是否已存在
        existing_player = Player.query.filter_by(username=username).first()
        if existing_player:
            flash('用户名已存在，请使用其他用户名')
            return redirect(url_for('add_player'))
        
        # 创建新玩家
        new_player = Player(username=username, game_id=game_id, 
                            level=int(level), score=int(score))
        db.session.add(new_player)
        db.session.commit()
        
        flash('玩家添加成功！')
        return redirect(url_for('index'))
    
    return render_template('add_player.html')

# 路由：编辑玩家
@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)
    
    if request.method == 'POST':
        player.username = request.form['username']
        player.game_id = request.form['game_id']
        player.level = int(request.form['level'])
        player.score = int(request.form['score'])
        
        db.session.commit()
        flash('玩家信息已更新！')
        return redirect(url_for('index'))
    
    return render_template('edit_player.html', player=player)

# 路由：删除玩家
@app.route('/delete/<int:player_id>')
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    
    flash('玩家已删除！')
    return redirect(url_for('index'))

# 新添加：管理员API路由
@app.route('/admin')
def admin():
    return render_template('admin.html')

# 新添加：API获取所有玩家数据
@app.route('/api/players')
def get_players():
    players = Player.query.all()
    player_list = []
    for player in players:
        player_list.append({
            'id': player.id,
            'username': player.username,
            'game_id': player.game_id,
            'level': player.level,
            'score': player.score
        })
    return jsonify(player_list)

# 运行应用
if __name__ == '__main__':
    app.run(debug=True) 