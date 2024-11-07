-- initialize
delete from classroom;
delete from event;
delete from price;
delete from time_slot;
delete from user;
delete from hold_info;
delete from lend;
delete from manage;
delete from take_info;
delete from usage_info;

-- classroom data
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('1101','Heping I','H108'),
  ('1102','Heping I','H108'),
  ('1104','Heping I','H108'),
  ('1105','Heping I','H108'),
  ('1106','Heping I','H108'),
  ('1107','Heping I','H108'),
  ('1108','Heping I','H108'),
  ('1109','Heping I','H108'),
  ('1201','Heping I','H108'),
  ('1202','Heping I','H108');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('1203','Heping I','H108'),
  ('1204','Heping I','H108'),
  ('1205','Heping I','H108'),
  ('1206','Heping I','H108'),
  ('1207','Heping I','H108'),
  ('1208','Heping I','H108'),
  ('1301','Heping I','H108'),
  ('1302','Heping I','H108'),
  ('1304','Heping I','H108'),
  ('1305','Heping I','H108');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('1306','Heping I','H108'),
  ('1307','Heping I','H108'),
  ('1401','Heping I','H108'),
  ('1402','Heping I','H108'),
  ('2101','Heping I','H107'),
  ('2102','Heping I','H107'),
  ('2103','Heping I','H107'),
  ('2104','Heping I','H107'),
  ('2105','Heping I','H107'),
  ('2106','Heping I','H107');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('2201','Heping I','H107'),
  ('2202','Heping I','H107'),
  ('2203','Heping I','H107'),
  ('2204','Heping I','H107'),
  ('2205','Heping I','H107'),
  ('2206','Heping I','H107'),
  ('2301','Heping I','H107'),
  ('2302','Heping I','H107'),
  ('2303','Heping I','H107'),
  ('2304','Heping I','H107');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('2305','Heping I','H107'),
  ('2306','Heping I','H107'),
  ('2401','Heping I','H107'),
  ('2402A','Heping I','H107'),
  ('2403','Heping I','H107'),
  ('2404','Heping I','H107'),
  ('2405','Heping I','H107'),
  ('2406','Heping I','H107'),
  ('3105','Heping I','H110'),
  ('3201','Heping I','H110');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('3202','Heping I','H110'),
  ('3203','Heping I','H110'),
  ('3204','Heping I','H110'),
  ('3205','Heping I','H110'),
  ('3206','Heping I','H110'),
  ('3301','Heping I','H110'),
  ('3302','Heping I','H110'),
  ('3303','Heping I','H110'),
  ('3304','Heping I','H110'),
  ('3305','Heping I','H110');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('3306','Heping I','H110'),
  ('3401','Heping I','H110'),
  ('3402','Heping I','H110'),
  ('3403','Heping I','H110'),
  ('3404','Heping I','H110'),
  ('3406','Heping I','H110'),
  ('3407','Heping I','H110'),
  ('7202','Heping II','H210'),
  ('7210','Heping II','H210'),
  ('7508','Heping II','H210');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('7509','Heping II','H210'),
  ('8103','Heping II','H205'),
  ('8201','Heping II','H205'),
  ('8202','Heping II','H205'),
  ('B101','Gongguan','G109'),
  ('B102','Gongguan','G109'),
  ('B103','Gongguan','G109'),
  ('E101','Gongguan','G109'),
  ('E102','Gongguan','G109'),
  ('E201','Gongguan','G109');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('E202','Gongguan','G109'),
  ('E301','Gongguan','G109'),
  ('E302','Gongguan','G109'),
  ('G001','Gongguan','G105'),
  ('G002','Gongguan','G105'),
  ('G003','Gongguan','G105'),
  ('H001','Gongguan','G102'),
  ('H002','Gongguan','G102'),
  ('H201','Gongguan','G102'),
  ('H202','Gongguan','G102');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('H301','Gongguan','G102'),
  ('S101','Gongguan','G112'),
  ('S102','Gongguan','G112'),
  ('S201','Gongguan','G112'),
  ('S202','Gongguan','G112'),
  ('S203','Gongguan','G112'),
  ('S204','Gongguan','G112'),
  ('S301','Gongguan','G112'),
  ('S302','Gongguan','G112'),
  ('S303','Gongguan','G112');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('S304','Gongguan','G112'),
  ('S305','Gongguan','G112'),
  ('S306','Gongguan','G112'),
  ('S307','Gongguan','G112'),
  ('S401','Gongguan','G112'),
  ('S402','Gongguan','G112'),
  ('S403','Gongguan','G112'),
  ('S404','Gongguan','G112'),
  ('S406','Gongguan','G112'),
  ('S407','Gongguan','G112');
INSERT INTO classroom (Classroom_ID,Campus_ID,Building_ID) VALUES
  ('S501','Gongguan','G112'),
  ('S502','Gongguan','G112'),
  ('S503','Gongguan','G112'),
  ('S504','Gongguan','G112'),
  ('S505','Gongguan','G112'),
  ('S506','Gongguan','G112'),
  ('S601','Gongguan','G112'),
  ('S602','Gongguan','G112'),
  ('S603','Gongguan','G112'),
  ('S604','Gongguan','G112');
