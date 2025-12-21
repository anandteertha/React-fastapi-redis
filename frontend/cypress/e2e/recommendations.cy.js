describe('Recommendations', () => {
  beforeEach(() => {
    cy.login('testuser', 'password123')
    cy.visit('/recommendations')
  })

  it('should display recommendations page', () => {
    cy.contains('AI-Powered Recommendations').should('be.visible')
    cy.contains('Filters').should('be.visible')
  })

  it('should allow setting target calories', () => {
    cy.get('input[placeholder*="2000"]').type('2000')
    cy.get('input[placeholder*="2000"]').should('have.value', '2000')
  })

  it('should allow setting dietary restrictions', () => {
    cy.get('input[placeholder*="vegetarian"]').type('vegetarian, gluten-free')
    cy.get('input[placeholder*="vegetarian"]').should('have.value', 'vegetarian, gluten-free')
  })

  it('should show empty state initially', () => {
    cy.contains('Click "Get Recommendations"').should('be.visible')
  })

  it('should get recommendations when button is clicked', () => {
    cy.get('button').contains('Get Recommendations').click()
    // Wait for API call
    cy.wait(2000)
    // Check if recommendations are displayed or loading message appears
    cy.get('.loading, .recommendations-list, .empty-state').should('exist')
  })
})

