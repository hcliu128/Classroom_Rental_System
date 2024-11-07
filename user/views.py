from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify , flash
from collections import defaultdict
from utils.time import *
from utils.db import connection
from utils.constant import goto_user
# from pprint import pprint
from . import user_bp


@user_bp.before_request
def before_request_handle():
    username = session.get('username')
    user_type = session.get('user_type')
    if not username or user_type not in goto_user:
        return redirect(url_for('auth.login'))



@user_bp.route('/')
def index():
    return render_template('index.html', username=session['username'])



@user_bp.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    data = request.get_json()
    """
    {'event': '1',
    'room': '1101',
    'slots': [{'date': '2024-05-25', 'time_slot': '08:00 - 09:00'},
            {'date': '2024-05-25', 'time_slot': '10:00 - 11:00'}]}
    """
    event_id = data['event']
    classroom_id = data['room']

    cur = connection.cursor(buffered=True)
    for slot in data['slots']:
        date = slot['date']
        time_slot = slot['time_slot']
        start_time, end_time = split_time_range(time_slot)
        q = "SELECT ts.Time_slot_ID FROM time_slot ts WHERE ts.Start_time=%s AND ts.End_time=%s"
        cur.execute(q, [start_time, end_time])
        time_slot_id = cur.fetchone()[0]

        # 檢查是否已經存在該紀錄
        q = """
        SELECT COUNT(*) FROM `usage_info`
        WHERE `Event_ID`=%s AND `Time_slot_ID`=%s AND `Classroom_ID`=%s AND `Date`=%s
        """
        cur.execute(q, [event_id, time_slot_id, classroom_id, date])
        if cur.fetchone()[0] == 0:
            # 如果不存在，則進行INSERT操作
            q = """
            INSERT INTO `usage_info`
                    (`Event_ID`, `Time_slot_ID`, `Approval_Status`, `Approval_Message`, `Date`, `Classroom_ID`)
            VALUES  (   %s,            %s,         'Pending',            NULL,           %s,       %s       )
            """
            print(q % (event_id, time_slot_id, date, classroom_id))
            cur.execute(q, [event_id, time_slot_id, date, classroom_id])
        else:
            # 如果存在，則進行UPDATE操作
            q = """
            UPDATE `usage_info`
            SET `Approval_Status` = 'Pending', `Approval_Message`= NULL
            WHERE `Date`= %s AND `Event_ID`=%s AND `Time_slot_ID`=%s AND `Classroom_ID`=%s
            """
            print(q % (date, event_id, time_slot_id, classroom_id))
            cur.execute(q, [date, event_id, time_slot_id, classroom_id])

    cur.close()

    return jsonify({'status': 'success', 'message': 'Reservation submitted successfully'})