INSERT INTO classroom (Classroom_ID, Campus_ID, Building_ID) VALUES
  ('S605','Gongguan','G112'),
  ('S606','Gongguan','G112');

-- event data 
INSERT INTO event (Event_ID, Info, Cost) VALUES
(1, 'Graduation', 10000),
(2, 'DBMS Final report', 0),
(3, 'OS Final exam', 0),
(4, 'Conference', 0),
(5, 'Celebration', 500);

-- price data
INSERT INTO price (Role, fee, Classroom_ID) VALUES
("Student", 100, '1101'),
("Teacher", 100, '1101'),
("Guest", 200, '1101'),
("Student", 150, '1102'),
("Teacher", 150, '1102'),
("Guest", 250, '1102'),
("Student", 200, '1104'),
("Teacher", 250, '1104'),
("Guest", 300, '1104');

-- time_slot data
INSERT INTO time_slot (Time_slot_ID,Start_time,End_time) VALUES
	 (1,'08:00:00','09:00:00'),
	 (2,'09:00:00','10:00:00'),
	 (3,'10:00:00','11:00:00'),
	 (4,'11:00:00','12:00:00'),
	 (5,'12:00:00','13:00:00'),
	 (6,'13:00:00','14:00:00'),
	 (7,'14:00:00','15:00:00'),
	 (8,'15:00:00','16:00:00'),
	 (9,'16:00:00','17:00:00'),
	 (10,'17:00:00','18:00:00');
INSERT INTO time_slot (Time_slot_ID,Start_time,End_time) VALUES
	 (11,'18:00:00','19:00:00'),
	 (12,'19:00:00','20:00:00'),
	 (13,'20:00:00','21:00:00'),
	 (14,'21:00:00','22:00:00');

-- user data 
INSERT INTO user VALUES
('root', 'Admin', 'root@example.com', 'root', '123', 'Super user', 'su', NULL),
('U1', 'Student', 'student1@example.com', 'pass1234', '1234567890', 'John Doe', 'johndoe', NULL),
('U2', 'Teacher', 'teacher1@example.com', 'pass5678', '0987654321', 'Jane Roe', 'janeroe', NULL),
('40973036H', 'Howard', 'howard@example.com', 'pass5678', '0987654321', 'Howardliu', 'hcliu', NULL),
('U3', 'Guest', 'guest1@example.com', 'pass91011', '1029384756', 'Alex Smith', 'alexsmith', NULL);


-- hold_info data
INSERT INTO hold_info (event_id, user_id) VALUES 
(1, 'U1'),
(2, '40973036H'),
(3, 'U1'),
(4, 'U2'),
(5, 'U3');

-- lend data
INSERT INTO lend VALUES
("U1", '1101', 1, '2024-05-25 00:00:00', '2024-06-10 01:53:47'),
("U1", '1101', 2, '2024-05-25 00:00:00', '2024-06-10 01:53:47'),
("U1", '1101', 3, '2024-05-25 00:00:00', '2024-06-10 01:53:47'),
("40973036H", '2304', 5, '2024-06-14 00:00:00', '2024-06-10 01:53:47'),
("U1", '1101', 8, '2024-05-25 00:00:00', '2024-06-10 01:53:47'),
("U2", '1101', 5, '2024-05-25 00:00:00', '2024-06-10 01:53:47'),
("U3", '1101', 6, '2024-05-25 00:00:00', '2024-06-10 01:53:47');

-- usage_info data
INSERT INTO usage_info(Event_ID, Time_slot_ID, Approval_Status, Approval_Message, Date, Classroom_ID)VALUES
(1, 1, 'Pending', NULL, '2024-05-25 00:00:00', '1101'),
(1, 2, 'Pending', NULL, '2024-05-25 00:00:00', '1101'),
(1, 3, 'Pending', NULL, '2024-05-25 00:00:00', '1101'),
(2, 5, 'Pending', NULL, '2024-06-14 00:00:00', '2304'),
(3, 8, 'Pending', NULL, '2024-05-25 00:00:00', '1101'),
(4, 5, 'Pending', NULL, '2024-05-25 00:00:00', '1101'),
(5, 6, 'Pending', NULL, '2024-05-25 00:00:00', '1101');

-- manage data
INSERT INTO manage VALUES
('root', '1101'),
('root', '2304');

-- take_info data
INSERT INTO take_info VALUES
(1, 1, '2024-05-25 00:00:00'),
(1, 2, '2024-05-25 00:00:00'),
(1, 3, '2024-05-25 00:00:00'),
(2, 5, '2024-06-14 00:00:00'),
(3, 8, '2024-05-25 00:00:00'),
(4, 5, '2024-05-25 00:00:00'),
(5, 6, '2024-05-25 00:00:00');
