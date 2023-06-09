from flask import Flask, render_template, request, redirect
import pymysql

# 连接数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='iot23',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor # 返回结果为字典类型
)

# 创建Flask应用
app = Flask(__name__)

# 员工列表页面
@app.route('/')
def employee_list():
    try:
        with connection.cursor() as cursor:
            # SQL查询语句
            sql = "SELECT * FROM employees"
            # 执行查询语句
            cursor.execute(sql)
            # 获取所有员工信息
            employees = cursor.fetchall()
        # 渲染指定模板并传入数据
        return render_template('list_employee.html', employees=employees)
    except:
        # 出现异常时回滚并且关闭数据库连接
        connection.rollback()
        connection.close()
        return "Something went wrong while displaying employee list."

# 增加员工页面
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    # 提交表单时
    if request.method == 'POST':
        try:
            # 获取表单提交的数据
            name = request.form['name']
            email = request.form['email']
            address = request.form['address']
            with connection.cursor() as cursor:
                # SQL插入语句
                sql = "INSERT INTO employees (name, email, address) VALUES (%s, %s, %s)"
                # 执行插入语句
                cursor.execute(sql, (name, email, address))
            # 提交到数据库执行
            connection.commit()
            # 重定向到员工列表页面
            return redirect('/', code=302)
        except:
            # 出现异常时回滚并且关闭数据库连接
            connection.rollback()
            connection.close()
            return "Something went wrong while adding employee."
    # 显示添加员工页面
    return render_template('add_employee.html')

# 修改员工页面
@app.route('/edit_employee/<id>', methods=['GET', 'POST'])
def edit_employee(id):
    # 提交表单时
    if request.method == 'POST':
        try:
            # 获取表单提交的数据
            name = request.form['name']
            email = request.form['email']
            address = request.form['address']
            with connection.cursor() as cursor:
                # SQL更新语句
                sql = "UPDATE employees SET name=%s, email=%s, address=%s WHERE id=%s"
                # 执行更新语句
                cursor.execute(sql, (name, email, address, id))
            # 提交到数据库执行
            connection.commit()
            # 重定向到员工列表页面
            return redirect('/', code=302)
        except:
            # 出现异常时回滚并且关闭数据库连接
            connection.rollback()
            connection.close()
            return "Something went wrong while updating employee."
    else:
        try:
            with connection.cursor() as cursor:
                # SQL查询语句
                sql = "SELECT * FROM employees WHERE id=%s"
                # 执行查询语句
                cursor.execute(sql, (id))
                # 获取指定员工信息
                employee = cursor.fetchone()
            # 渲染指定模板并传递数据
            return render_template('edit_employee.html', employee=employee)
        except:
            # 出现异常时回滚并且关闭数据库连接
            connection.rollback()
            connection.close()
            return "Something went wrong while displaying employee."

# 删除员工
@app.route('/delete_employee/<id>', methods=['GET', 'POST'])
def delete_employee(id):
    try:
        with connection.cursor() as cursor:
            # SQL删除语句
            sql = "DELETE FROM employees WHERE id=%s"
            # 执行删除语句
            cursor.execute(sql, (id))
        # 提交到数据库执行
        connection.commit()
        # 重定向到员工列表页面
        return redirect('/', code=302)
    except:
        # 出现异常时回滚并且关闭数据库连接
        connection.rollback()
        connection.close()
        return "Something went wrong while deleting employee."

# 应用启动
if __name__ == '__main__':
    app.run(debug=True)

