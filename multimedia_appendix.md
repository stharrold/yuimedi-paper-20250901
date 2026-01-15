# Multimedia Appendix 1

## Appendix A: HIMSS Analytics Maturity Assessment Model (AMAM) Stages

+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage   | Name                         | Description                                                          | Key Capabilities                                                     |
+=========+==============================+======================================================================+======================================================================+
| Stage 0 | Data Collection              | Basic data capture without integration                               | Manual data entry, paper records                                     |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 1 | Data Verification            | Automated data validation and error checking                         | Basic quality controls, automated checks                             |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 2 | Data Utilization             | Standard reporting and basic analytics                               | Automated reports, dashboard creation                                |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 3 | Automated Decision Support   | Rule-based clinical and operational support                          | Clinical alerts, automated protocols                                 |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 4 | Population Health Analytics  | Population-level analysis and intervention                           | Cohort identification, risk stratification                           |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 5 | Predictive Analytics         | Statistical modeling and predictive capabilities                     | Predictive models, trend analysis                                    |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 6 | Cognitive Analytics          | Machine learning and AI integration                                  | Advanced AI, pattern recognition                                     |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+
| Stage 7 | Precision Medicine           | Personalized treatment and genomic integration                       | Personalized care, genomic analytics                                 |
+---------+------------------------------+----------------------------------------------------------------------+----------------------------------------------------------------------+

## Appendix B: Healthcare NL2SQL Query Examples

### Patient Population Analysis
**Natural Language**: "Show me all diabetic patients over 65 who had an HbA1c test in the last 6 months"

**Rationale**: Aligned with NCQA HEDIS measures for Comprehensive Diabetes Care (CDC), monitoring HbA1c testing compliance in older adult populations.

**Generated SQL**:
```sql
SELECT p.patient_id, p.age, l.test_date, l.result_value
FROM patients p
JOIN lab_results l ON p.patient_id = l.patient_id
JOIN diagnoses d ON p.patient_id = d.patient_id
WHERE d.icd10_code LIKE 'E11%'  -- Type 2 Diabetes
  AND p.age > 65
  AND l.test_name = 'HbA1c'
  AND l.test_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
```

### Complex Clinical Cohort: Heart Failure Readmission Risk
**Natural Language**: "Identify patients discharged with Heart Failure in 2024 who had a readmission within 30 days, excluding those discharged to hospice. For each, calculate their max creatinine levels during the index stay."

**Rationale**: Supports CMS Hospital Readmissions Reduction Program (HRRP) tracking by identifying 30-day all-cause readmissions for Heart Failure (HF) index stays, with standard exclusions (hospice).

**Generated SQL**:
```sql
WITH IndexAdmissions AS (
    -- Identify index admissions for Heart Failure
    SELECT
        a.admission_id,
        a.patient_id,
        a.discharge_date,
        a.discharge_disposition
    FROM admissions a
    JOIN diagnoses d ON a.admission_id = d.admission_id
    WHERE d.icd10_code LIKE 'I50%'          -- Heart Failure codes
      AND a.discharge_date BETWEEN '2024-01-01' AND '2024-12-31'
      AND a.discharge_disposition != 'HOSPICE' -- Exclusion Criteria
),
Readmissions AS (
    -- Find readmissions within 30 days
    SELECT
        i.patient_id,
        i.admission_id AS index_admission_id,
        r.admission_date AS readmission_date,
        DATEDIFF(r.admission_date, i.discharge_date) AS days_to_readmit
    FROM IndexAdmissions i
    JOIN admissions r ON i.patient_id = r.patient_id
    WHERE r.admission_date > i.discharge_date
      AND r.admission_date <= DATE_ADD(i.discharge_date, INTERVAL 30 DAY)
)
-- Final Output: Cohort with Max Creatinine
SELECT
    r.patient_id,
    r.index_admission_id,
    r.days_to_readmit,
    MAX(CASE
        WHEN l.unit = 'mg/dL' THEN l.val_num
        WHEN l.unit = 'mmol/L' THEN l.val_num / 88.4  -- Value Normalization
        ELSE NULL
    END) as max_creatinine_mgdl
FROM Readmissions r
JOIN lab_events l ON r.index_admission_id = l.admission_id
WHERE l.itemid IN (50912, 50913) -- Creatinine lab codes
GROUP BY r.patient_id, r.index_admission_id, r.days_to_readmit;
```

### Quality Metrics
**Natural Language**: "How many patients were readmitted within 30 days of discharge for heart failure?"

**Rationale**: Aligned with CMS Hospital Readmissions Reduction Program (HRRP) requirements, demonstrating aggregation capabilities for organizational quality reporting by specifically tracking 30-day readmission rates for heart failure populations.

**Generated SQL**:
```sql
SELECT COUNT(DISTINCT r.patient_id) as readmission_count
FROM (
  SELECT a1.patient_id, a1.discharge_date, a2.admission_date
  FROM admissions a1
  JOIN admissions a2 ON a1.patient_id = a2.patient_id
  JOIN diagnoses d ON a2.admission_id = d.admission_id
  WHERE d.icd10_code LIKE 'I50%'  -- Heart failure
    AND a2.admission_date BETWEEN a1.discharge_date AND DATE_ADD(a1.discharge_date, INTERVAL 30 DAY)
    AND a1.admission_id != a2.admission_id
) r
```