@user_bp.route('/add_reservation', methods=['GET'])
def add_reservation():

    # get args
    username = session['username']
    roomSel = request.args.get('roomSel', '1101')
    base_date_str = request.args.get('date', '2024-05-25')

    base_date = datetime.strptime(base_date_str, '%Y-%m-%d')
    week_dates = get_week_dates(base_date)
    week_dates_str = [d.strftime('%Y-%m-%d') for d in week_dates]


    cur = connection.cursor(buffered=True)

    # get available time slots
    q = 'SELECT ts.`Start_time`, ts.`End_time` from time_slot ts'
    cur.execute(q)
    results = cur.fetchall()
    time_slots=[]
    for result in sorted(results):
        start_time = timedelta_to_hm(result[0])
        end_time = timedelta_to_hm(result[1])
        time_slots.append(start_time + ' - ' + end_time)


    # get available event_id
    event_ids = []
    q = """
        SELECT
            hi.Event_ID
        FROM
            hold_info hi
            NATURAL JOIN user u
        WHERE
            user_name = %s
    """
    cur.execute(q, [username])
    results = cur.fetchall()
    for result in results:
        event_ids.append(result[0])

    # get available classrooms
    q = """
        SELECT
            l.`Classroom_ID`
        FROM
            lend l
    """
    classrooms = set()
    cur.execute(q)
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
            AND NOT EXISTS (
                SELECT 1
                FROM usage_info ui
                NATURAL JOIN time_slot ts2
                WHERE
                    ui.Classroom_ID = c.Classroom_ID
                    AND ui.Date = l.Date
                    AND ts2.Start_time = ts.Start_time
                    AND ts2.End_time = ts.End_time
                    AND ui.Approval_Status <> 'Cancel'
                    AND ui.Approval_Status <> 'Decline'
            )
    """

    cur.execute(q, [week_dates_str[0], week_dates_str[-1]])

    results = cur.fetchall()
    availability = []

    for result in results:
        classroom = result[0]
        date = result[1].strftime('%Y-%m-%d')
        start_time = timedelta_to_hm(result[2])
        end_time = timedelta_to_hm(result[3])
        time_slot_str = f"{start_time} - {end_time}"
        availability.append((classroom, date, time_slot_str))

    cur.close()

    ret_dict = {'rooms': classrooms,
        'time_slots': time_slots,
        'week_dates': week_dates,
        'availability': availability,
        'base_date': base_date.strftime('%Y-%m-%d'),
        'roomSel': roomSel,
        'event_ids': event_ids}

    return render_template(
        'calendar.html',
        ret_dict=ret_dict
    )



@user_bp.route('/manage_reservation', methods=['GET'])
def manage_reservation():

    # get args
    username = session['username']
    roomSel = request.args.get('roomSel', '1101')
    base_date_str = request.args.get('date', '2024-05-25')

    print(base_date_str)

    base_date = datetime.strptime(base_date_str, '%Y-%m-%d')
    week_dates = get_week_dates(base_date)
    week_dates_str = [d.strftime('%Y-%m-%d') for d in week_dates]

    cur = connection.cursor(buffered=True)

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
            l.`Classroom_ID`
        FROM
            lend l
    """
    classrooms = set()
    cur.execute(q)
    results = cur.fetchall()
    for result in results:
        classrooms.add(result[0])

    if roomSel not in classrooms:
        roomSel = classrooms[0]

    # get datas
    q = """
    SELECT c.`Classroom_ID`, ui.`Date`, ts.`Start_time`, ts.`End_time`, e.`Info`, e.`Event_ID`, ui.Approval_Status
    FROM classroom c NATURAL JOIN usage_info ui NATURAL JOIN event e NATURAL JOIN hold_info NATURAL JOIN user u NATURAL JOIN time_slot ts
    WHERE u.`User_Name`=%s and ui.`Date` BETWEEN %s AND %s
    """

    cur.execute(q, [username, week_dates_str[0], week_dates_str[-1]])

    results = cur.fetchall()
    availability = []
    href_names = {}
    href_parms = {}
    for result in results:
        classroom = result[0]
        date = result[1].strftime('%Y-%m-%d')
        start_time = timedelta_to_hm(result[2])
        end_time = timedelta_to_hm(result[3])
        info = result[4]
        event_id = result[5]
        approval_status = result[6]
        # if approval_status in ['Cancel', 'Decline']:
        #     continue
        time_slot_str = f"{start_time} - {end_time}"
        availability.append((classroom, date, time_slot_str))
        href_names[(classroom, date, time_slot_str)] = f'{event_id}:{info}'
        href_parms[(classroom, date, time_slot_str)] = f'?event_id={event_id}'


    cur.close()

    ret_dict = {
        'rooms': classrooms,
        'time_slots': time_slots,
        'week_dates': week_dates,
        'availability': availability,
        'base_date': base_date.strftime('%Y-%m-%d'),
        'roomSel': roomSel,
        'href': 'user.edit_reservation',
        'href_names': href_names,
        'href_parms': href_parms
    }

    return render_template(
        'calendar.html',
        ret_dict=ret_dict
    )


