SELECT Teachers.LastName, Teachers.Experience, SUM(Workload.Hours) AS TotalWorkloadHours
FROM Teachers
JOIN Workload ON Teachers.TeacherCode = Workload.TeacherCode
WHERE Teachers.Experience > 10
GROUP BY Teachers.LastName, Teachers.Experience;
