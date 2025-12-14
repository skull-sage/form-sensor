export type ResolutionStatus = 'pending'| 'under_investigation' | 'temp_solved' | 'solved'

export type IncidentSummary = {
  id: number,
  title: string,
  severity_level: 'critical'| 'high' | 'medium' | 'low',
  reported_at: string, // ISO UTC type
  resolution_status: ResolutionStatus,
  occurred_at: string, // ISO UTC type

  jira_id_list?: string[],
  description?: string,
  impacted_areas: string,



}

export type IncidentResponsible = {

    name: string,
    team: string,
    department: string,
    designation: string,
    line_manager: string,

}

export type IncidentReporter = {

  org_rel: 'Internal' | 'External',
  name: string,
  designation: string,
  department: string,
  other_info?: string, // relevant if org_rel is External

  team?: string, // applicable only if org_rel is Internal
  line_manager?: string, // applicable only if org_rel is Internal

}

export type IncidentResolution = {
  planned_deadline: string, // ISO UTC type
  resolved_at: string, // ISO UTC type
  description: string, // how ?

  verified_by: string,
  verified_at: string, // ISO UTC type
  lessons_learned: string,
  preventive_measure: string,

}

export type Incident = IncidentSummary & {
  reporter: IncidentReporter,
  resolution?:  IncidentResolution,
  responsible?: IncidentResponsible,
}



