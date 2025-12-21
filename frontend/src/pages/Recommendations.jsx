import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import './Recommendations.css'

function Recommendations() {
  const [targetCalories, setTargetCalories] = useState('')
  const [dietaryRestrictions, setDietaryRestrictions] = useState('')

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['recommendations', targetCalories, dietaryRestrictions],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (targetCalories) params.append('target_calories', targetCalories)
      if (dietaryRestrictions) params.append('dietary_restrictions', dietaryRestrictions)
      
      const response = await api.get(`/recommender/recommendations?${params.toString()}`)
      return response.data
    },
    enabled: false, // Only fetch when button is clicked
  })

  const handleGetRecommendations = () => {
    refetch()
  }

  return (
    <div className="recommendations-page">
      <h1>AI-Powered Recommendations</h1>
      <div className="recommendations-container">
        <div className="filters-section">
          <h2>Filters</h2>
          <div className="form-group">
            <label>Target Calories (optional)</label>
            <input
              type="number"
              value={targetCalories}
              onChange={(e) => setTargetCalories(e.target.value)}
              placeholder="e.g., 2000"
            />
          </div>
          <div className="form-group">
            <label>Dietary Restrictions (comma-separated)</label>
            <input
              type="text"
              value={dietaryRestrictions}
              onChange={(e) => setDietaryRestrictions(e.target.value)}
              placeholder="e.g., vegetarian, gluten-free"
            />
          </div>
          <button onClick={handleGetRecommendations} className="get-recommendations-btn">
            Get Recommendations
          </button>
        </div>
        <div className="recommendations-section">
          <h2>Recommendations</h2>
          {isLoading ? (
            <div className="loading">Loading recommendations...</div>
          ) : data?.recommendations ? (
            <div className="recommendations-list">
              {data.recommendations.map((rec, index) => (
                <div key={index} className="recommendation-card">
                  <h3>{rec.name}</h3>
                  <div className="recommendation-macros">
                    <span>Calories: {rec.calories_per_100g} per 100g</span>
                    <span>Protein: {rec.protein_per_100g}g per 100g</span>
                  </div>
                  {rec.reason && (
                    <p className="recommendation-reason">{rec.reason}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>Click "Get Recommendations" to see personalized food suggestions!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Recommendations

