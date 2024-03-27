SELECT Groups.GroupNumber, Groups.Specialty, Groups.NumberOfStudents
FROM Groups
WHERE Groups.Specialty = 'Computer Science' AND Groups.NumberOfStudents > 50;
