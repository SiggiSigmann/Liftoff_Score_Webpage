CREATE DATABASE LIFTOFF_DATA;

USE LIFTOFF_DATA;

CREATE USER 'test'@'%' IDENTIFIED BY '1234567';
GRANT ALL PRIVILEGES ON LIFTOFF_DATA . * TO 'test'@'%';

CREATE TABLE USERS(
    userid int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    username varchar(25) NOT NULL,
    usercolor varchar(7) NOT NULL
);
ALTER TABLE USERS AUTO_INCREMENT=0;

CREATE TABLE DRONES(
    droneid int PRIMARY KEY Not Null AUTO_INCREMENT,
    dronename varchar(25)
);
ALTER TABLE DRONES AUTO_INCREMENT=0;

CREATE TABLE MAPS(
    mapid int PRIMARY KEY AUTO_INCREMENT  NOT NULL,
    mapname varchar(50) NOT NULL
);
ALTER TABLE MAPS AUTO_INCREMENT=0;

CREATE TABLE TRACKS(
    mapid int  NOT NULL,
    trackid int  NOT NULL,
    trackname varchar(50)  NOT NULL,
    hardness int Not Null,
    FOREIGN KEY (mapid) REFERENCES MAPS(mapid),
    PRIMARY KEY (mapid, trackid)
);

CREATE TABLE RESULTS(
    resultid int AUTO_INCREMENT NOT NULL PRIMARY KEY,
    mapid int  NOT NULL,
    trackid int  NOT NULL,
    userid int NOT NULL,
    droneid int NOT NULL,
    FOREIGN KEY userref (userid) REFERENCES USERS(userid),
    FOREIGN KEY droneref (droneid) REFERENCES DRONES(droneid),
    FOREIGN KEY trackref (trackid, mapid) REFERENCES TRACKS(mapid, trackid),
    resulttimestamp DATETIME NOT NULL
);
ALTER TABLE RESULTS AUTO_INCREMENT=0;

INSERT INTO MAPS 
    (mapname) 
VALUES 
    ("Straw Bale"),
    ("Pine Valley"),
    ("Minus Two"),
    ("Autume Fields"),
    ("Hanga C03"),
    ("Liftoff arena"),
    ("Dubai Legend"),
    ("Hanover"),
    ("Paris Drone"),
    ("The Pid"),
    ("The Green"),
    ("Hall 26"),
    ("Bardwells Yard"),
    ("Bango City"),
    ("RussianWoodpecker");

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (1, 1, "1", 6),
    (1, 2, "2", 6),
    (1, 3, "3", 3),
    (1, 4, "4", 4),
    (1, 5, "5", 3),
    (1, 6, "6", 1);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (2, 1, "1", 4),
    (2, 2, "2", 6),
    (2, 3, "3", 4),
    (2, 4, "4", 4),
    (2, 5, "5", 5);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (3, 1, "1", 6),
    (3, 2, "2", 6),
    (3, 3, "3", 6),
    (3, 4, "4", 6),
    (3, 5, "5", 6);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (4, 1, "1", 4),
    (4, 2, "2", 6),
    (4, 3, "3", 4),
    (4, 4, "4", 4),
    (4, 5, "5", 6),
    (4, 6, "6", 5);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (5, 1, "1", 4);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (6, 1, "Dover Innternationals  IDRA", 5),
    (6, 2, "Eastside FPV Meet", 6),
    (6, 3, "FormulaFPV", 6),
    (6, 4, "1", 6),
    (6, 5, "2", 6),
    (6, 6, "3", 4),
    (6, 7, "4", 4),
    (6, 8, "5", 6),
    (6, 9, "6", 6);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (7, 1, "1", 6);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (8, 1, "1", 0),
    (8, 2, "2", 6),
    (8, 3, "3", 4),
    (8, 4, "4", 4),
    (8, 5, "5", 4);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (9, 1, "1", 6),
    (9, 2, "2", 6),
    (9, 3, "3", 6),
    (9, 4, "4", 6),
    (9, 5, "5", 6);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (10, 1, "1", 4),
    (10, 2, "2", 4),
    (10, 3, "3", 4),
    (10, 4, "4", 4),
    (10, 5, "5", 7),
    (10, 6, "6", 4);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (11, 1, "1", 6),
    (11, 2, "2", 4),
    (11, 3, "3", 4),
    (11, 4, "4", 4),
    (11, 5, "5", 3);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (12, 1, "1", 6),
    (12, 2, "2", 6),
    (12, 3, "3", 3),
    (12, 4, "4", 3),
    (12, 5, "5", 6);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (13, 1, "1", 8),
    (13, 2, "2", 6),
    (13, 3, "3", 5),
    (13, 4, "4", 4),
    (13, 5, "5", 4),
    (13, 6, "6", 4);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (14, 1, "1", 4),
    (14, 2, "2", 6),
    (14, 3, "3", 6),
    (14, 4, "4", 6),
    (14, 5, "5", 5);

INSERT INTO TRACKS
    (mapid, trackid, trackname, hardness)
VALUES
    (15, 1, "1", 6);

/* Todo: Remove user insertion*/
INSERT INTO USERS VALUES (1, "ZebraFPV", "#FF0000");