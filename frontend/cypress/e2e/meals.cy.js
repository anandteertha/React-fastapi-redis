describe('Meals', () => {
  beforeEach(() => {
    cy.login('testuser', 'password123')
    cy.visit('/meals')
  })

  it('should display meals page', () => {
    cy.contains('Meals').should('be.visible')
    cy.contains('Add Meal').should('be.visible')
  })

  it('should allow selecting meal type', () => {
    cy.get('select').first().select('lunch')
    cy.get('select').first().should('have.value', 'lunch')
  })

  it('should search for foods', () => {
    cy.get('input[placeholder="Search foods..."]').type('chicken')
    cy.wait(1000) // Wait for API call
    cy.get('.food-item').should('exist')
  })
})

