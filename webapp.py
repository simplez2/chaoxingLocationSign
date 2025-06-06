from flask import Flask, request, render_template_string
from api import login, get_account_username, get_course, check_activity, loading_sign_page, sign_location

app = Flask(__name__)

INDEX_HTML = '''
<h2>Chaoxing Sign</h2>
<form method="post" action="/courses">
  <label>手机号: <input name="username" required></label><br>
  <label>密码: <input type="password" name="password" required></label><br>
  <label>经纬度: <input name="location" value="104.19107,30.827562" required></label><br>
  <label>地址名称: <input name="address" value="中国四川省成都市新都区新都街道南环路" required></label><br>
  <button type="submit">登录</button>
</form>
'''

COURSES_HTML = '''
<h2>选择课程签到</h2>
<form method="post" action="/sign">
  <input type="hidden" name="username" value="{{ username }}">
  <input type="hidden" name="password" value="{{ password }}">
  <input type="hidden" name="location" value="{{ location }}">
  <input type="hidden" name="address" value="{{ address }}">
  {% for idx, course in courses %}
    <div><input type="radio" name="course" value="{{ idx }}" required> {{ course.courseName }} {{ course.teacherName }}</div>
  {% endfor %}
  <button type="submit">签到</button>
</form>
'''

RESULT_HTML = '''
<h2>结果</h2>
<p>{{ message }}</p>
<a href="/">返回</a>
'''


def perform_sign(username: str, password: str, location: str, address: str, course_index: int) -> str:
    result = login(username, password)
    if not result.status:
        return f"登录失败: {result.msg}"
    account_username = get_account_username(result.data)
    result.data["account_username"] = account_username
    cookies = result.data
    course_list = get_course(cookies).course_list
    try:
        course = course_list[course_index]
    except Exception:
        return "课程序号无效"

    activity = check_activity(cookies, course.courseId, course.classId)
    if not activity.status:
        return f"{course.courseName} 没有活动: {activity.msg}"
    loading_sign_page(cookies, activity.activity_id, activity.classId, activity.courseId)
    lng, lat = location.split(',')
    resp = sign_location(cookies, activity.activity_id, address, float(lng), float(lat))
    return resp.msg


@app.route('/', methods=['GET'])
def index():
    return render_template_string(INDEX_HTML)


@app.route('/courses', methods=['POST'])
def courses():
    username = request.form['username']
    password = request.form['password']
    location = request.form['location']
    address = request.form['address']
    result = login(username, password)
    if not result.status:
        return render_template_string(RESULT_HTML, message=f"登录失败: {result.msg}")
    account_username = get_account_username(result.data)
    result.data["account_username"] = account_username
    cookies = result.data
    course_list = get_course(cookies).course_list
    return render_template_string(COURSES_HTML, username=username, password=password, location=location, address=address, courses=list(enumerate(course_list)))


@app.route('/sign', methods=['POST'])
def sign():
    username = request.form['username']
    password = request.form['password']
    location = request.form['location']
    address = request.form['address']
    course_index = int(request.form['course'])
    message = perform_sign(username, password, location, address, course_index)
    return render_template_string(RESULT_HTML, message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
