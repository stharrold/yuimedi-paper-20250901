# Multimedia Appendix 1

## Validated Query Triple Examples for Healthcare Analytics

This appendix illustrates the Validated Query Triple artifact proposed by the HITL-KG framework (see Section 2.2 of the main paper). Each triple comprises three components: (1) **Natural Language Intent**, the clinical business question; (2) **Executable SQL**, the technical implementation; and (3) **Rationale Metadata**, the contextual "why" behind the logic. Together, these components capture not just *what* query was run but *why* it was constructed that way, preserving institutional knowledge that would otherwise be lost during staff turnover.

---

### Triple 1: Diabetes Care Monitoring

**Natural Language Intent:** "Show me all diabetic patients over 65 who had an HbA1c test in the last 6 months"

**Executable SQL:**
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

**Rationale Metadata:** Aligned with NCQA HEDIS measures for Comprehensive Diabetes Care (CDC), monitoring HbA1c testing compliance in older adult populations. Uses ICD-10 E11% for Type 2 Diabetes specifically (not E10% for Type 1) per organizational coding convention. Six-month window matches the HEDIS reporting period.

---

### Triple 2: Heart Failure Readmission Cohort

**Natural Language Intent:** "Identify patients discharged with Heart Failure in 2024 who had a readmission within 30 days, excluding those discharged to hospice. For each, calculate their max creatinine levels during the index stay."

**Executable SQL:**
```sql
WITH IndexAdmissions AS (
    SELECT
        a.admission_id,
        a.patient_id,
        a.discharge_date,
        a.discharge_disposition
    FROM admissions a
    JOIN diagnoses d ON a.admission_id = d.admission_id
    WHERE d.icd10_code LIKE 'I50%'
      AND a.discharge_date BETWEEN '2024-01-01' AND '2024-12-31'
      AND a.discharge_disposition != 'HOSPICE'
),
Readmissions AS (
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
SELECT
    r.patient_id,
    r.index_admission_id,
    r.days_to_readmit,
    MAX(CASE
        WHEN l.unit = 'mg/dL' THEN l.val_num
        WHEN l.unit = 'mmol/L' THEN l.val_num / 88.4
        ELSE NULL
    END) as max_creatinine_mgdl
FROM Readmissions r
JOIN lab_events l ON r.index_admission_id = l.admission_id
WHERE l.itemid IN (50912, 50913)
GROUP BY r.patient_id, r.index_admission_id, r.days_to_readmit;
```

**Rationale Metadata:** Supports CMS Hospital Readmissions Reduction Program (HRRP) tracking. Hospice exclusion per CMS 2025 rules (discharge disposition != 'HOSPICE'). Creatinine unit normalization (mmol/L to mg/dL via /88.4) required because our lab system stores results in mixed units depending on the originating facility. Lab item IDs 50912 and 50913 are MIMIC-III creatinine codes; local implementations must map to their own lab dictionary.

---

### Triple 3: Quality Metric Aggregation

**Natural Language Intent:** "How many patients were readmitted within 30 days of discharge for heart failure?"

**Executable SQL:**
```sql
SELECT COUNT(DISTINCT r.patient_id) as readmission_count
FROM (
  SELECT a1.patient_id, a1.discharge_date, a2.admission_date
  FROM admissions a1
  JOIN admissions a2 ON a1.patient_id = a2.patient_id
  JOIN diagnoses d ON a2.admission_id = d.admission_id
  WHERE d.icd10_code LIKE 'I50%'
    AND a2.admission_date BETWEEN a1.discharge_date
        AND DATE_ADD(a1.discharge_date, INTERVAL 30 DAY)
    AND a1.admission_id != a2.admission_id
) r
```

**Rationale Metadata:** Aligned with CMS HRRP requirements for organizational quality reporting. COUNT(DISTINCT patient_id) ensures each patient is counted once even if they have multiple readmissions. This is the aggregate metric version of Triple 2; the detailed cohort query should be run first to validate individual cases before reporting the aggregate number.

---

## How Triples Preserve Institutional Knowledge

In traditional analytics workflows, only the SQL (component 2) would be saved, if anything. The Natural Language Intent (component 1) would exist only in an email or chat message. The Rationale Metadata (component 3), the most critical knowledge for institutional continuity, would exist only in the departing analyst's memory.

When a new analyst inherits these triples, they receive not just executable code but the clinical reasoning, regulatory context, and institutional conventions that informed the query's construction. This is the mechanism by which HITL-KG converts ephemeral analytical work into durable organizational memory.

## References

1. National Committee for Quality Assurance (NCQA). HEDIS measures and technical resources. 2025. Available from: https://www.ncqa.org/hedis/
2. Centers for Medicare and Medicaid Services (CMS). Hospital Readmissions Reduction Program (HRRP). 2025. Available from: https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps/hospital-readmissions-reduction-program-hrrp
