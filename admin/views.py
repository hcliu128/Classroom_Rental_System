# admin/views.py
from flask import render_template, request, jsonify, redirect, session, flash
from . import admin_bp
from datetime import datetime


@admin_bp.route("/")
def home():
    if ('user_type' not in session or session['user_type'] != "Admin"):
        return "<script>alert('請先登入!'); window.location.href = '/auth/login';</script>";
    from app import connection
    user_id = connection.get_one_data(f"SELECT user_id FROM user WHERE user_name='{session['username']}'" )[0]
    data = connection.get_all_data(f"SELECT E.Event_ID, E.Info, C.Classroom_ID, U.User_ID, U.Name, U.Email, T.time_slot_id, T.Start_time, T.End_time, UI.Date FROM event E JOIN usage_info UI ON E.Event_ID = UI.Event_ID JOIN time_slot T ON UI.Time_slot_ID = T.Time_slot_ID JOIN classroom C ON UI.Classroom_ID = C.Classroom_ID JOIN hold_info HI ON E.Event_ID = HI.Event_ID JOIN user U ON HI.User_ID = U.User_ID JOIN manage m ON m.user_id = '{user_id}' and m.classroom_id = UI.classroom_id WHERE UI.Approval_Status = 'Pending';")
    attribute = ['Event ID', 'Info', 'Classroom ID', 'Student ID', 'Name', 'Email', 'time id', 'Start_time', 'End_time', 'Date']
    return render_template('home.html', data = data, attribute = attribute, user_name = session['username'])

@admin_bp.route('/add_classroom')
def add_classroom():
    if ('user_type' not in session or session['user_type'] != "Admin"):
        return "<script>alert('請先登入!'); window.location.href = '/auth/login';</script>";
    data = connection.get_all_data("SELECT Classroom_ID, Campus_ID, Building_ID FROM Classroom;")
    return render_template('add_classroom.html', data = data)

@admin_bp.route('/add_timeslot')
def add_timeslot():
    if ('user_type' not in session or session['user_type'] != "Admin"):
        return "<script>alert('請先登入!'); window.location.href = '/auth/login';</script>";
    data = connection.get_all_data("SELECT time_slot_id, start_time, end_time FROM time_slot;")
    return render_template('add_timeslot.html', data = data)

@admin_bp.route('/delete_account')
def delete_account():
    if ('user_type' not in session or session['user_type'] != "Admin"):
        return "<script>alert('請先登入!'); window.location.href = '/auth/login';</script>";
    data = connection.get_all_data("SELECT Type, User_ID, Email, Phone, Name, User_name FROM user;")
    attribute = ["Role", "User_ID", "Email", "Phone", "Name", "User_name"]
    return render_template('delete_account.html', data = data, attribute = attribute)

@admin_bp.route("/update_status", methods = ['POST'])
def update_status():
    data = request.get_json()
    try:
        reason = data.get('reason', None)
        print(f"{data['status']} & {reason} & {data['date']}")
        connection.execute_query(f"UPDATE usage_info SET approval_status = '{data['status']}', approval_message = '{reason}' WHERE event_id = {int(data['eid'])} and time_slot_id = {int(data['time_slot_id'])} and date = '{data['date']}'")
        return jsonify({'success': True})
    except:
        return jsonify({'error': 'Database update failed'}), 500

@admin_bp.route("/submit_timeslot", methods = ['POST'])
def submit_timeslot():
    try:
        current_id = connection.get_one_data("SELECT MAX(time_slot_id) FROM time_slot;")[0]
        start_time = request.form['start_time'] + ':00'
        end_time = request.form['end_time'] + ':00'
        connection.execute_query(f"INSERT INTO time_slot VALUES ({int(current_id) + 1}, '{start_time}',  '{end_time}');")
    except Exception as e:
        print(e)
        return jsonify({"status": "fail", "message": str(e)}), 500
    return "<script>alert('新增完成!'); window.location.href = '/admin';</script>";

@admin_bp.route("/submit_classroom", methods = ['POST'])
def submit_classroom():
    try:
        connection.execute_query(f"INSERT INTO classroom VALUES ('{request.form['classroom_ID']}', '{request.form['campus_ID']}', '{request.form['building_ID']}');")
        user_id = connection.get_one_data(f"SELECT user_id FROM user WHERE user_name='{session['username']}'" )[0]
        connection.execute_query(f"INSERT INTO manage (classroom_id, user_id) VALUES ('{request.form['classroom_ID']}', '{user_id}');")
        connection.commit()
        connection.execute_query(f"INSERT INTO Price (classroom_id, role, fee) VALUES ('{request.form['classroom_ID']}', 'Guest', '{request.form['guestfee']}');")
        connection.execute_query(f"INSERT INTO Price (classroom_id, role, fee) VALUES ('{request.form['classroom_ID']}', 'Teacher', '{request.form['teacherfee']}');")
        connection.execute_query(f"INSERT INTO Price (classroom_id, role, fee) VALUES ('{request.form['classroom_ID']}', 'Student', '{request.form['studentfee']}');")
    except Exception as e:
        print(e)
    return "<script>alert('新增完成!'); window.location.href = '/admin';</script>";

