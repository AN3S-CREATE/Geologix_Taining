You are a market intelligence researcher building a comprehensive tender monitoring system for a South African industrial group operating across mining services, logistics, energy, equipment rental, security, IT, and construction.

RESEARCH TASK — Return all of the following as structured data:

1. NATIONAL TENDER PORTALS
For each of these tender portals, provide: portal name, URL, update frequency, registration requirements, data format (HTML / PDF / API / RSS), and which Veralogix Group sectors benefit most:
- National Treasury eTenders (etenders.gov.za)
- CIDB (cidb.org.za)
- Eskom supplier portal
- Transnet supplier portal
- DMRE procurement notices
- Armscor (if relevant to security)
- Any other major national tender portal

2. KEY MINING HOUSE PROCUREMENT PORTALS
Which South African mining companies maintain supplier portals or publish procurement opportunities? For each, provide:
- Mining company name
- Supplier portal URL
- Registration process
- Commodities they mine (coal / chrome / gold / platinum / iron ore, etc.)
- Which Veralogix Group companies could supply them

3. MUNICIPAL TENDER SOURCES
List the top 15 South African municipalities most likely to publish tenders relevant to an industrial group (security services, connectivity, solar installation, construction, equipment hire):
- Municipality name
- Tender portal URL
- Province
- Update frequency

4. INDUSTRY-SPECIFIC TENDER AGGREGATORS
Are there any South African tender aggregator services (paid or free) that consolidate mining, construction, and government tenders? List each with URL, cost model, and coverage.

5. TENDER DATA FORMAT ASSESSMENT
For each portal listed in sections 1–3: does it expose data via an API, RSS feed, or bulk download? Or is it scrape-only? This determines the collection method for the Geologix Vanguard database.

Format your entire response as structured JSON with keys: national_portals, mining_house_portals, municipal_portals, aggregators, data_format_assessment.
```