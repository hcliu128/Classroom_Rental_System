-- team16.classroom definition

CREATE TABLE `classroom` (
  `Classroom_ID` varchar(50) NOT NULL,
  `Campus_ID` varchar(50) DEFAULT NULL,
  `Building_ID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Classroom_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.event definition

CREATE TABLE `event` (
  `Event_ID` int(20) NOT NULL,
  `Info` varchar(300) DEFAULT NULL,
  `Cost` int(11) DEFAULT NULL,
  PRIMARY KEY (`Event_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.price definition

CREATE TABLE `price` (
  `Role` varchar(50) NOT NULL,
  `Fee` int(11) DEFAULT NULL,
  `Classroom_ID` varchar(50) NOT NULL,
  PRIMARY KEY (`Role`, `Classroom_ID`),
  KEY `Classroom_ID` (`Classroom_ID`),
  CONSTRAINT `price_ibfk_1` FOREIGN KEY (`Classroom_ID`) REFERENCES `classroom` (`Classroom_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



-- team16.time_slot definition

CREATE TABLE `time_slot` (
  `Time_slot_ID` int(11) NOT NULL,
  `Start_time` TIME DEFAULT NULL,
  `End_time` TIME DEFAULT NULL,
  PRIMARY KEY (`Time_slot_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.user definition

CREATE TABLE `user` (
  `User_ID` varchar(50) NOT NULL,
  `Type` varchar(50) DEFAULT NULL,
  `Email` varchar(300) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Phone` varchar(50) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `User_Name` varchar(50) DEFAULT NULL,
  `Session_ID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`User_ID`),
  UNIQUE KEY `unique_username` (`User_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;




-- team16.hold_info definition

CREATE TABLE `hold_info` (
  `User_ID` varchar(50) NOT NULL,
  `Event_ID` int(11) NOT NULL,
  PRIMARY KEY (`User_ID`,`Event_ID`),
  KEY `Event_ID` (`Event_ID`),
  CONSTRAINT `hold_info_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `hold_info_ibfk_2` FOREIGN KEY (`Event_ID`) REFERENCES `event` (`Event_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.lend definition

CREATE TABLE `lend` (
  `User_ID` varchar(50) NOT NULL,
  `Classroom_ID` varchar(50) NOT NULL,
  `Time_slot_ID` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Apply_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`User_ID`,`Classroom_ID`,`Time_slot_ID`,`Date`),
  KEY `Classroom_ID` (`Classroom_ID`),
  KEY `FK_lend_Time_slot` (`Time_slot_ID`),
  CONSTRAINT `FK_lend_Time_slot` FOREIGN KEY (`Time_slot_ID`) REFERENCES `time_slot` (`Time_slot_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lend_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lend_ibfk_2` FOREIGN KEY (`Classroom_ID`) REFERENCES `classroom` (`Classroom_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.manage definition

CREATE TABLE `manage` (
  `User_ID` varchar(50) NOT NULL,
  `Classroom_ID` varchar(50) NOT NULL,
  PRIMARY KEY (`User_ID`,`Classroom_ID`),
  KEY `Classroom_ID` (`Classroom_ID`),
  CONSTRAINT `manage_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `manage_ibfk_2` FOREIGN KEY (`Classroom_ID`) REFERENCES `classroom` (`Classroom_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.take_info definition

CREATE TABLE `take_info` (
  `Event_ID` int(11) NOT NULL,
  `Time_slot_ID` int(11) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`Event_ID`,`Time_slot_ID`,`Date`),
  KEY `FK_take_info_Time_slot` (`Time_slot_ID`),
  CONSTRAINT `FK_take_info_Time_slot` FOREIGN KEY (`Time_slot_ID`) REFERENCES `time_slot` (`Time_slot_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `take_info_ibfk_1` FOREIGN KEY (`Event_ID`) REFERENCES `event` (`Event_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- team16.usage_info definition

CREATE TABLE `usage_info` (
  `Event_ID` int(11) NOT NULL,
  `Time_slot_ID` int(11) NOT NULL,
  `Classroom_ID` varchar(50) NOT NULL, 
  `Approval_Status` varchar(50) DEFAULT NULL,
  `Approval_Message` varchar(50) DEFAULT NULL,
  `Date` datetime DEFAULT NULL, 
  PRIMARY KEY (`Event_ID`, `Time_slot_ID`, `Classroom_ID`), 
  KEY `FK_usage_info_Time_slot` (`Time_slot_ID`),
  KEY `FK_usage_info_Classroom` (`Classroom_ID`), 
  CONSTRAINT `FK_usage_info_Time_slot` FOREIGN KEY (`Time_slot_ID`) REFERENCES `time_slot` (`Time_slot_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_usage_info_Classroom` FOREIGN KEY (`Classroom_ID`) REFERENCES `classroom` (`Classroom_ID`) ON DELETE CASCADE ON UPDATE CASCADE, 
  CONSTRAINT `usage_info_ibfk_1` FOREIGN KEY (`Event_ID`) REFERENCES `event` (`Event_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
