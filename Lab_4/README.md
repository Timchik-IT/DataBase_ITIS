# Лабораторная работа 4. Вариант 9.

## 1) Вывести StudentId, StudentName, GroupId по :StudentId:
   - Π(StudentId, StudentName, GroupId)(σ(StudentId=':StudentId')(Students))
   ```sql
   SELECT StudentId, StudentName, GroupId 
   FROM Students 
   WHERE StudentId = ':StudentId';
   ```

## 2) Вывести StudentId, StudentName, GroupName по :StudentName:
   - Π(StudentId, StudentName, GroupName)((Students ⨝ Groups) ⨝ σ(StudentName=':StudentName')(Students))
   ```sql
   SELECT S.StudentId, S.StudentName, G.GroupName 
   FROM Students S 
   JOIN Groups G ON S.GroupId = G.GroupId 
   WHERE StudentName = ':StudentName';
   ```

## 3) Вывести StudentId, StudentName, GroupId по :Mark, :LecturerName:
   - Π(S.StudentId, S.StudentName, S.GroupId)((Students as S) ⨝ (Marks as M) ⨝ (Plan as P) ⨝ (Lecturers as L) 
     σ(M.Mark=':Mark' AND L.LecturerName=':LecturerName' AND S.StudentId = M.StudentId AND M.CourseId = P.CourseId 
     AND P.LecturerId = L.LecturerId AND S.GroupId = P.GroupId))
   ```sql
   SELECT S.StudentId, S.StudentName, S.GroupId 
   FROM Students S 
   JOIN Marks M ON S.StudentId = M.StudentId 
   JOIN Plan P ON M.CourseId = P.CourseId AND S.GroupId = P.GroupId 
   JOIN Lecturers L ON P.LecturerId = L.LecturerId 
   WHERE M.Mark = ':Mark' AND L.LecturerName = ':LecturerName';
   ```

