# Лабораторная работа 3. Вариант 9.

## Работа и бенчмарк анализ индексов.

### Три сценария использования базы данных и запросы:

#### 1. **Сценарий: Вычисление общей нагрузки по часам для каждого преподавателя:**
```sql
SELECT Teachers.LastName, SUM(Workload.Hours) AS TotalHours
FROM Teachers
JOIN Workload ON Teachers.TeacherCode = Workload.TeacherCode
GROUP BY Teachers.LastName;
```

#### 2. **Сценарий: Получение информации о группах с определенной специальностью и количеством студентов более 50:**
```sql
SELECT Groups.GroupNumber, Groups.Specialty, Groups.NumberOfStudents
FROM Groups
WHERE Groups.Specialty = 'Computer Science' AND Groups.NumberOfStudents > 50;
```

#### 3. **Сценарий: Определение преподавателей с опытом более 10 лет и их общая загруженность:**
```sql
SELECT Teachers.LastName, Teachers.Experience, SUM(Workload.Hours) AS TotalWorkloadHours
FROM Teachers
JOIN Workload ON Teachers.TeacherCode = Workload.TeacherCode
WHERE Teachers.Experience > 10
GROUP BY Teachers.LastName, Teachers.Experience;
```
## Бенчмарк без индексов

//TODO фотки бенчмарков

## Создание индексов для первого запроса:

#### 1. **B-tree индекс:**
```sql
CREATE INDEX idx_total_hours_btree ON Workload(Hours);
```

#### 2. **Включенный индекс (Index-Only Scan):**
```sql
CREATE INDEX idx_included_index ON Workload(TeacherCode) INCLUDE (Hours);
```

#### 3. **Условный индекс (Conditional Index):**
```sql
CREATE INDEX idx_conditional_index ON Teachers(Experience) WHERE Experience > 5;
```

## Создание индексов для второго запроса:

#### 1. **B-tree индекс:**
```sql
CREATE INDEX idx_specialty_btree ON Groups(Specialty);
```

#### 2. **Включенный индекс (Index-Only Scan):**
```sql
CREATE INDEX idx_included_index_group ON Groups(Number_Of_Students) INCLUDE (GroupNumber);
```

#### 3. **Условный индекс (Conditional Index):**
```sql
CREATE INDEX idx_conditional_index_group ON Groups(Specialty) WHERE Specialty = 'Computer Science';
```

## Создание индексов для третьего запроса:

#### 1. **B-tree индекс:**
```sql
CREATE INDEX idx_experience_btree ON Teachers(Experience);
```

#### 2. **Включенный индекс (Index-Only Scan for Total Workload):**
```sql
CREATE INDEX idx_included_index_workload ON Teachers(TeacherCode) INCLUDE (Experience);
```

#### 3. **Условный индекс (Conditional Index for Experience > 10 years):**
```sql
CREATE INDEX idx_conditional_index_experience ON Teachers(TeacherCode, Experience) WHERE Experience > 10;
```



