# Power BI Dashboard Walkthrough

This dashboard is designed as a short maintenance-analytics journey rather than a wall of charts.

## Page 1 — Fleet overview

**Question:** Where is the maintenance burden concentrated?  
**Visual intent:** establish scale quickly with top ATA chapters, repeat-discrepancy rates, and a headline KPI.  
**Decision supported:** where a maintenance leader should look first.

The strongest story on this page is the separation between volume and recurrence: ATA 53 is not only the highest-volume chapter, it also carries the highest repeat-discrepancy rate in the dataset.

![Power BI recurring burden page](screenshots/powerbi_page_1.png)

## Page 2 — Trend analysis

**Question:** Is the burden changing over time?  
**Visual intent:** show whether observed problems are isolated spikes or persistent patterns.  
**Decision supported:** whether the issue needs a one-time response or a longer-term corrective strategy.

The month-over-month trend shows recurring volume, while the year-over-year repeat-rate view helps reveal which ATA chapters remain stubbornly persistent.

![Power BI trend analysis page](screenshots/powerbi_page_2.png)

## Page 3 — Aircraft detail

**Question:** Which aircraft deserve deeper investigation?  
**Visual intent:** move from fleet-level patterns into drill-down analysis by aircraft family and aircraft ID.  
**Decision supported:** which aircraft should be paired with richer operator data such as labor hours, utilization, and corrective-action history.

This page is intentionally where the analysis becomes more cautious. The current project can identify suspicious clusters, but the SDR dataset alone cannot prove true operational readiness or root cause.

![Power BI aircraft detail page](screenshots/powerbi_page_3.png)

## Design choices

- **Three pages, one narrative:** overview → trend → detail
- **Few visuals per page:** enough to answer the question without burying the signal
- **Shared operational language:** ATA chapters, repeat discrepancies, and readiness-style metrics
- **Explicit caveats:** the dashboard is useful because it avoids claiming more than the source data can support

## If this were deployed in an actual maintenance organization

The next version would add:

1. actual utilization hours
2. labor-hour and downtime records
3. corrective-action outcomes
4. age / cycle exposure
5. operator or fleet segmentation

That would turn this from a strong burden-analysis dashboard into a true maintenance decision-support product.
