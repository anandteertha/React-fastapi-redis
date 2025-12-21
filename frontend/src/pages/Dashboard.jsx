import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import './Dashboard.css'

function Dashboard() {
  const { data: todayReport, isLoading } = useQuery({
    queryKey: ['report', 'today'],
    queryFn: async () => {
      const response = await api.get('/reports/today')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      {todayReport ? (
        <div className="dashboard-content">
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Calories</h3>
              <p className="stat-value">{todayReport.total_calories.toFixed(0)}</p>
            </div>
            <div className="stat-card">
              <h3>Protein</h3>
              <p className="stat-value">{todayReport.total_protein.toFixed(1)}g</p>
            </div>
            <div className="stat-card">
              <h3>Carbs</h3>
              <p className="stat-value">{todayReport.total_carbs.toFixed(1)}g</p>
            </div>
            <div className="stat-card">
              <h3>Fats</h3>
              <p className="stat-value">{todayReport.total_fats.toFixed(1)}g</p>
            </div>
          </div>
          {todayReport.analysis && (
            <div className="analysis-card">
              <h2>Today's Analysis</h2>
              <p>{todayReport.analysis}</p>
            </div>
          )}
          {todayReport.recommendations && (
            <div className="recommendations-card">
              <h2>Recommendations</h2>
              <p>{todayReport.recommendations}</p>
            </div>
          )}
          {todayReport.motivation_message && (
            <div className="motivation-card">
              <h2>💪 Motivation</h2>
              <p>{todayReport.motivation_message}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="empty-state">
          <p>No data for today. Start logging your meals!</p>
        </div>
      )}
    </div>
  )
}

export default Dashboard