@admin_bp.route("/delete_user", methods = ['POST'])
def delete_user():
    data = request.get_json()
    try:
        connection.execute_query(f"DELETE FROM User WHERE user_id = '{data['user_id']}'")
        return jsonify({'success': True})
    except:
        return jsonify({'error': 'Database update failed'}), 500

from utils.time import *
from utils.db import connection

@admin_bp.route('/submit_lend', methods=['POST'])
def submit_lend():
    data = request.get_json()
    """
    {'event': '1',
    'room': '1101',
    'slots': [{'date': '2024-05-25', 'time_slot': '08:00 - 09:00'},
            {'date': '2024-05-25', 'time_slot': '10:00 - 11:00'}]}
    """

    classroom_id = data['room']
    print(data)
    cur = connection.cursor(buffered=True)


    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id FROM user WHERE user_name='{session['username']}'" )
    user_id = cursor.fetchone()[0]


    for slot in data['slots']:
        date = slot['date']
        time_slot = slot['time_slot']
        start_time, end_time = split_time_range(time_slot)
        q = "SELECT ts.Time_slot_ID FROM time_slot ts WHERE ts.Start_time=%s AND ts.End_time=%s"
        cur.execute(q, [start_time, end_time])
        time_slot_id = cur.fetchone()[0]

        # 檢查是否已經存在該紀錄(正常不會發生)
        q = """
        SELECT COUNT(*) FROM `lend`
        WHERE `User_ID`=%s AND `Classroom_ID`=%s AND `Time_slot_ID`=%s AND `Date`=%s
        """
        cur.execute(q, [user_id, classroom_id, time_slot_id, date])
        if cur.fetchone()[0] == 0:
            # 如果不存在，則進行INSERT操作
            q = """
            INSERT INTO `lend`
                    (`User_ID`, `Classroom_ID`, `Time_slot_ID`, `Date`, `Apply_time`)
            VALUES  (   %s,         %s,               %s,          %s,    CURDATE())
            """

            cur.execute(q, [user_id, classroom_id, time_slot_id, date])

    cur.close()

    return jsonify({'status': 'success', 'message': 'lend submitted successfully'})




@admin_bp.route('/add_lend', methods=['GET'])
def add_lend():

    # get args
    roomSel = request.args.get('roomSel', '1101')
    base_date_str = request.args.get('date', '2024-05-25')

    base_date = datetime.strptime(base_date_str, '%Y-%m-%d')
    week_dates = get_week_dates(base_date)
    week_dates_str = [d.strftime('%Y-%m-%d') for d in week_dates]


    cur = connection.cursor(buffered=True)

    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id FROM user WHERE user_name='{session['username']}'" )
    user_id = cursor.fetchone()[0]



    # get available time slots
    q = 'SELECT ts.`Start_time`, ts.`End_time` from time_slot ts'
    cur.execute(q)
    results = cur.fetchall()
    time_slots=[]
    for result in sorted(results):
        start_time = timedelta_to_hm(result[0])
        end_time = timedelta_to_hm(result[1])
        time_slots.append(start_time + ' - ' + end_time)


    # get available classrooms
    q = """
        SELECT
            m.`Classroom_ID`
        FROM
            manage m
        WHERE
            m.`user_id` = %s
    """
    classrooms = set()
    cur.execute(q, [user_id])
    results = cur.fetchall()
    for result in results:
        classrooms.add(result[0])


    if roomSel not in classrooms:
        roomSel = classrooms[0]

    # get datas
    q = """
        SELECT
            c.`Classroom_ID`,
            l.`Date`,
            ts.`Start_time`,
            ts.`End_time`
        FROM
            classroom c
            NATURAL JOIN lend l
            NATURAL JOIN time_slot ts
        WHERE
            l.`Date` BETWEEN %s AND %s
    """

    cur.execute(q, [week_dates_str[0], week_dates_str[-1]])

    results = cur.fetchall()
    not_availability = []

    for result in results:
        classroom = result[0]
        date = result[1].strftime('%Y-%m-%d')
        start_time = timedelta_to_hm(result[2])
        end_time = timedelta_to_hm(result[3])
        time_slot_str = f"{start_time} - {end_time}"
        not_availability.append((classroom, date, time_slot_str))

    availability = []
    for classroom in classrooms:
        for date in week_dates_str:
            for time_slot in time_slots:
                if (classroom, date, time_slot) not in not_availability:
                    availability.append((classroom, date, time_slot))

    cur.close()

    return render_template(
        'calendar2.html',
        rooms=classrooms,
        time_slots=time_slots,
        week_dates=week_dates,
        availability=availability,
        base_date=base_date.strftime('%Y-%m-%d'),
        roomSel=roomSel,
        event_ids=None
    )