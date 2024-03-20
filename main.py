import sqlite3

conn = sqlite3.connect('many_to_many_db.db')

conn.execute("DROP TABLE IF EXISTS Relationships")
conn.execute("DROP TABLE IF EXISTS Student")
conn.execute("DROP TABLE IF EXISTS Advisor")

conn.executescript('''
CREATE TABLE Advisor( 
AdvisorID INTEGER NOT NULL PRIMARY KEY, 
AdvisorName TEXT NOT NULL
);

CREATE TABLE Student( 
StudentID INTEGER NOT NULL PRIMARY KEY, 
StudentName TEXT NOT NULL
); 

CREATE TABLE Relationships(
StudentID INTEGER NOT NULL, 
AdvisorID INTEGER NOT NULL, 
FOREIGN KEY(StudentID) REFERENCES Student(StudentID), 
FOREIGN KEY(AdvisorID) REFERENCES Advisor(AdvisorID), 
PRIMARY KEY(StudentID, AdvisorID)
);

INSERT INTO Advisor(AdvisorID, AdvisorName) VALUES 
(1,"John Paul"), 
(2,"Anthony Roy"), 
(3,"Raj Shetty"), 
(4,"Sam Reeds"), 
(5,"Arthur Clintwood"); 

INSERT INTO Student(StudentID, StudentName) VALUES 
(501,"Geek1"), 
(502,"Geek2"), 
(503,"Geek3"), 
(504,"Geek4"), 
(505,"Geek5"), 
(506,"Geek6"), 
(507,"Geek7"), 
(508,"Geek8"), 
(509,"Geek9"), 
(510,"Geek10"); 

INSERT INTO Relationships(StudentID, AdvisorID) VALUES
(501, 1),
(502, 1),
(503, 2),
(501, 2),
(501, 3),
(502, 4),
(503, 4),
(506, 5),
(507, 5),
(510, 1),
(503, 3),
(501, 5),
(507, 4),
(508, 4),
(509, 3),
(510, 5),
(510, 2),
(506, 2), 
(504, 4);
''')

conn.execute("DROP TABLE IF EXISTS Advisor_Student_Relationship")
conn.execute('''CREATE TABLE Advisor_Student_Relationship AS SELECT a.AdvisorID, a.AdvisorName, s.StudentID,
s.StudentName FROM Advisor AS a INNER JOIN Relationships AS r ON a.AdvisorID = r.AdvisorID
INNER JOIN Student AS s ON s.StudentID = r.StudentID
''')

conn.commit()

result = conn.execute('''SELECT a.AdvisorID, a.AdvisorName, COUNT(a.StudentID) FROM Advisor_Student_Relationship AS a
GROUP BY a.AdvisorID;
''')
for i in result.fetchall():
    print("Advisor {} with ID {} has {} students.".format(i[1], i[0], i[2]))

conn.close()