## 4) Вывести StudentId, StudentName, GroupId по :CourseName:
   - Π(S.StudentId, S.StudentName, S.GroupId)((Students as S) ⨝ (Plan as P) ⨝ (Courses as C) 
     σ(C.CourseName=':CourseName' AND P.CourseId = C.CourseId AND S.GroupId = P.GroupId)
   ```sql
   SELECT S.StudentId, S.StudentName, S.GroupId 
   FROM Students S 
   JOIN Plan P ON S.GroupId = P.GroupId 
   JOIN Courses C ON P.CourseId = C.CourseId 
   WHERE C.CourseName = ':CourseName';
   ```

## 5) Для каждого студента ФИО и названия дисциплин есть, но у него не 4 или 5 StudentName, CourseName:
   - Π(S.StudentName, C.CourseName)(Students as S ⨝ Plan as P ⨝ Courses as C) - 
     Π(S.StudentName, C.CourseName)((Π(S.StudentName, C.CourseName)(Students as S ⨝ Plan as P ⨝ Courses as C)) ⨝ (Π(S.StudentName, C.CourseName)(Students as S ⨝ Plan as P ⨝ Courses as C)))
   ```sql
   SELECT S.StudentName, C.CourseName
   FROM Students S
   JOIN Plan P ON S.GroupId = P.GroupId
   JOIN Courses C ON P.CourseId = C.CourseId
   WHERE (S.StudentName, C.CourseName) NOT IN (
       SELECT S.StudentName, C.CourseName
       FROM Students S
       JOIN Plan P ON S.GroupId = P.GroupId
       JOIN Courses C ON P.CourseId = C.CourseId
       WHERE S.StudentName = 'StudentName1' OR S.StudentName = 'StudentName2'
           OR C.CourseName = 'CourseName1' OR C.CourseName = 'CourseName2'
   );
   ```

## 6) Вывести идентификаторы студентов по преподавателю не имеющих ни одной оценки у преподавателя StudentId по :LecturerName:
   - Π(S.StudentId)((Students as S) - (Π(S.StudentId)(Students as S ⨝ Marks as M ⨝ Plan as P ⨝ Lecturers as L 
     σ(L.LecturerName = ':LecturerName' AND S.StudentId = M.StudentId AND M.CourseId = P.CourseId AND P.LecturerId = L.LecturerId)))   
     ```sql
     SELECT DISTINCT S.StudentId
     FROM Students S
     JOIN Plan P ON S.GroupId = P.GroupId
     JOIN Lecturers L ON P.LecturerId = L.LecturerId
     WHERE L.LecturerName = ':LecturerName' AND S.StudentId NOT IN (
         SELECT M.StudentId
         FROM Marks M
         JOIN Plan P ON M.CourseId = P.CourseId
         JOIN Lecturers L ON P.LecturerId = L.LecturerId
         WHERE L.LecturerName = ':LecturerName'
     );
     ```

## 7) Вывести группы и дисциплины, такие что все студенты группы имеют оценку по этой дисциплине. Идентификаторы (GroupId, CourseId):
   - Π(P.GroupId, P.CourseId)(Plan as P) - (Π(P.GroupId, P.CourseId)(Plan as P ⨝ Students as S) - 
     (Π(P.GroupId, P.CourseId)(Plan as P ⨝ Students as S ⨝ Marks as M))
   ```sql
   SELECT P.GroupId, P.CourseId
   FROM Plan P
   WHERE P.CourseId NOT IN (
       SELECT M.CourseId
       FROM Marks M
       JOIN Students S ON M.StudentId = S.StudentId
       WHERE S.GroupId = P.GroupId
   );
   ```

## 8) Вывести суммарный балл каждой группы:
   - Σ(M.Mark)((Students as S) ⨝ (Marks as M) σ(S.StudentId = M.StudentId) ⨝ Π(S.GroupId, M.Mark)(Students as S ⨝ Marks as M))
   ```sql
   SELECT S.GroupId, SUM(M.Mark) AS TotalMarks
   FROM Marks M
   JOIN Students S ON M.StudentId = S.StudentId
   GROUP BY S.GroupId;
   ```

## 9) Средний балл средних баллов студентов каждой группы:

1. Вычисление среднего балла каждого студента:
   - π(StudentId, GroupId, AVG(Mark) as AvgMark (σ(StudentId = StudentId)(Students ⨝ Marks))

2. Вычисление среднего балла каждой группы из средних баллов студентов:
   - π(GroupId, AVG(AvgMark) AS AverageGroupAvgMark (результат_1 Группировка по GroupId))
  
  ```sql
   SELECT S.GroupId, AVG(T.AvgMark) AS AverageGroupAvgMark
   FROM (
       SELECT S.StudentId, S.GroupId, AVG(M.Mark) AS AvgMark
       FROM Students S
       JOIN Marks M ON S.StudentId = M.StudentId
       GROUP BY S.StudentId, S.GroupId
   ) AS T
   GROUP BY S.GroupId;
   ```

## 10) Для каждого студента: число дисциплин, количество сданных дисциплин и количество несданных дисциплин:
1. Подсчет общего числа дисциплин для каждого студента:
   - π(StudentId, COUNT(CourseId) AS Total (Students ⨝ Plan Группировка по StudentId)

2. Подсчет сданных дисциплин для каждого студента:
   - π(StudentId, COUNT(CourseId) AS Passed (Marks WHERE Mark >= 60 Группировка по StudentId)

3. Получение сведений о количестве несданных дисциплин для каждого студента:
   - Объединение предыдущих результатов для вычисления количества несданных дисциплин
   - Обработка NULL значений, если студент не имеет сданных дисциплин

   ```sql
    WITH StudentsDisciplines AS (
        SELECT S.StudentId, COUNT(DISTINCT P.CourseId) AS Total
        FROM Students S
        JOIN Plan P ON S.GroupId = P.GroupId
        GROUP BY S.StudentId
    ),
    PassedDisciplines AS (
        SELECT M.StudentId, COUNT(DISTINCT M.CourseId) AS Passed
        FROM Marks M
        WHERE M.Mark >= 60  -- Предположим, что сдача начинается с оценки 60
        GROUP BY M.StudentId
    )
    SELECT SD.StudentId, SD.Total, COALESCE(PD.Passed, 0) AS Passed, (SD.Total - COALESCE(PD.Passed, 0)) AS Failed
    FROM StudentsDisciplines SD
    LEFT JOIN PassedDisciplines PD ON SD.StudentId = PD.StudentId;
    ```
   
