You are a strategic intelligence analyst. I need to define signal routing rules for an AI intelligence system serving a diversified South African industrial group called Veralogix Group.

The group has 16 companies across these verticals:
- Mining services (Salaria Mining Services, Coal Processors International, Mining Safety Services)
- Equipment (Veralogix Rentals, Veralift)
- Processing (Veralogix Plant, Alpha Technical Solutions)
- Logistics & Trading (Treadstone, Vera-Commodities, Ritz International)
- Energy (IO Green)
- Engineering (Endeto Project Services)
- Security (Aiguille Security)
- Technology (Veramani)
- Automotive (Pencox Auto Air)
- Connectivity (Bioniq)

RESEARCH TASK — For each signal type below, tell me which Veralogix companies should be notified, what specific opportunity it represents for each, and what the urgency level is (immediate / this week / this month):

SIGNAL 1: A new coal mine or coal mine expansion is announced in Mpumalanga or Limpopo.

SIGNAL 2: A major mining company announces a planned 3-week maintenance shutdown at one of their operations.

SIGNAL 3: Eskom announces load-shedding escalation to Stage 4 or higher for an extended period.

SIGNAL 4: A new solar or renewable energy project (50MW+) breaks ground in South Africa.

SIGNAL 5: A large construction project (R500m+) is awarded in a mining region.

SIGNAL 6: A major mining company publishes an RFP for a 3-year equipment rental contract.

SIGNAL 7: A competitor to one of the Veralogix companies is acquired, closes, or significantly downsizes.

SIGNAL 8: Transnet announces a significant disruption to coal export rail capacity.

SIGNAL 9: A government department issues a new mining safety directive or amendment.

SIGNAL 10: A mining company publishes a tender for integrated site security services.

For each signal, return:
- affected_companies: list of Veralogix companies that should be notified
- opportunity_per_company: what the opportunity specifically is for each
- urgency: immediate / this_week / this_month
- recommended_action: what each affected company should do within 48 hours of detection

Format as structured JSON with the signal number as the key.
```