import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import FoodSelector from '../components/FoodSelector'
import LoadingSpinner from '../components/LoadingSpinner'
import './Meals.css'

function Meals() {
  const [selectedFoods, setSelectedFoods] = useState([])
  const [mealType, setMealType] = useState('breakfast')
  const [notes, setNotes] = useState('')
  const queryClient = useQueryClient()

  const { data: meals, isLoading } = useQuery({
    queryKey: ['meals'],
    queryFn: async () => {
      const response = await api.get('/meals')
      return response.data
    },
  })

  const mutation = useMutation({
    mutationFn: async (mealData) => {
      const response = await api.post('/meals', mealData)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['meals'])
      queryClient.invalidateQueries(['report'])
      setSelectedFoods([])
      setNotes('')
      // Toast is handled by API interceptor
    },
  })

  const handleAddFood = (food) => {
    setSelectedFoods([...selectedFoods, food])
  }

  const handleRemoveFood = (index) => {
    setSelectedFoods(selectedFoods.filter((_, i) => i !== index))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (selectedFoods.length === 0) {
      return
    }

    mutation.mutate({
      meal_type: mealType,
      meal_date: new Date().toISOString(),
      notes: notes,
      foods: selectedFoods.map((sf) => ({
        food_id: sf.food_id,
        quantity_g: sf.quantity_g,
      })),
    })
  }

  return (
    <div className="meals-page">
      <h1>Meals</h1>
      <div className="meals-container">
        <div className="add-meal-section">
          <h2>Add Meal</h2>
          <form onSubmit={handleSubmit} className="meal-form">
            <div className="form-group">
              <label>Meal Type</label>
              <select
                value={mealType}
                onChange={(e) => setMealType(e.target.value)}
              >
                <option value="breakfast">Breakfast</option>
                <option value="lunch">Lunch</option>
                <option value="dinner">Dinner</option>
                <option value="snack">Snack</option>
              </select>
            </div>
            <FoodSelector onSelect={handleAddFood} selectedFoods={selectedFoods} />
            {selectedFoods.length > 0 && (
              <div className="selected-foods">
                <h3>Selected Foods</h3>
                {selectedFoods.map((sf, index) => (
                  <div key={index} className="selected-food-item">
                    <span>
                      {sf.food.name} - {sf.quantity_g}g
                    </span>
                    <button
                      type="button"
                      onClick={() => handleRemoveFood(index)}
                      className="remove-btn"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}
            <div className="form-group">
              <label>Notes (optional)</label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows="3"
              />
            </div>
            <button type="submit" className="submit-btn" disabled={mutation.isPending || selectedFoods.length === 0}>
              {mutation.isPending ? (
                <>
                  <LoadingSpinner size="small" /> Adding...
                </>
              ) : (
                'Add Meal'
              )}
            </button>
          </form>
        </div>
        <div className="meals-list-section">
          <h2>Recent Meals</h2>
          {isLoading ? (
            <LoadingSpinner />
          ) : meals && meals.length > 0 ? (
            <div className="meals-list">
              {meals.map((meal) => (
                <div key={meal.id} className="meal-card">
                  <div className="meal-header">
                    <h3>{meal.meal_type}</h3>
                    <span className="meal-date">
                      {new Date(meal.meal_date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="meal-foods">
                    {meal.meal_foods.map((mf) => (
                      <div key={mf.id} className="meal-food-item">
                        {mf.food.name} - {mf.quantity_g}g
                      </div>
                    ))}
                  </div>
                  <div className="meal-nutrition">
                    <span>Calories: {meal.total_calories.toFixed(0)}</span>
                    <span>Protein: {meal.total_protein.toFixed(1)}g</span>
                    <span>Carbs: {meal.total_carbs.toFixed(1)}g</span>
                    <span>Fats: {meal.total_fats.toFixed(1)}g</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="empty-state">No meals logged yet</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Meals

