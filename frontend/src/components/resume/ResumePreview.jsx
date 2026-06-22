import { useState } from 'react'

function ResumePreview({ resumeData }) {
  const [expanded, setExpanded] = useState(false)

  if (!resumeData) return null

  const skills = resumeData.skills || []
  const projects = resumeData.projects || []
  const experience = resumeData.experience || []
  const education = resumeData.education || []
  const coursework = resumeData.coursework || []
  const extracurriculars = resumeData.extracurriculars || []

  return (
    <div
      className={`bg-bg-card border border-border rounded-2xl p-6 transition-all duration-200 ${
        expanded ? 'max-w-7xl w-full' : 'max-w-md'
      }`}
    >
      <p className="text-text-secondary text-sm mb-1">Step 2</p>
      <h2 className="text-text-primary text-lg font-semibold mb-4">Resume analyzed</h2>

      {/* Compact summary — only visible when collapsed */}
      {!expanded && (
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between">
            <span className="text-text-secondary text-sm">Skills detected</span>
            <span className="text-text-primary text-sm font-medium">{skills.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-text-secondary text-sm">Projects</span>
            <span className="text-text-primary text-sm font-medium">{projects.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-text-secondary text-sm">Experience</span>
            <span className="text-text-primary text-sm font-medium">{experience.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-text-secondary text-sm">Education</span>
            <span className="text-text-primary text-sm font-medium">{education.length}</span>
          </div>
          {coursework.length > 0 && (
            <div className="flex items-center justify-between">
              <span className="text-text-secondary text-sm">Coursework</span>
              <span className="text-text-primary text-sm font-medium">{coursework.length}</span>
            </div>
          )}
          {extracurriculars.length > 0 && (
            <div className="flex items-center justify-between">
              <span className="text-text-secondary text-sm">Extracurriculars</span>
              <span className="text-text-primary text-sm font-medium">{extracurriculars.length}</span>
            </div>
          )}

          {/* Skill pills preview — only when collapsed */}
          <div className="flex flex-wrap gap-1.5 pt-1">
            {skills.slice(0, 5).map((skill) => (
              <span key={skill} className="bg-accent-soft text-accent text-xs px-2.5 py-1 rounded-full">
                {skill}
              </span>
            ))}
            {skills.length > 5 && (
              <span className="text-text-secondary text-xs px-2.5 py-1">
                +{skills.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      <button
        onClick={() => setExpanded(!expanded)}
        className="text-accent text-sm font-medium hover:underline"
      >
        {expanded ? '← Hide details' : 'View full details →'}
      </button>

      {/* Full details — wide, two-column grid layout */}
      {expanded && (
        <div className="mt-5 pt-5 border-t border-border grid grid-cols-2 gap-x-8 gap-y-5">
          <div className="col-span-2">
            <p className="text-text-secondary text-xs mb-2">All skills</p>
            <div className="flex flex-wrap gap-1.5">
              {skills.map((skill) => (
                <span key={skill} className="bg-accent-soft text-accent text-xs px-2.5 py-1 rounded-full">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div>
            <p className="text-text-secondary text-xs mb-2">Projects</p>
            <ul className="space-y-1">
              {projects.map((p) => (
                <li key={p.name} className="text-text-primary text-sm">• {p.name}</li>
              ))}
            </ul>
          </div>

          {experience.length > 0 && (
            <div>
              <p className="text-text-secondary text-xs mb-2">Experience</p>
              <ul className="space-y-1">
                {experience.map((exp, i) => (
                  <li key={i} className="text-text-primary text-sm">
                    • {exp.role} {exp.organization && `at ${exp.organization}`}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {education.length > 0 && (
            <div>
              <p className="text-text-secondary text-xs mb-2">Education</p>
              <ul className="space-y-1">
                {education.map((edu, i) => (
                  <li key={i} className="text-text-primary text-sm">
                    • {edu.degree}, {edu.institution}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {coursework.length > 0 && (
            <div>
              <p className="text-text-secondary text-xs mb-2">Relevant coursework</p>
              <div className="flex flex-wrap gap-1.5">
                {coursework.map((course) => (
                  <span key={course} className="bg-bg-card-hover text-text-secondary text-xs px-2.5 py-1 rounded-full">
                    {course}
                  </span>
                ))}
              </div>
            </div>
          )}

          {extracurriculars.length > 0 && (
            <div>
              <p className="text-text-secondary text-xs mb-2">Extracurriculars</p>
              <ul className="space-y-1">
                {extracurriculars.map((x, i) => (
                  <li key={i} className="text-text-primary text-sm">• {x.activity}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ResumePreview
