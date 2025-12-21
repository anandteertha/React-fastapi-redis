import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import './Reports.css'

function Reports() {
  const { data: reports, isLoading, error } = useQuery({
    queryKey: ['reports'],
    queryFn: async () => {
      const response = await api.get('/reports')
      return response.data
    },
  })

  if (isLoading) {
    return <LoadingSpinner fullScreen={true} />
  }

  if (error) {
    return (
      <div className="reports-page">
        <h1>Daily Reports</h1>
        <div className="error-state">
          <p>Failed to load reports. Please try again.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="reports-page">
      <h1>Daily Reports</h1>
      {reports && reports.length > 0 ? (
        <div className="reports-list">
          {reports.map((report) => (
            <div key={report.id} className="report-card">
              <div className="report-header">
                <h2>
                  {new Date(report.report_date).toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </h2>
              </div>
              <div className="report-stats">
                <div className="stat">
                  <span className="stat-label">Calories</span>
                  <span className="stat-value">{report.total_calories.toFixed(0)}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Protein</span>
                  <span className="stat-value">{report.total_protein.toFixed(1)}g</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Carbs</span>
                  <span className="stat-value">{report.total_carbs.toFixed(1)}g</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Fats</span>
                  <span className="stat-value">{report.total_fats.toFixed(1)}g</span>
                </div>
              </div>
              {report.analysis && (
                <div className="report-section">
                  <h3>Analysis</h3>
                  <p>{report.analysis}</p>
                </div>
              )}
              {report.recommendations && (
                <div className="report-section">
                  <h3>Recommendations</h3>
                  <p>{report.recommendations}</p>
                </div>
              )}
              {report.motivation_message && (
                <div className="report-section motivation">
                  <h3>💪 Motivation</h3>
                  <p>{report.motivation_message}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No reports available. Start logging meals to generate reports!</p>
        </div>
      )}
    </div>
  )
}

export default Reports

