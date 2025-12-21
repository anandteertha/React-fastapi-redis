import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import LoadingSpinner from './LoadingSpinner'
import './PreferenceForm.css'

/**
 * Reusable PreferenceForm component
 * Handles user food preferences and dietary restrictions
 */
function PreferenceForm() {
  const [formData, setFormData] = useState({
    target_calories: '',
    target_protein: '',
    target_carbs: '',
    target_fats: '',
    preferred_meal_times: '',
    dietary_restrictions: [],
  })

  const [newRestriction, setNewRestriction] = useState('')
  const [restrictionSeverity, setRestrictionSeverity] = useState('moderate')

  const queryClient = useQueryClient()

  const { data: preferences, isLoading } = useQuery({
    queryKey: ['preferences'],
    queryFn: async () => {
      try {
        const response = await api.get('/preferences')
        return response.data
      } catch (error) {
        if (error.response?.status === 404) {
          return null
        }
        throw error
      }
    },
  })

  useEffect(() => {
    if (preferences) {
      setFormData({
        target_calories: preferences.target_calories || '',
        target_protein: preferences.target_protein || '',
        target_carbs: preferences.target_carbs || '',
        target_fats: preferences.target_fats || '',
        preferred_meal_times: preferences.preferred_meal_times || '',
        dietary_restrictions: preferences.dietary_restrictions || [],
      })
    }
  }, [preferences])

  const mutation = useMutation({
    mutationFn: async (data) => {
      const response = await api.post('/preferences', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['preferences'])
      // Toast is handled by API interceptor
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    mutation.mutate({
      target_calories: formData.target_calories ? parseFloat(formData.target_calories) : null,
      target_protein: formData.target_protein ? parseFloat(formData.target_protein) : null,
      target_carbs: formData.target_carbs ? parseFloat(formData.target_carbs) : null,
      target_fats: formData.target_fats ? parseFloat(formData.target_fats) : null,
      preferred_meal_times: formData.preferred_meal_times || null,
      dietary_restrictions: formData.dietary_restrictions.map((r) => ({
        restriction_type: r.restriction_type,
        severity: r.severity,
      })),
    })
  }

  const handleAddRestriction = () => {
    if (newRestriction.trim()) {
      setFormData({
        ...formData,
        dietary_restrictions: [
          ...formData.dietary_restrictions,
          {
            restriction_type: newRestriction.trim(),
            severity: restrictionSeverity,
          },
        ],
      })
      setNewRestriction('')
    }
  }

  const handleRemoveRestriction = (index) => {
    setFormData({
      ...formData,
      dietary_restrictions: formData.dietary_restrictions.filter((_, i) => i !== index),
    })
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  return (
    <form onSubmit={handleSubmit} className="preference-form">
      <h2>Nutrition Preferences</h2>

      <div className="form-section">
        <h3>Daily Targets</h3>
        <div className="form-grid">
          <div className="form-group">
            <label>Target Calories</label>
            <input
              type="number"
              value={formData.target_calories}
              onChange={(e) =>
                setFormData({ ...formData, target_calories: e.target.value })
              }
              placeholder="e.g., 2000"
            />
          </div>
          <div className="form-group">
            <label>Target Protein (g)</label>
            <input
              type="number"
              value={formData.target_protein}
              onChange={(e) =>
                setFormData({ ...formData, target_protein: e.target.value })
              }
              placeholder="e.g., 150"
            />
          </div>
          <div className="form-group">
            <label>Target Carbs (g)</label>
            <input
              type="number"
              value={formData.target_carbs}
              onChange={(e) =>
                setFormData({ ...formData, target_carbs: e.target.value })
              }
              placeholder="e.g., 200"
            />
          </div>
          <div className="form-group">
            <label>Target Fats (g)</label>
            <input
              type="number"
              value={formData.target_fats}
              onChange={(e) =>
                setFormData({ ...formData, target_fats: e.target.value })
              }
              placeholder="e.g., 65"
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3>Dietary Restrictions</h3>
        <div className="restriction-input">
          <input
            type="text"
            value={newRestriction}
            onChange={(e) => setNewRestriction(e.target.value)}
            placeholder="e.g., vegetarian, vegan, gluten-free"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault()
                handleAddRestriction()
              }
            }}
          />
          <select
            value={restrictionSeverity}
            onChange={(e) => setRestrictionSeverity(e.target.value)}
          >
            <option value="strict">Strict</option>
            <option value="moderate">Moderate</option>
            <option value="flexible">Flexible</option>
          </select>
          <button type="button" onClick={handleAddRestriction}>
            Add
          </button>
        </div>
        <div className="restrictions-list">
          {formData.dietary_restrictions.map((restriction, index) => (
            <div key={index} className="restriction-item">
              <span>
                {restriction.restriction_type} ({restriction.severity})
              </span>
              <button
                type="button"
                onClick={() => handleRemoveRestriction(index)}
                className="remove-btn"
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="form-section">
        <h3>Preferred Meal Times</h3>
        <textarea
          value={formData.preferred_meal_times}
          onChange={(e) =>
            setFormData({ ...formData, preferred_meal_times: e.target.value })
          }
          placeholder="e.g., Breakfast: 8am, Lunch: 1pm, Dinner: 7pm"
          rows="3"
        />
      </div>

      <button type="submit" className="submit-btn" disabled={mutation.isPending}>
        {mutation.isPending ? (
          <>
            <LoadingSpinner size="small" /> Saving...
          </>
        ) : (
          'Save Preferences'
        )}
      </button>
    </form>
  )
}

export default PreferenceForm

