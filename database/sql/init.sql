CREATE DATABASE LIFTOFF_DATA;

USE LIFTOFF_DATA;

CREATE USER 'test'@'%' IDENTIFIED BY '1234567';
GRANT ALL PRIVILEGES ON networkdata . * TO 'test'@'%';

CREATE TABLE USERS(
    userid int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    username varchar(25) NOT NULL,
    usercolor varchar(7) NOT NULL
);
ALTER TABLE USERS AUTO_INCREMENT=0;

CREATE TABLE MAPS(
    mapid int PRIMARY KEY AUTO_INCREMENT  NOT NULL,
    mapname varchar(50) NOT NULL
);
ALTER TABLE MAPS AUTO_INCREMENT=0;

CREATE TABLE TRACKS(
    mapid int  NOT NULL,
    trackid int NOT NULL,
    trackname varchar(50)  NOT NULL,
    FOREIGN KEY (mapid) REFERENCES MAPS(mapid),
    PRIVATE KEY (mapid, trackid)
);

CREATE TABLE RESULT(
    resultid int AUTO_INCREMENT NOT NULL PRIMARY KEY,
    userid int NOT NULL,
    mapid int NOT NULL,
    trackid int NOT NULL,
    FOREIGN KEY (userid) REFERENCES USERS(userid)  NOT NULL,
    FOREIGN KEY (mapid, trackid) REFERENCES TRACKS(mapid, trackid) NOT NULL,
    resulttimestamp DATETIME NOT NULL
);
ALTER TABLE RESULT AUTO_INCREMENT=0;





