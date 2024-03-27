SELECT Teachers.LastName, SUM(Workload.Hours) AS TotalHours
FROM Teachers
JOIN Workload ON Teachers.TeacherCode = Workload.TeacherCode
GROUP BY Teachers.LastName;
