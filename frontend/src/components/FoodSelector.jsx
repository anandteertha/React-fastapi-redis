import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import LoadingSpinner from './LoadingSpinner'
import './FoodSelector.css'

/**
 * Reusable FoodSelector component
 * Allows users to search and select foods
 */
function FoodSelector({ onSelect, selectedFoods = [] }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [quantity, setQuantity] = useState(100)

  const { data: foods, isLoading } = useQuery({
    queryKey: ['foods', searchQuery],
    queryFn: async () => {
      if (!searchQuery) {
        const response = await api.get('/foods?limit=20')
        return response.data
      }
      const response = await api.get(`/foods/search?q=${searchQuery}&limit=10`)
      return response.data
    },
    enabled: true,
  })

  const handleAddFood = (food) => {
    onSelect({
      food_id: food.id,
      quantity_g: quantity,
      food: food,
    })
    setQuantity(100)
  }

  return (
    <div className="food-selector">
      <div className="search-section">
        <input
          type="text"
          placeholder="Search foods..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        <input
          type="number"
          placeholder="Quantity (g)"
          value={quantity}
          onChange={(e) => setQuantity(parseFloat(e.target.value) || 0)}
          className="quantity-input"
          min="1"
        />
      </div>

      {isLoading ? (
        <div className="loading-container">
          <LoadingSpinner size="small" />
          <p>Loading foods...</p>
        </div>
      ) : (
        <div className="food-list">
          {foods?.map((food) => (
            <div key={food.id} className="food-item">
              <div className="food-info">
                <h4>{food.name}</h4>
                <p className="food-macros">
                  {food.calories_per_100g} cal | {food.protein_per_100g}g protein |{' '}
                  {food.carbs_per_100g}g carbs | {food.fats_per_100g}g fats
                </p>
              </div>
              <button
                onClick={() => handleAddFood(food)}
                className="add-food-btn"
                disabled={selectedFoods.some((sf) => sf.food_id === food.id)}
              >
                {selectedFoods.some((sf) => sf.food_id === food.id)
                  ? 'Added'
                  : 'Add'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default FoodSelector

