import sqlite3

def view_players():
    # 连接到数据库
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    
    # 执行查询 - 注意表名改为 Player (首字母大写)
    cursor.execute("SELECT * FROM Player")
    players = cursor.fetchall()
    
    # 显示列名
    columns = [description[0] for description in cursor.description]
    print('-' * 80)
    print(f"{columns[0]:<5} {columns[1]:<15} {columns[2]:<15} {columns[3]:<10} {columns[4]:<10}")
    print('-' * 80)
    
    # 显示每个玩家的信息
    for player in players:
        print(f"{player[0]:<5} {player[1]:<15} {player[2]:<15} {player[3]:<10} {player[4]:<10}")
    
    # 关闭连接
    conn.close()

if __name__ == "__main__":
    view_players() 