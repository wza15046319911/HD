import csv
import pymysql


with open("订单列表.csv", "r", encoding='utf-8-sig') as r:
    lines = r.readlines()
    header = lines[0].strip().split(",")
    header = [h.strip() for h in header if h]
    order_num = header[0] # int
    order_type = header[1] # text
    username, nickname, tutor = header[2], header[3], header[4] # text
    title, course_code, chapter = header[5], header[6], header[7] # text  # int  # text
    refund_chapter = header[8] # text
    major = header[9] # text
    faculty = header[10]  # text
    tax = header[11] # float
    original_price = header[12] # float
    currency = header[13]  # text
    paid_amount = header[14] # float
    payment_status = header[15]  # text
    payment_method = header[16]  # text
    client = header[17]  # text
    created_time = header[18]  # text
    # '订单编号', '订单类型', '用户名', '昵称', '主讲导师', '标题', '课程ID', '购买章节', '退款章节', '所属科目', '所属院校', '汇率', '课原价', '币种', '实际支付', '支付状态', '支付方式', '客户端', '创建时间'
    db = pymysql.connect("localhost","root","1995hujiajian","信息汇总")
    cursor = db.cursor()
    create_table_command = """CREATE TABLE 订单列表(
        {} BIGINT NOT NULL, 
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} INT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} FLOAT,
        {} FLOAT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} TEXT,
        {} TEXT)""".format(order_num, order_type, username, nickname, tutor, title, course_code, chapter, refund_chapter, major, faculty, tax, original_price, currency, paid_amount, payment_status, payment_method, client, created_time)
    cursor.execute(create_table_command)
    insert_header = "INSERT INTO 订单列表("
    for i in range(len(header)):
        insert_header += header[i]
        if i != len(header) - 1:
            insert_header += ","
    insert_header += ") VALUES ("
    for line in lines[1:]:
        new = ''
        line = line.strip().split(",")[:19]
        for j in range(len(line)):
            data = line[j]
            try:
                if j == 0 or j == 6:
                    if data == '':
                        data = 0
                    else:
                        data = int(data)
                elif j == 11 or j == 12 or j == 14:
                    if data == '':
                        data = 0
                    else:
                        data = float(data)
                if data == '':
                    data = "N/A"
            except Exception as e:
                print(" ".join(line))
            if not isinstance(data, str):
                new += str(data)
            else:
                new += "'{}'".format(data) 
            if j != len(line) - 1:
                new += ","
        new += ");\n"
        sql = insert_header + new
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(sql)
            db.rollback()
db.close()