import {IncidentSummary, Incident} from "./incident-type";
import {date} from "quasar";

export const sample_list: IncidentSummary[] = [
  {
    id: 11,
    title: "Production Server for ERP3 Crushed",
    severity_level: "critical",
    reported_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    jira_id_list: ['ISR-11', 'ISR-12', 'ISR-13'],
    resolution_status: "under_investigation",
    occurred_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    impacted_areas: "Customer Relationship Management, ERP3",
  },
  {
    id: 12,
    title: "ERP3 Patch Update deployment is failing",
    severity_level: "high",
    reported_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    jira_id_list: ['ISR-11', 'ISR-12', 'ISR-13'],
    resolution_status: "pending",
    occurred_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    impacted_areas: "Customer Relationship Management, ERP3",
  },
  {
    id: 13,
    title: "Dashboard CoPilot is not reporting contextual information",
    severity_level: "low",
    reported_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    jira_id_list: ['ISR-11', 'ISR-12', 'ISR-13'],
    resolution_status: "temp_solved",
    occurred_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    impacted_areas: "Customer Relationship Management, ERP3",
  },
  {
    id: 14,
    title: "ERP server was slow to respond for 2 hours",
    severity_level: "medium",
    reported_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    jira_id_list: ['ISR-11', 'ISR-12', 'ISR-13'],
    impacted_areas: "Customer Relationship Management, ERP3",
    resolution_status: "solved",
    occurred_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
  }
];

export const sample_incident: Incident = {
  id: 11,
  title: "Production Server for ERP3 Crushed",
  severity_level: "critical",
  reported_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
  jira_id_list: ['ISR-11', 'ISR-12', 'ISR-13'],
  resolution_status: "pending",
  occurred_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
  impacted_areas: "Customer Relationship Management, ERP3",
  description: "Production Server for ERP3 Crushed."
                + "The primary database server storage has reached its limit."
                +" The hardware has only 1TB storage in place. "+
                "It is also lacking replication configuration. All data added after Jan 2025 has been lost",

  reporter: {
    org_rel: 'Internal',
    name: "John Doe",
    designation: "Software Engineering Lead",
    department: "Software Development",
    team: "ERP3 Dev",
    line_manager: "Donuld Trump"
  },
  responsible: {
    name: "Rashed Alam",
    team: "Software Development",
    department: "",
    designation: "",
    line_manager: ""
  },
  resolution: {
    description: "This incident was resolved by the team. The hardware was replaced with a new one. 2TB will not be enough. To avoid future consequence kindly plan for higher volume",
    resolved_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    planned_deadline: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),

    verified_by: "Omar Sani",
    verified_at: date.formatDate(new Date("2025-01-01"), "Do MMM, YYYY"),
    lessons_learned: "A resource tracking system is mendatory",
    preventive_measure: "any cloud instance should have a resource tracking system in place. "
  }
}


