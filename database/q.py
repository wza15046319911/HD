import pymysql

db = pymysql.connect("localhost","root","1995hujiajian","信息汇总")
cursor = db.cursor()
with open("HDP/公开课列表.csv", "r", encoding="utf-8-sig") as r:
    lines = r.readlines()
    header = lines[0].strip().split(",")
    print(header)
    insert_header = "INSERT INTO 公开课列表("
    for i in range(len(header)):
        insert_header += header[i]
        if i != len(header) - 1:
            insert_header += ","
    insert_header += ") VALUES ("
    for line in lines[-26:]:
        line = line.strip().split(",")
        new = ''
        for i in range(len(line)):
            data = line[i]

            if i == 0:
                data = int(data)
            if i == 9:
                if data:
                    data = int(data)
                else:
                    data = 0
            if i == 11:
                if data:
                    data = float(data)
                else:
                    data = "NULL"
            if data == '':
                data = "NULL"
            if not isinstance(data, str):
                new += str(data)
            else:
                new += "'{}'".format(data) 
            if i != len(line) - 1:
                new += ","
        new += ");\n"
        sql = insert_header + new
        # print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            # print(sql)
            print(str(e))
            # db.rollback()
db.close()