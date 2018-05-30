from flask import Flask, g
import pymysql
import pymysql.cursors
import json
app = Flask(__name__)

FLOW_LIMIT = 4000


@app.before_request
def before_request():
    """处理请求生命周期内的数据库加载
    """
    g.db = pymysql.connect(
        '127.0.0.1', 'root', 'p5243992', 'flow_db',
        charset='utf8', cursorclass=pymysql.cursors.DictCursor)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def get_latest_time():
    """获取最近的时间
    """
    with g.db.cursor() as cur:
        # 查询所有数据
        sql = 'SELECT MAX(last_updated) latest FROM flow_table'
        cur.execute(sql)
        return cur.fetchone()


def get_all_discrete_list_builder(keyword):
    """获取所有的协议
    Returns:
    """

    with g.db.cursor() as cur:
        # 查询所有数据
        sql = 'SELECT %s FROM (SELECT * FROM flow_table ORDER BY last_updated DESC LIMIT 300) as tmp  ORDER BY last_updated ASC' % (
            keyword)
        cur.execute(sql)
        return list(set([item[keyword] for item in cur.fetchall()]))


@app.route('/dist/<key>')
def dist(key):
    with g.db.cursor() as cur:
        sql = "SELECT %s _k,sum(packetcount) _v FROM flow_table GROUP BY %s" % (
            key, key)
        cur.execute(sql)
        data = cur.fetchall()
        data = [{'_k': item['_k'], '_v':float(item['_v'])}
                for item in data]
        return json.dumps(data)


@app.route('/series/<category>/<value>')
def get_series(category, value):
    """获取分类分布信息
    Returns:
        [type] -- [description]
    """

    with g.db.cursor() as cur:
        sql = "SELECT * FROM flow_table WHERE %s LIKE '%s' ORDER BY last_updated ASC" % (
            category, value)
        cur.execute(sql)
        return json.dumps(cur.fetchall())


@app.route('/flowdata')
def get_flow_data():
    """获取流量信息

    Returns:
        [type] -- [description]
    """

    with g.db.cursor() as cur:
        # 查询所有数据 注意 限制300条
        sql = 'SELECT * FROM flow_table ORDER BY last_updated DESC LIMIT 300'
        cur.execute(sql)
        flow_data = cur.fetchall()
        return json.dumps(
            {
                'packets': flow_data,
                'filters': {
                    'protocols': get_all_discrete_list_builder(keyword='protocol'),
                    'src_ips': get_all_discrete_list_builder(keyword='src_ip'),
                    'dst_ips': get_all_discrete_list_builder(keyword='dst_ip'),
                    'src_ports': get_all_discrete_list_builder(keyword='src_port'),
                    'dst_ports': get_all_discrete_list_builder(keyword='dst_port'),
                },
                'protocols': get_all_discrete_list_builder('protocol'),
                'latest': get_latest_time()
            }
        )


@app.route('/new/<last_time>')
def get_new_flow(last_time):
    """查询最新的实时数据
    """

    with g.db.cursor() as cur:
        print(last_time)
        sql = "SELECT * FROM flow_table WHERE last_updated>%s ORDER BY last_updated ASC" % last_time
        print(sql)
        cur.execute(sql)
        flow_data = cur.fetchall()
        return json.dumps({
            'new_flow': flow_data,
            'latest': get_latest_time(),
            'protocols': get_all_discrete_list_builder('protocol'),
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
