\## Missing Values

\* \*\*Initial Report:\*\* Printed and reviewed prior to pipeline execution.

\* \*\*Sensor Gaps:\*\* Short gaps (limit=2) in `temperature\_c`, `humidity\_pct`, and `co2\_ppm` were imputed using forward-fill (`ffill`), assuming short-term MCAR dropouts (e.g., power blips).

\* \*\*Target Variable:\*\* Rows with missing `yield\_kg` after forward-filling were explicitly dropped.



\## Outliers \& Anomalies

\* \*\*Threshold Filters:\*\* Applied explicit bounding rules for an oyster mushroom polyhouse. Readings outside these ranges were treated as sensor failures (e.g., dead probes) rather than rare microclimate events.

\* \*\*Ranges:\*\* Humidity (50-100%), Temperature (10-35°C), CO2 (400-2000 ppm). 



\## Duplicates

\* \*\*Resolution:\*\* Duplicate timestamps, likely caused by double exports, were removed. The `last` recorded reading for any duplicate timestamp was kept.