@user_bp.route('/edit_reservation', methods=['GET', 'POST'])
def edit_reservation():
    if request.method == 'POST':
        event_id = request.form['event_id']
        action = request.form['action']

        event_id = request.args.get('event_id', '-1')

        cur = connection.cursor(buffered=True)

        if action == 'Cancel':
            q = """
                UPDATE usage_info ui
                NATURAL JOIN event e
                SET ui.Approval_Status = %s
                WHERE e.Event_ID = %s AND ui.Approval_Status <> 'Accept'
            """
        else:
            q = """
                UPDATE usage_info ui
                NATURAL JOIN event e
                SET ui.Approval_Status = %s
                WHERE e.Event_ID = %s AND ui.Approval_Status = 'Wait_For_Payment'
            """

        cur.execute(q, [action, event_id])


    username = session['username']
    event_id = request.args.get('event_id', '1')



    cur = connection.cursor(buffered=True)

    q = "SELECT u.`Type` FROM user u WHERE user_name=%s"
    cur.execute(q, [username])
    user_role = cur.fetchone()[0]


    classroom_data = defaultdict(lambda: defaultdict(list))
    classroom_fee = {}
    approval_status_data = defaultdict(lambda: defaultdict(defaultdict))
    approval_message_data = defaultdict(lambda: defaultdict(defaultdict))
    q = """
        SELECT
            c.`Classroom_ID`, ui.`Date`, ts.`Start_time`, ts.`End_time`, e.`Info`, e.`Event_ID`, ui.`Approval_Message`, ui.`Approval_Status`, p.Fee
        FROM
            classroom c NATURAL JOIN usage_info ui NATURAL JOIN event e NATURAL JOIN hold_info NATURAL JOIN user u NATURAL JOIN time_slot ts NATURAL JOIN price  p
        WHERE e.`Event_ID`=%s AND p.Role=%s
    """
    cur.execute(q, [event_id, user_role])
    results = cur.fetchall()
    cur.close()
    
    if not results:
        return "<script>alert('查無結果!'); window.history.go(-1);</script>"

    for result in results:
        classroom = result[0]
        date = result[1].strftime('%Y-%m-%d')
        start_time = timedelta_to_hm(result[2])
        end_time = timedelta_to_hm(result[3])
        time_slot = f"{start_time}-{end_time}"
        event_info = result[4]
        approval_message = result[6]
        approval_status = result[7]
        fee = result[8]

        # if approval_status in ['Cancel', 'Decline']:
        #     continue

        classroom_fee[classroom] = fee
        classroom_data[classroom][date].append(time_slot)
        approval_status_data[classroom][date][time_slot] = approval_status
        approval_message_data[classroom][date][time_slot] = approval_message

    from pprint import pprint

    pprint(classroom_data)
    total_cost = 0
    for classroom, dates in classroom_data.items():
        for date, times in dates.items():
            l = 0
            for time in times:
                if approval_status_data[classroom][date][time] == 'Wait_For_Payment':
                    l += 1
            total_cost += l * classroom_fee[classroom]


    return render_template('edit_reservation.html',
                           event_id=event_id,
                           event_info=event_info,
                           classroom_data=classroom_data,
                           approval_status=approval_status,
                           approval_message=approval_message,
                           approval_status_data=approval_status_data,
                           approval_message_data=approval_message_data,
                           total_cost=total_cost,
                           classroom_fee=classroom_fee
                        )



@user_bp.route('/classroom-schedule')
def classroom_schedule():
    cursor = connection.cursor()
    query = "SELECT Time_slot_ID, Start_time, End_time FROM time_slot"
    cursor.execute(query)
    time_slots = cursor.fetchall()
    cursor.close()
    return render_template('classroom_schedule.html', time_slots=time_slots)

@user_bp.route('/view_all_events')
def view_all_events():
    user_id = session['username']
    query = f"select e.Event_ID, e.Info from event e JOIN hold_info hi ON e.Event_ID = hi.Event_ID NATURAL JOIN user where user_name = '{user_id}';"
    
    cur = connection.cursor()
    cur.execute(query)
    events = cur.fetchall()
    cur.close()

    return render_template('all_events.html', events=events)

@user_bp.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_info = request.form.get('event_info')

        if not event_info:
            flash('活動描述是必填的！', 'danger')
            return redirect(url_for('user.index'))

        cur = connection.cursor()
        cur.execute("SELECT MAX(Event_ID) FROM event")
        max_id = cur.fetchone()[0]
        if max_id is None:
            max_id = 0
        event_name = f"Event {max_id + 1}"

        cur.execute(
            "INSERT INTO event (Event_ID , Info, Cost) VALUES (%s, %s, %s)",
            (max_id + 1, event_info, 0)  # 先填 Cost 為 0
        )
        connection.commit()
        cur = connection.cursor()
        query1 = f"SELECT user_id FROM user where user_name = '{session['username']}';"
        cur.execute(query1)  
        user_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO hold_info (User_ID , Event_ID) VALUES (%s, %s)",
            (user_id , max_id + 1)
        )
        connection.commit()
        cur.close()

        flash('活動添加成功！', 'success')
        return  "<script>alert('成功提交!'); window.location.href = '/user/';</script>";

    return render_template('add_event.html')
